class ApiException(Exception):
    pass


class ApiAuthorizationException(Exception):
    pass


class TokenExpiredException(Exception):
    pass
