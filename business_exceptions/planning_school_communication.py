from mini_framework.web.std_models.errors import MiniHTTPException


class PlanningSchoolCommunicationNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "PLANNING_SCHOOL_COMMUNICATION_NOT_FOUND", "PlanningSchoolCommunication not found.", "规划校通信信息不存在")
