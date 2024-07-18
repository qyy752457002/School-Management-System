from mini_framework.web.std_models.errors import MiniHTTPException

class CampusEduinfoNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CAMPUS_EDUINFO_NOT_FOUND", "CampusEduinfo not found.", "校区教学信息不存在")
