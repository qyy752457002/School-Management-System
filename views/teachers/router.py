from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.teachers.teachers_view import TeachersView
from views.teachers.newteachers_view import NewTeachersView
from views.teachers.teachers_extend_view import TeacherLearnExperienceView, TeacherWorkExperienceView, \
    TeacherJobAppointmentsView, TeacherProfessionalTitlesView, TeacherQualificationsView, TeacherSkillCertificatesView, \
    TeacherEthicRecordsView,EducationalTeachingView,TeacherExtendImportView
from views.teachers.teachers_extend_view import DomesticTrainingView,OverseasStudyView,TalentProgramView,AnnualReviewView,ResearchAchievementsView
from views.teachers.teacher_work_flow_define import WorkFlowDefineView
from views.teachers.teacher_transaction_view import TeacherTransactionView
from views.teachers.teacher_transaction_view import TeacherBorrowView
from views.teachers.teacher_transaction_view import TransferDetailsView
from views.teachers.teacher_transaction_view import  TeacherRetireView


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

    router.include_api_view_class(TeacherTransactionView, "/v1/teacher-transaction", description="教师变动管理")
    router.include_api_view_class(TeacherBorrowView, "/v1/teacher-transaction", description="教师借动管理")
    router.include_api_view_class(TransferDetailsView, "/v1/teacher-transaction", description="教师调动管理")
    router.include_api_view_class(TeacherRetireView, "/v1/teacher-transaction", description="教师退休管理")
    router.include_api_view_class(TeacherExtendImportView, "/v1/teacher-extend-import", description="教师扩展信息导入")


    return router
