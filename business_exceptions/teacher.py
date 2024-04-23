from mini_framework.web.std_models.errors import MiniHTTPException
class TeacherNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_NOT_FOUND", "Teacher not found.", "教师不存在")

class TeacherInfoNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_INFO_NOT_FOUND", "TeacherInfo not found.", "教师信息不存在")


class TeacherWorkExperienceNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_WORK_EXPERIENCE_NOT_FOUND", "TeacherWorkExperience not found.", "教师工作经历不存在")

class TeacherLearnExperienceNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_LEARN_EXPERIENCE_NOT_FOUND", "TeacherLearnExperience not found.", "教师学习经历不存在")

class TeacherSkillNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_SKILL_NOT_FOUND", "TeacherSkill not found.", "教师技能不存在")
