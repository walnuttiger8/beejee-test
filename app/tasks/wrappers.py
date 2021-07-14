from flask import session, redirect, flash, url_for
from functools import wraps


def require_api_token(func):
    """
    Декоратор для проверки токена авторизации
    :param func:
    :return:
    """

    @wraps(func)
    def check_token(*args, **kwargs):
        if not session.get("token"):
            flash("You need be logged")
            return redirect(url_for("tasks.login"))

        return func(*args, **kwargs)

    return check_token
