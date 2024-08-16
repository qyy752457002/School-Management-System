from mini_framework.web.std_models.errors import MiniHTTPException


# 无权限
class NoPermissionError(MiniHTTPException):
    def __init__(self):
        super().__init__(403, "NO_PERMISSION", "No permission.", "用户无权限")
