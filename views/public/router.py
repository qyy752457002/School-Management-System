from mini_framework.web.router import Router

from views.public.classes_view import ClassesView
from views.public.current_students_view import CurrentStudentsView
from views.public.school_and_teacher_sync_view import SchoolTeacherView


def routers():
    router = Router()
    router.include_api_view_class(CurrentStudentsView, "/v1/public/current-student", description="在校生管理")
    router.include_api_view_class(ClassesView, "/v1/public/class", description="班级管理")
    router.include_api_view_class(SchoolTeacherView, "/v1/sync", description="同步管理")


    return router
