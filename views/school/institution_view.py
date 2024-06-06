from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchool,PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.institutions import Institutions, InstitutionTask
from rules.institution_rule import InstitutionRule
from mini_framework.web.request_context import request_context_manager

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
# 当前工具包里支持get  patch前缀的 方法的自定义使用
class InstitutionView(BaseView):
    def __init__(self):
        super().__init__()
        self.institution_rule = get_injector(InstitutionRule)



    async def page(self,
                   page_request= Depends(PageRequest),
                   # planning_school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  # planning_school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),




                  ):
        print(page_request)
        items=[]
        res = await self.institution_rule.query_institution_with_page(page_request,)
        return res

    async def post_institution_import_example(self, account: Institutions = Body(..., description="")) -> Task:
        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="institution_import",
            # 文件 要对应的 视图模型
            payload=account,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 导入 事业单位      上传文件获取 桶底值

    async def post_institution_import(self,
                                      filename: str = Query(..., description="文件名"),
                                      bucket: str = Query(..., description="文件名"),
                                      scene: str = Query('', description="文件名"),
                                      ) -> Task:
        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="institution_import",
            # 文件 要对应的 视图模型
            payload=InstitutionTask(file_name=filename, bucket=bucket, scene=scene),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task


