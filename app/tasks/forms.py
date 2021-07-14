from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class TaskForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired(), Length(min=5, max=255)])
    email = StringField("Email", validators=[Email()])
    submit = SubmitField("Create task")


class EditTaskForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired(), Length(5, 255)])
    status = BooleanField("Status")
    submit = SubmitField("Change")