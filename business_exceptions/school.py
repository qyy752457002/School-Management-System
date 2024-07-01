from mini_framework.web.std_models.errors import MiniHTTPException


class SchoolNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SCHOOL_NOT_FOUND", "School not found.", "学校不存在")

class SchoolValidateError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SCHOOL_VALIDATE_FAILED", "School validae failed.", "缺乏必要参数|请检查参数")

class SchoolBaseInfoValidateError(BaseException ):
    def __init__(self):
        super().__init__(404, "SCHOOL_VALIDATE_FAILED", "School validae failed.", "缺乏必要参数|请检查参数")

class SchoolStatusError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SCHOOL_STATUS_ERROR", "School Status Error .", "学校当前的状态不支持此操作,请检查状态")
