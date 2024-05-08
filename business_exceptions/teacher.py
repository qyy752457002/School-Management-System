from mini_framework.web.std_models.errors import MiniHTTPException
class TeacherNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_NOT_FOUND", "Teacher not found.", "教师不存在")

class TeacherExistsError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_EXISTS_ERROR", "Teacher exists error.", "教师已存在")

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

class TeacherInfoExitError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_INFO_EXIT_ERROR", "TeacherInfo exit error.", "教师基本信息已存在")



class TeacherQualificationsNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_QUALIFICATIONS_NOT_FOUND", "TeacherQualifications not found.", "教师资格证书不存在")


class TeacherJobAppointmentsNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_JOB_APPOINTMENTS_NOT_FOUND", "TeacherJobAppointments not found.", "教师职务任职不存在")


class TeacherProfessionalTitleNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_PROFESSIONAL_TITLE_NOT_FOUND", "TeacherProfessionalTitle not found.", "教师专业技术职位不存在")

class TeacherEthicRecordsNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TEACHER_ETHIC_RECORDS_NOT_FOUND", "TeacherEthnicRecords not found.", "教师师德记录不存在")

class EducationalTeachingNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "EDUCATIONAL_TEACHING_NOT_FOUND", "EducationalTeaching not found.", "教育教学工作不存在")


class DomesticTrainingNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "DOMESTIC_TRAINING_NOT_FOUND", "DomesticTraining not found.", "国内培训不存在")


class OverseasStudyNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "OVERSEAS_STUDY_NOT_FOUND", "OverseasStudy not found.", "海外学习不存在")


class AnnualReviewNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "ANNUAL_REVIEW_NOT_FOUND", "AnnualReview not found.", "年度考核不存在")

class ResearchAchievementsNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "RESEARCH_ACHIEVEMENTS_NOT_FOUND", "ResearchAchievements not found.", "科研成果不存在")

class TalentProgramNotFoundError(MiniHTTPException):
    def __init__(self):
        super().__init__(404, "TALENT_PROGRAM_NOT_FOUND", "TalentProgram not found.", "人才项目不存在")