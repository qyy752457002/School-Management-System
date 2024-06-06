from mini_framework.web.std_models.errors import MiniHTTPException
class IdCardError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "IDCARD_NOT_TRUE", "IdCard not true.", "身份证号错误")
class EduNumberError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "EDUNUMBER_ALREADY_EXIST", "EduNumber already exist.", "学籍号已经存在")
class EnrollNumberError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "ENROLLNUMBER_ALREADY_EXIST", "EnrollNumber already exist.", "报名号已经存在")
