from mini_framework.web.std_models.errors import MiniHTTPException


class PlanningSchoolNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_NOT_FOUND", "PlanningSchool not found.", "规划校不存在")

