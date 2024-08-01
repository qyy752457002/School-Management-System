from mini_framework.web.std_models.errors import MiniHTTPException


class StudentSessionNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_SESSION_NOT_FOUND", "StudentSession not found.", "届别不存在")


class StudentSessionAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_SESSION_ALREADY_EXIST", "StudentSession already exist.", "届别已存在")

