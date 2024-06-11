from mini_framework.web.std_models.errors import MiniHTTPException


class OrganizationNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ORG_NOT_FOUND", "Organization not found.", "输入的组织 不存在")

class OrganizationExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "ORG_ALREADY_EXIST", "Organization already exist.", "组织已经存在")

class OrganizationMemberNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ORG_MEMBER_NOT_FOUND", "Organization member not found.", "输入的组织成员 不存在")

class OrganizationMemberExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "ORG_MEMBER_ALREADY_EXIST", "Organization member already exist.", "组织成员已经存在")

