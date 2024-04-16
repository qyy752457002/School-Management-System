from mini_framework.web.router import Router

from views.models.operation_record import OperationRecord
from views.models.test import ApplicationInfo
from views.school.school_view import SchoolView
from views.tests.test_view import TestView
from views.models.planning_school import PlanningSchool
from views.school.planning_school_view import PlanningSchoolView
from views.system.operation_record_view import OperationRecordView


def routers():
    router = Router()
    router.include_api_view_class(OperationRecordView, "/v1/system", response_cls=OperationRecord , description="操作日志管理")





    return router
