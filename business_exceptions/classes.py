from mini_framework.web.std_models.errors import MiniHTTPException


class ClassesNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CLASSES_NOT_FOUND", "Classes not found.", "班级不存在")


class ClassesAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CLASSES_ALREADY_EXIST", "Classes already exist.", "班级已存在")

