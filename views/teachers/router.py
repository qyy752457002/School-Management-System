from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.teachers.teachers_view import TeachersView
from views.teachers.newteachers_view import NewTeachersView
from views.teachers.teachers_extend_view import TeacherLearnExperienceView, TeacherWorkExperienceView, \
    TeacherJobAppointmentsView, TeacherProfessionalTitlesView, TeacherQualificationsView, TeacherSkillCertificatesView, \
    TeacherEthicRecordsView,EducationalTeachingView
from views.teachers.teachers_extend_view import DomesticTrainingView,OverseasStudyView,TalentProgramView,AnnualReviewView,ResearchAchievementsView
from views.teachers.teacher_work_flow_define import WorkFlowDefineView


def routers():
    router = Router()
    router.include_api_view_class(TeachersView, "/v1/teachers", description="在职教师管理")
    router.include_api_view_class(NewTeachersView, "/v1/new-teachers", description="新入职教师管理")
    router.include_api_view_class(TeacherLearnExperienceView, "/v1/teacher-extend", description="教师学习经历信息管理")
    router.include_api_view_class(TeacherWorkExperienceView, "/v1/teacher-extend", description="教师工作经历信息管理")
    router.include_api_view_class(TeacherJobAppointmentsView, "/v1/teacher-extend", description="教师岗位任聘管理")
    router.include_api_view_class(TeacherProfessionalTitlesView, "/v1/teacher-extend", description="教师专业技术职位信息管理")
    router.include_api_view_class(TeacherQualificationsView, "/v1/teacher-extend", description="教师资格信息管理")
    router.include_api_view_class(TeacherSkillCertificatesView, "/v1/teacher-extend",
                                  description="教师技能证书信息管理")
    router.include_api_view_class(TeacherEthicRecordsView, "/v1/teacher-extend", description="教师师德记录信息管理")
    router.include_api_view_class(EducationalTeachingView, "/v1/teacher-extend", description="教师教育教学信息管理")
    router.include_api_view_class(DomesticTrainingView, "/v1/teacher-extend", description="教师国内培训信息管理")
    router.include_api_view_class(OverseasStudyView, "/v1/teacher-extend", description="教师海外研修信息管理")
    router.include_api_view_class(TalentProgramView, "/v1/teacher-extend", description="教师入学人才项目信息管理")
    router.include_api_view_class(AnnualReviewView, "/v1/teacher-extend", description="教师年度考核信息管理")
    router.include_api_view_class(ResearchAchievementsView, "/v1/teacher-extend", description="教师科研项目管理")
    router.include_api_view_class(WorkFlowDefineView, "/v1/teacher-workflow", description="教师工作流定义配置管理")

    return router
