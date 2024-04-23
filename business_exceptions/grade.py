from mini_framework.web.std_models.errors import MiniHTTPException


class GradeNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "GRADE_NOT_FOUND", "Grade not found.", "年级不存在")


class GradeAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "GRADE_ALREADY_EXIST", "Grade already exist.", "年级已存在")

