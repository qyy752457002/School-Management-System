from mini_framework.web.std_models.errors import MiniHTTPException

class TenantNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TENANT_NOT_FOUND", "Tenant not found.", "租户不存在")

class TenantAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TENANT_ALREADY_EXIST", "Tenant already exist.", "租户已存在")
class TenantNotFoundOrUnActiveError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TENANT_NOT_FOUND_OR_UNACTIVE",   "Tenant not found or unactive.", "租户不存在或未激活,请确认地址")
