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
class BizDataEmptyError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "BIZDATA_CANNOT_NULL", "BizData can not be null .", "业务数据不能为空")
class OrgCenterApiError(MiniHTTPException):
    def __init__(self,):
        # msgtult = msg if len(msg)>0 else "组织中心api响应失败"
        super().__init__(400, "ORG_CENTER_API_ERROR",  "OrgCenterApiError.", "组织中心api响应失败")
class SocialCreditCodeExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "SOCIAL_CREDIT_CODE_ALREADY_EXIST", "social_credit_code already exist.", "社会信用编码已经存在,不允许重复")