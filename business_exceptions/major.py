from mini_framework.web.std_models.errors import MiniHTTPException


class MajorNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "MAJOR_NOT_FOUND", "Major not found.", "专业不存在")


class MajorAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "MAJOR_ALREADY_EXIST", "Major already exist.", "专业已存在")

