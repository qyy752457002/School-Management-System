from mini_framework.web.std_models.errors import MiniHTTPException


class InstitutionStatusError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "INSTITUTION_STATUS_ERROR", "Institution Status Error .", "事业/行政单位当前的状态不支持此操作,请检查状态")
