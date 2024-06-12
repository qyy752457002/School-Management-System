from mini_framework.web.std_models.errors import MiniHTTPException


class EnumValueNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ENUM_VALUE_NOT_FOUND", "EnumValue not found.", "枚举值不存在")
class EnumValueNotMatchError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ENUM_VALUE_NOT_MATCH", "EnumValue not match.", "枚举值不匹配")

