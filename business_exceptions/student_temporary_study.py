from mini_framework.web.std_models.errors import MiniHTTPException
class StudentTemporaryStudyExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(400, "STUDENT_TEMPORARY_STUDY_EXISTS", "Student Temporary Study  already exists.", "学生临时就读已存在")

class StudentTemporaryStudyNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_TEMPORARY_STUDY_NOT_FOUND", "StudentTemporaryStudy not found.", "就读信息不存在")


class StudentTemporaryStudyAlreadyExistError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "STUDENT_TEMPORARY_STUDY_ALREADY_EXIST", "StudentTemporaryStudy already exist.", "就读信息已存在")

class TargetSchoolError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TARGET_SCHOOL_ERROR", "TargetSchool must not same with current school.", "临时就读学校不能与当前学校一致")

