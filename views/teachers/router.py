from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.teachers.teachers_view import TeachersView
from views.teachers.newteachers_view import NewTeachersView
from views.teachers.teachers_extend_view import TeacherLearnExperienceView, TeacherWorkExperienceView, \
    TeacherJobAppointmentsView, TeacherProfessionalTitlesView, TeacherQualificationsView, TeacherSkillCertificatesView, \
    TeacherEthicRecordsView,EducationalTeachingView


def routers():
    router = Router()
    router.include_api_view_class(TeachersView, "/v1/teachers", description="在职教师管理")
    router.include_api_view_class(NewTeachersView, "/v1/new-teachers", description="新入职教师管理")
    router.include_api_view_class(TeacherLearnExperienceView, "/v1/teacher-extend", description="教师学习经历信息管理")
    router.include_api_view_class(TeacherWorkExperienceView, "/v1/teacher-extend", description="教师工作经历信息管理")
    router.include_api_view_class(TeacherJobAppointmentsView, "/v1/teacher-extend", description="教师任职信息管理")
    router.include_api_view_class(TeacherProfessionalTitlesView, "/v1/teacher-extend", description="教师职称信息管理")
    router.include_api_view_class(TeacherQualificationsView, "/v1/teacher-extend", description="教师资格信息管理")
    router.include_api_view_class(TeacherSkillCertificatesView, "/v1/teacher-extend",
                                  description="教师技能证书信息管理")
    router.include_api_view_class(TeacherEthicRecordsView, "/v1/teacher-extend", description="教师道德记录信息管理")
    router.include_api_view_class(EducationalTeachingView, "/v1/teacher-extend", description="教师教育教学信息管理")

    return router
