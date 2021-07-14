from flask import request, session, redirect, url_for, render_template, flash
from app.tasks.wrappers import require_api_token
from app.api import Api, SortField, SortDirection, TaskStatus
from app.tasks.services.task_service import TaskService
from app.tasks.forms import LoginForm, TaskForm, EditTaskForm
from app.api.exceptions import ApiAuthorizationException, TokenExpiredException

from app.tasks import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Авторизация
    :return:
    """
    form = LoginForm()
    api = Api()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            data = api.login(username, password)
            token = data.get("token")
        except ApiAuthorizationException:
            flash("Incorrect auth data")
            return redirect(url_for("tasks.login"))
        session["token"] = token
        return redirect(url_for("tasks.index"))

    return render_template("tasks/login.html", title="Sign in", form=form)


@bp.route("/logout")
def logout():
    session["token"] = ""
    return redirect(url_for("tasks.index"))


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    """
    Все посты и добавление
    :return:
    """
    form = TaskForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        text = form.text.data
        Api.create_task(username, email, text)
        flash("Your task is now alive")
        return redirect(url_for("tasks.index"))

    page = request.args.get("page", 1, type=int)
    sort_field = request.args.get("sort_field", SortField.ID, type=str)
    sort_direction = request.args.get("sort_direction", SortDirection.ASC, type=str)

    tasks = TaskService.get_tasks(sort_field, sort_direction, str(page))
    next_url = url_for("tasks.index", page=page + 1, sort_field=sort_field,
                       sort_direction=sort_direction) if TaskService.has_next_page(page) else None
    prev_url = url_for("tasks.index", page=page - 1, sort_field=sort_field,
                       sort_direction=sort_direction) if page > 1 else None

    return render_template("index.html", title="Home", form=form, tasks=tasks, next_url=next_url,
                           prev_url=prev_url, SortDirection=SortDirection, SortField=SortField, sort_field=sort_field,
                           sort_direction=sort_direction, TaskStatus=TaskStatus)


@bp.route("/edit/<task_id>", methods=["GET", "POST"])
@require_api_token
def edit(task_id: int):
    """
    Редактирование задачи
    :param task_id:
    :return:
    """
    form = EditTaskForm()
    if form.validate_on_submit():
        text = form.text.data
        status = form.status.data
        try:
            TaskService.edit_task(task_id, session["token"], text, status)
        except TokenExpiredException:
            flash("Your token has been expired")
            return redirect(url_for("tasks.logout"))
        flash("Your changes has been saved")
        return redirect(url_for("tasks.index"))
    elif request.method == "GET":
        task_text = request.args.get("task_text")
        task_status = request.args.get("task_status")
        task_status = task_status in (TaskStatus.COMPLETED, TaskStatus.COMPLETED_EDITED)
        form.text.data = task_text
        form.status.data = task_status
    return render_template("tasks/edit_task.html", form=form)
