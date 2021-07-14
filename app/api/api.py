import requests
from .exceptions import ApiException, ApiAuthorizationException, TokenExpiredException
from .response_status import ResponseStatus

DEVELOPER = "Bulat"


class Api:
    _base_url = "https://uxcandy.com/~shapoval/test-task-backend/v2"

    @staticmethod
    def _get(url, params):
        """
        Базовая обертка GET-запроса
        :param url: адрес запроса
        :param params: заголовки
        :return: ответ из поля "message"
        """
        params.update({"developer": DEVELOPER})
        response = requests.get(url, params=params)
        content = response.json()
        if content["status"] == ResponseStatus.ERROR:
            raise ApiException(content.get("message"))

        return content.get("message")

    @staticmethod
    def _post(url, data):
        """
        Базовая обертка POST-запроса
        :param url: адрес запроса
        :param data: тело запроса
        :return: ответ из поля "message"
        """
        params = {"developer": DEVELOPER}
        response = requests.post(url, params=params, data=data)
        content = response.json()
        if content["status"] == ResponseStatus.ERROR:
            raise ApiException(content.get("message"))

        return content.get("message")

    @staticmethod
    def get_tasks(sort_field: str = None, sort_direction: str = None, page: str = None) -> dict:
        """
        Получить список всех задач
        :param sort_field: поле, по которому выполняется сортировка
        :param sort_direction: направление сортировки
        :param page: номер страницы для пагинации
        :return: Словарь: "tasks" (список задач на странице) и "total_task_count" (общее кол-во задач)
        :rtype: dict
        """
        params = {
            "sort_field": sort_field,
            "sort_direction": sort_direction,
            "page": page,
        }
        url = Api._base_url + "/"
        content = Api._get(url, params)
        return content

    @staticmethod
    def create_task(username: str, email: str, text: str):
        """
        Добавление задачи
        :param username: текстовое поле - имя пользователя, который добавляет задачу
        :param email: текстовое поле - email-адрес пользователя, который добавляет задачу,
        email-адрес должен быть валидным
        :param text: текстовое поле - текст задачи
        :return:
        """
        data = {
            "username": username,
            "email": email,
            "text": text,
        }
        url = Api._base_url + "/create"
        content = Api._post(url, data)
        return content

    @staticmethod
    def login(username, password) -> dict:
        """
        Логин. В случае успешной авторизации в теле сообщения будет передан авторизационный токен,
        срок жизни которого - 1 день (24 часа).
        :param username: Имя пользователя
        :param password: Пароль
        :return:
        """
        data = {
            "username": username,
            "password": password,
        }
        url = Api._base_url + "/login"
        try:
            content = Api._post(url, data)
        except ApiException:
            raise ApiAuthorizationException("Ошибка авторизации")
        return content

    @staticmethod
    def edit_task(task_id: int, token: str, text: str = None, status: str = None):
        """
        Редактирование задачи
        Редактирование доступно только для авторизованных пользователей
        :param task_id: id задачи
        :param token: авторизационный токен
        :param text: новый текст задачи
        :param status: новый статус задачи
        :return:
        """
        data = {
            "token": token,
            "text": text,
            "status": status,
        }
        url = Api._base_url + "/edit/" + str(task_id)
        try:
            content = Api._post(url, data)
        except ApiException:
            raise TokenExpiredException("Истек срок действия авторизационного токена")

        return content
