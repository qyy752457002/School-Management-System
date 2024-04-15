from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.teachers.teachers_view import TeachersView


def routers():
    router = Router()
    router.include_api_view_class(TeachersView, "/v1/teachers", response_cls=Teachers, description="教师管理")
    return router
