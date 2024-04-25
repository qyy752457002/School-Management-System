from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.operation_record import OperationRecordRule
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.operation_record import OperationRecord, OperationTargetType, OperationModule, OperationType


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class OperationRecordView(BaseView):
    def __init__(self):
        super().__init__()
        self.operation_record_rule = get_injector(OperationRecordRule)

    async def page(self,
                   page_request=Depends(PageRequest),
                   operation_target_type: OperationTargetType = Query(None, title="", description="操作主体类型",
                                                                      example='school', min_length=1, max_length=25),

                   action_target_id: int = Query(None, title="", description="主体id(规划校/学校/老师/学生等的ID)",
                                                 example='1'),
                   operater_account: str = Query(None, title="", description="操作账号", example='admin', min_length=1,
                                                 max_length=25),
                   operater_id: int = Query(None, title="", description="操作人ID", example='1', ),
                   operation_module: OperationModule = Query(None, title="", description="操作模块", example='admin',
                                                             min_length=1, max_length=25),
                   operation_type: OperationType = Query(None, title="", description="操作对象", example='admin',
                                                         min_length=1, max_length=25),

                   ):
        print(page_request)
        items = []
        res = await self.operation_record_rule.query_operation_record_with_page(page_request, operation_target_type,
                                                                                action_target_id, operater_account,
                                                                                operater_id, operation_module,
                                                                                operation_type

                                                                                )
        return res
