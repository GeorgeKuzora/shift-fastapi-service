class DatabaseException(Exception):
    pass


class DataNotFoundException(DatabaseException):
    pass


class LoggingConfigException(Exception):
    pass


class AuthConfigException(Exception):
    pass
