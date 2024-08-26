from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from common.decorators import require_role_permission
from views.common.common_view import convert_snowid_in_model
from views.models.classes import Classes
from views.models.grades import Grades

from fastapi import Query, Depends
from rules.classes_rule import ClassesRule
from views.models.planning_school import PlanningSchoolImportReq, PlanningSchoolFileStorageModel
from views.models.school import SchoolTask
from views.models.system import ImportScene


class ClassesView(BaseView):
    def __init__(self):
        super().__init__()
        self.classes_rule = get_injector(ClassesRule)
    @require_role_permission("class", "add")
    async def post(self, classes: Classes):
        print(classes)
        res = await  self.classes_rule.add_classes(classes)
        convert_snowid_in_model(res ,["id", "school_id",'grade_id','session_id','teacher_id','care_teacher_id'])

        return res
    @require_role_permission("class", "view")

    async def page(self,
                   page_request=Depends(PageRequest),

                   borough: str = Query('', title=" ", description=" 行政管辖区", examples=['铁西区']),
                   teacher_name: str = Query('', title=" ", description=" ", examples=['']),
                   block: str = Query('', title=" ", description="地域管辖区", examples=['铁西区']),

                   school_id: int|str  = Query(0, title="学校ID", description="学校ID", examples=[1]),

                   grade_id: int|str  = Query(0, title="年级ID", description="年级ID", examples=[2]),
                   class_name: str = Query('', title="Grade_name", description="班级名称", examples=['一年级'])

                   ):
        school_id= int(school_id)
        # grade_id= int(grade_id)
        print(page_request)
        items = []
        res = await self.classes_rule.query_classes_with_page(page_request, borough, block, school_id, grade_id,
                                                              class_name,teacher_name=teacher_name)
        return res

    # 删除
    @require_role_permission("class", "delete")

    async def delete(self, class_id: str = Query(..., title="", description="班级id", min_length=1, max_length=20,
                                                 example='SC2032633'), ):
        print(class_id)
        res = await self.classes_rule.softdelete_classes(class_id)

        return res

    # 修改 关键信息
    @require_role_permission("class", "edit")

    async def put(self, classes: Classes
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.classes_rule.update_classes(classes)

        return res


    # 班级导入
    async def post_class_import(self,
                                 file:PlanningSchoolImportReq
                                 ) -> Task:
        file_name= file.file_name
        task_model = PlanningSchoolFileStorageModel(file_name=file_name, virtual_bucket_name=file.bucket_name,file_size='51363', scene= ImportScene.CLASS.value)


        task = Task(
            task_type="class_import",
            # 文件 要对应的 视图模型
            payload=task_model,
            # payload=SchoolTask(file_name=file_name, scene= ImportScene.CLASS.value, bucket='class_import' ),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task
