from mini_framework.web.std_models.errors import MiniHTTPException


class CampusNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CAMPUS_NOT_FOUND", "Campus not found.", "校区不存在")

