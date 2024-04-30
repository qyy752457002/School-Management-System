from mini_framework.web.std_models.errors import MiniHTTPException
class IdCardError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "IDCARD_NOT_TRUE", "IdCard not true.", "身份证号错误")
