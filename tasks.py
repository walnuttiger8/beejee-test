from app import create_app
import os


app = create_app()
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 320029))
    app.run(debug=False, port=port)
