from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.enum_value_rule import EnumValueRule
from rules.task_rule import TaskRule
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.enum_value import EnumValue
from views.models.task import TaskActionType


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class TaskView(BaseView):
    def __init__(self):
        super().__init__()
        self.task_rule = get_injector( TaskRule)

    async def page(self,
                   page_request=Depends(PageRequest),
                   task_start_time:str= Query(None, title="", description=" ",min_length=1,max_length=100,example='2020-10-10'),
                   task_id:str= Query('', title="", description="任务编号",min_length=1,max_length=50,example='2zAkahKMTUmkJTAGirG3en'),
                   user_id: int = Query(0, description="", example='1'),
                   ):
        # print(page_request)
        items = []

        res = await self.task_rule.query_task_with_page(page_request ,task_start_time,task_id,user_id )
        return res

    async def get(self,
                  task_id:str= Query('', title="", description="任务编号",min_length=1,max_length=50,example='2zAkahKMTUmkJTAGirG3en'),
                                       ):
        res  = await self.task_rule.get_task_by_id(task_id)

        return res
    # todo  启动和 暂停和取消任务依赖于 框架组件 等待框架提供这个功能
    async def patch(self,
                    action_type:TaskActionType= Query('', title="", description="操作 启动 sart",min_length=1,max_length=50, ),

                  task_id:list[str]= Query([], title="", description="任务编号 列表",  ),
                  ):
        if action_type==TaskActionType.START:
            for task_id in task_id:
                await self.task_rule.start_task(task_id)
        if action_type==TaskActionType.STOP:
            for task_id in task_id:
                await self.task_rule.start_task(task_id)
        if action_type==TaskActionType.CANCEL:
            for task_id in task_id:
                await self.task_rule.cancel_task(task_id)
        # res  = await self.task_rule.get_task_by_id(task_id)

        return {}