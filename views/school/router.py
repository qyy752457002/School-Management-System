from mini_framework.web.router import Router

from views.models.school import School
from views.models.test import ApplicationInfo
from views.school.school_view import SchoolView
from views.tests.test_view import TestView


def routers():
    router = Router()
    router.include_api_view_class(SchoolView, "/v1/school", response_cls=School , description="学校管理")





    return router
