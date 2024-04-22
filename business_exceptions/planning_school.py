from mini_framework.web.std_models.errors import MiniHTTPException


class PlanningSchoolNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_NOT_FOUND", "PlanningSchool not found.", "规划校不存在")

class PlanningSchoolValidateError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_VALIDATE_FAILED", "PlanningSchool validae failed.", "缺乏必要参数|请检查参数")

class PlanningSchoolBaseInfoValidateError(BaseException ):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_VALIDATE_FAILED", "PlanningSchool validae failed.", "缺乏必要参数|请检查参数")

