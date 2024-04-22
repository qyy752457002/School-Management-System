from mini_framework.web.std_models.errors import MiniHTTPException


class GraduationStudentNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "GRADUATION_STUDENT_NOT_FOUND", "GraduationStudent not found.", "毕业生不存在")


class GraduationStudentAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "GRADUATION_STUDENT_ALREADY_EXIST", "GraduationStudent already exist.", "毕业生已存在")

