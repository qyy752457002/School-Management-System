from mini_framework.web.std_models.errors import MiniHTTPException


class SubjectNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SUBJECT_NOT_FOUND", "Subject not found.", "课程不存在")


class SubjectAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SUBJECT_ALREADY_EXIST", "Subject already exist.", "课程已存在")

