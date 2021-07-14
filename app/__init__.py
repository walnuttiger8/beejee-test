import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, current_app
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from app.config import Config

migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    migrate.init_app(app)
    bootstrap.init_app(app)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.tasks import bp as tasks_bp

    app.register_blueprint(tasks_bp)

    if not app.debug and not app.testing:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler("logs/tasks.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("Tasks startup")

    return app
