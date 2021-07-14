from app.api import Api
from app.api.task_status import TaskStatus
from app.config import Config


class Task:
    def __init__(self, data: dict) -> None:
        self.id = data.get("id")
        self.username = data.get("username")
        self.text = data.get("text")
        self.status = str(data.get("status"))
        self.email = data.get("email")


class TaskService:

    @staticmethod
    def get_tasks(sort_field: str, sort_direction: str, page: str) -> list:
        content = Api.get_tasks(sort_field=sort_field, sort_direction=sort_direction, page=page)
        tasks = content.get("tasks")
        return list(map(Task, tasks))

    @staticmethod
    def has_next_page(current_page):
        content = Api.get_tasks(sort_field=None, sort_direction=None, page=current_page)
        tasks = content.get("tasks")
        total_task_count = int(content.get("total_task_count"))
        return total_task_count - Config.TASKS_PER_PAGE * (int(current_page) - 1) - len(tasks) > 0

    @staticmethod
    def edit_task(task_id: int, token: str, text: str, status: bool):
        status = TaskStatus.COMPLETED_EDITED if status else TaskStatus.NOT_COMPLETED_EDITED
        return Api.edit_task(task_id, token, text=text, status=status)
