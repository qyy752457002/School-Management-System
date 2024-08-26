from mini_framework.web.std_models.errors import MiniHTTPException

class CampusCommunicationNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CAMPUS_COMMUNICATION_NOT_FOUND", "CampusCommunication not found.", "校区通信信息不存在")
