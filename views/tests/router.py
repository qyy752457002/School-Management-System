from mini_framework.web.router import Router

from views.models.test import ApplicationInfo
from views.tests.test_view import TestView


def routers():
    router = Router()
    router.include_api_view_class(TestView, "/v1/test", response_cls=ApplicationInfo, description="账户管理")
    return router
