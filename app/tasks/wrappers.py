from flask import session, Response, redirect, flash, url_for
from functools import wraps

def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if not session.get("token"):
            flash("You need be logged")
            return redirect(url_for("tasks.login"))

        return func(*args, **kwargs)
    
    return check_token