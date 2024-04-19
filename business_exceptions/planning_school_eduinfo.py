from mini_framework.web.std_models.errors import MiniHTTPException


class PlanningSchoolEduinfoNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_EDUINFO_NOT_FOUND", "PlanningSchoolEduinfo not found.", "规划校教学信息不存在")
