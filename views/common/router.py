from mini_framework.web.router import Router

from views.public.school_and_teacher_sync_view import SchoolTeacherView


def routers():
    router = Router()
    router.include_api_view_class(SchoolTeacherView, "/v1/sync", description="同步管理")
    return router
