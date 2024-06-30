from mini_framework.web.std_models.errors import MiniHTTPException
class OriginPositionError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ORIGIN_POSITION_ERROR", "Origin position error.", "原职位必填")

class CurrentPositionError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "CURRENT_POSITION_ERROR", "Current position error.", "现职位必填")


class PositionDateError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "POSITION_DATE_ERROR", "Position date error.", "任职时间必填")


class TransactionError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TRANSACTION_APPROVAL_ERROR", "Transaction  error.", "该老师未在职，不可发起变动")
