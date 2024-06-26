from datetime import datetime

import shortuuid
from mini_framework.async_task.data_access.models import TaskInfo, TaskProgress, TaskResult
from mini_framework.async_task.task import Task, TaskState
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.toolkit.model_utilities import view_model_to_orm_model, orm_model_to_view_model

from daos.task_dao import TaskDAO
# from views.models.task import Task as TaskModel
from mini_framework.async_task.task import Task as TaskModel



@dataclass_inject
class TaskRule(object):
    task_dao: TaskDAO

    async def create_task(self, task: Task):
        """
        添加任务
        :param task: 任务
        :return:
        """
        task.created_at = task.created_at or datetime.now()
        task_info: TaskInfo = view_model_to_orm_model(task, TaskInfo)
        task_info.last_updated = datetime.now()
        task_progress: TaskProgress = view_model_to_orm_model(task, TaskProgress)
        task_progress.progress_id = shortuuid.uuid()
        task_progress.last_updated = datetime.now()
        task_progress.progress_desc = ""
        task_progress.task_id = task.task_id
        task_results: TaskResult = view_model_to_orm_model(task, TaskResult)
        task_results.result_id = shortuuid.uuid()
        task_results.last_updated = datetime.now()
        task_info = await self.task_dao.add_task(task_info)
        task_process = await self.task_dao.add_task_progress(task_progress)
        task_results = await self.task_dao.add_task_result(task_results)
        return task_info, task_process, task_results

    async def progress_change(
        self,
        task: Task,
        progress: float,
        desc: str,
        state: TaskState,
        result_extra=None,
        result_file: str = "",
    ):
        """
        添加任务进度
        :param task: 任务
        :param progress: 进度
        :param desc: 描述
        :param state: 状态
        :param result_extra: 额外结果
        :param result_file: 结果文件
        :return:
        """
        if result_extra is None:
            result_extra = {}
        task_progress = TaskProgress()
        task_progress.progress_id = shortuuid.uuid()
        task_progress.task_id = task.task_id
        task_progress.last_updated = datetime.now()
        task_progress.progress_desc = desc
        task_progress.progress = progress
        task.progress = progress

        if state != task.state:
            task.state = state
            task_results = TaskResult()
            task_results.result_id = shortuuid.uuid()
            task_results.task_id = task.task_id
            task_results.state = state
            task_results.result_extra = result_extra
            task_results.result_file = result_file
            task_results.last_updated = datetime.now()
            await self.task_dao.add_task_result(task_results)

        return await self.task_dao.add_task_progress(task_progress)

    def cancel_task(self, task):
        pass


    async def query_task_with_page(self, page_request: PageRequest, task_start_time,task_id,user_id,  ):
        paging = await self.task_dao.query_task_with_page(page_request,task_start_time,task_id,user_id,  )
        # 字段映射的示例写法   , {"hash_password": "password"} SystemConfigSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, TaskModel,other_mapper={

        })
        title= ''
        return paging_result

    async def get_task_by_id(self, task_id):
        task_db = await self.task_dao.get_task_by_id(task_id)
        # 可选 , exclude=[""]
        task = orm_model_to_view_model(task_db, TaskModel)
        return task