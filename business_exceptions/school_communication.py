from mini_framework.web.std_models.errors import MiniHTTPException


class SchoolCommunicationNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "SCHOOL_COMMUNICATION_NOT_FOUND", "SchoolCommunication not found.", "学校通信信息不存在")
