import requests
from .exceptions import ApiException
from .response_status import ResponseStatus

DEVELOPER = "Bulat"


class Api:
    _base_url = "https://uxcandy.com/~shapoval/test-task-backend/v2"

    def _get(self, url, params):
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

    def _post(self, url, data):
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

    def get_tasks(self, sort_field: str = None, sort_direction: str = None, page: str = None) -> dict:
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
        content = self._get(url, params)
        print(content)
        return content

    def create_task(self, username: str, email: str, text: str):
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
        content = self._post(url, data)
        return content

    def login(self, username, password) -> dict:
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
        content = self._post(url, data)
        return content

    def edit_task(self, task_id: int, token: str, text: str = None, status: str = None):
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
        content = self._post(url, data)
        return content


if __name__ == '__main__':
    api = Api()
    print(api.get_tasks())  # 26302
    print(api.login("admin", "123"))
    token = "b1AvTjRMOWpQWDRQY21iQWVvUzdROW8xSmZ0d1dZcWVCQTFraWFlOTJGczU0dHNwM3Zndmw1ZnNoNGgvWlA0SDVacmZNYlFaVUN2NTh6RnJQcVBvblE9PQ=="
    print(api.edit_task(26302, token, "Edited text"))
    print(api.get_tasks())  # 26302
