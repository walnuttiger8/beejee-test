from app.api import Api
from app.api.task_status import TaskStatus
from app.config import Config


class Task:
    """
    Класс для использования в шаблонах.
    """

    def __init__(self, data: dict) -> None:
        self.id = data.get("id")
        self.username = data.get("username")
        self.text = data.get("text")
        self.status = str(data.get("status"))
        self.email = data.get("email")


class TaskService:
    """
    Статический класс для работы с бизнес-логикой
    """

    @staticmethod
    def get_tasks(sort_field: str, sort_direction: str, page: str) -> list:
        """
        Преобразовывает стандартный ответ API в удобный для отображения в шаблонах вид
        :param sort_field: Поле сортировки
        :param sort_direction: Направление сортировки
        :param page: Страница
        :return: Список задач
        :rtype: list[Task]
        """
        content = Api.get_tasks(sort_field=sort_field, sort_direction=sort_direction, page=page)
        tasks = content.get("tasks")
        return list(map(Task, tasks))

    @staticmethod
    def has_next_page(current_page) -> bool:
        """
        Проверяет, есть ли у текущей страницы следующая (для пагинации)
        :param current_page: текущая страница
        :rtype: bool
        """
        content = Api.get_tasks(sort_field=None, sort_direction=None, page=current_page)
        tasks = content.get("tasks")
        total_task_count = int(content.get("total_task_count"))
        return total_task_count - Config.TASKS_PER_PAGE * (int(current_page) - 1) - len(tasks) > 0

    @staticmethod
    def edit_task(task_id: int, token: str, text: str, status: bool) -> None:
        """
        Обертка для редактирования задачи.
        :param task_id: id задачи
        :param token: токен авторизации
        :param text: новый текст задачи
        :param status: новый статус задачи
        :return: None
        """
        status = TaskStatus.COMPLETED_EDITED if status else TaskStatus.NOT_COMPLETED_EDITED
        return Api.edit_task(task_id, token, text=text, status=status)
