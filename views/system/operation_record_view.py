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
from views.models.operation_record import OperationRecord, OperationType, ChangeModule, OperationType, OperationTarget


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class OperationRecordView(BaseView):
    def __init__(self):
        super().__init__()
        self.operation_record_rule = get_injector(OperationRecordRule)

    async def page(self,
                   page_request=Depends(PageRequest),
                   operation_target_type: OperationTarget = Query(None, title="", description="操作的对象的类型",
                                                                  example='school', min_length=1, max_length=25),
                   action_target_id: int | str = Query(None, title="",
                                                       description="主体id(规划校/学校/老师/学生等的ID)",
                                                       example='1'),
                   operater_account: str = Query(None, title="", description="操作账号", example='admin', min_length=1,
                                                 max_length=25),
                   operater_id: int | str = Query(None, title="", description="操作人ID", example='1', ),
                   process_instance_id: int | str = Query(None, title="", description="process_instance_id",
                                                          example='1', ),
                   operation_module: ChangeModule = Query(None, title="", description="操作模块", min_length=1,
                                                          max_length=40, example='key_info_change'),
                   operation_type: OperationType = Query(None, title="", description="操作类型", example='创建',
                                                         min_length=1, max_length=25),
                   ):
        print('入参', page_request)
        if action_target_id:
            action_target_id = int(action_target_id)
        if operater_id:
            operater_id = int(operater_id)
        if process_instance_id:
            process_instance_id = int(process_instance_id)
        items = []
        res = await self.operation_record_rule.query_operation_record_with_page(page_request, operation_target_type,
                                                                                action_target_id, operater_account,
                                                                                operater_id, operation_module,
                                                                                operation_type, process_instance_id
                                                                                )
        return res
