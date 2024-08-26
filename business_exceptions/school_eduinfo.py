from mini_framework.web.std_models.errors import MiniHTTPException


class SchoolEduinfoNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SCHOOL_EDUINFO_NOT_FOUND", "SchoolEduinfo not found.", "学校教学信息不存在")
