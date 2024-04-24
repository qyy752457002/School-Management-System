from mini_framework.web.std_models.errors import MiniHTTPException
class StudentNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_NOT_FOUND", "Student not found.", "学生不存在")