from mini_framework.web.std_models.errors import MiniHTTPException

class InstitutionNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "INSTITUTION_NOT_FOUND", "Institution not found.", "事业/行政单位不存在")

class InstitutionStatusError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "INSTITUTION_STATUS_ERROR", "Institution Status Error .", "事业/行政单位当前的状态不支持此操作,请检查状态")
