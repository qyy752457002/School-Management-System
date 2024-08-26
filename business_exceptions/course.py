from mini_framework.web.std_models.errors import MiniHTTPException

class CourseNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "COURSE_NOT_FOUND", "Course not found.", "课程不存在")

class CourseAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "COURSE_ALREADY_EXIST", "Course already exist.", "课程已存在")
