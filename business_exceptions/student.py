from mini_framework.web.std_models.errors import MiniHTTPException
class StudentNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_NOT_FOUND", "Student not found.", "学生不存在")

class StudentExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "STUDENT_EXISTS", "Student already exists.", "学生已存在")

class StudentFamilyInfoNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_FAMILY_INFO_NOT_FOUND", "Student family info not found.", "学生家庭信息不存在")
class StudentFamilyInfoExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "STUDENT_FAMILY_INFO_EXISTS", "Student family info already exists.", "学生家庭信息已存在")
class StudentSessionNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_SESSION_NOT_FOUND", "Student session not found.", "未找到开启的届别,请先开启届别")

class StudentExistsThisSchoolError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_EXISTS_IN_THIS_SCHOOL", "Student already exists this school.", "学生已经存在于当前学校")
class StudentTransactionExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_TRANSACTION_EXISTS", "Student Transaction already exists .", "学生已经存在未处理完成的变动,请勿先处理后再提交")
