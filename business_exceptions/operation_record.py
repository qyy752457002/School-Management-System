from mini_framework.web.std_models.errors import MiniHTTPException


class OperationRecordNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "OPERATION_RECORD_NOT_FOUND", "OperationRecord not found.", "操作记录不存在")


class OperationRecordAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "OPERATION_RECORD_ALREADY_EXIST", "OperationRecord already exist.", "操作记录已存在")

