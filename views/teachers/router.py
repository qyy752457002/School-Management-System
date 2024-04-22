from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.teachers.teachers_view import TeachersView
from views.teachers.newteachers_view import NewTeachersView
from views.teachers.teachers_extend_view import TeacherLearnExperienceView



def routers():
    router = Router()
    router.include_api_view_class(TeachersView, "/v1/teachers",  description="在职教师管理")
    router.include_api_view_class(NewTeachersView, "/v1/new-teachers", description="新入职教师管理")
    router.include_api_view_class(TeacherLearnExperienceView, "/v1/teacher-extend", description="教师扩展信息管理")
    return router
