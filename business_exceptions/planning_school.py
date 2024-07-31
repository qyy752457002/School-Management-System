from mini_framework.web.std_models.errors import MiniHTTPException


class PlanningSchoolNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_NOT_FOUND", "PlanningSchool not found.", "规划校不存在")
class PlanningSchoolExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_ALREADY_EXISTS",  "PlanningSchool already exists.", "规划校已存在")
class PlanningSchoolValidateError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_VALIDATE_FAILED", "PlanningSchool validae failed.", "缺乏必要参数|请检查参数")

class PlanningSchoolBaseInfoValidateError(BaseException ):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_VALIDATE_FAILED", "PlanningSchool validae failed.", "缺乏必要参数|请检查参数")
class PlanningSchoolStatusError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_STATUS_ERROR", "PlanningSchool Status Error .", "规划校当前的状态不支持此操作,请检查状态")
class PlanningSchoolNotFoundByProcessInstanceIdError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_NOT_FOUND_BY_PROCESS_INSTANCEID", "PlanningSchool not found by process_instance.", "未找到流程对应的规划校")


