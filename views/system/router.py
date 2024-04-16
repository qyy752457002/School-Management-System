from mini_framework.web.router import Router

from views.models.operation_record import OperationRecord
from views.models.test import ApplicationInfo
from views.school.school_view import SchoolView
from views.system.enum_value_view import EnumValueView
from views.tests.test_view import TestView
from views.models.planning_school import PlanningSchool
from views.system.sub_system_view import SubSystemView
from views.system.operation_record_view import OperationRecordView


def routers():
    router = Router()
    router.include_api_view_class(OperationRecordView, "/v1/system",   description="操作日志管理")

    router.include_api_view_class(SubSystemView, "/v1/subsystem",   description="子系统列表")

    router.include_api_view_class(EnumValueView, "/v1/enums",   description="枚举值列表")



    return router
