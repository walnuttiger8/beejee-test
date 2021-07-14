from wtforms.validators import Email


class SortField:
    ID = "id"
    USERNAME = "username"
    EMAIL = "email"
    STATUS = "status"

    description = {
        ID: "Id",
        USERNAME: "Username",
        EMAIL: "Email",
        STATUS: "Status",
    }
