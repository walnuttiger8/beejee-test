from app import create_app
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 320029))
    app = create_app()
    app.run(debug=False, port=port)
