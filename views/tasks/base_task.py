import traceback

from mini_framework.async_task.consumers import TaskExecutor
# from mini_framework.async_task.task.task import Task
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.classes_rule import ClassesRule
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule
from rules.planning_school_rule import PlanningSchoolRule
# from rules.school_rule import PlanningSchoolRule
from rules.school_rule import SchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.common.common_view import map_keys
from views.models.classes import Classes, ClassesImport
from views.models.school import School

class BaseExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
        self.class_rule = get_injector(ClassesRule)
        self.system_rule = get_injector(SystemRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)

        super().__init__()
    #     定义一个自动解析负载得到数据的方法
    async def parse_payload_to_data(self, payload):
        info= payload
        data=None
        if info.file_name.isdecimal():
            # 得到的是下载链接  下载到本地
            fileinfo =await self.system_rule.get_download_url_by_id(info.file_name)
            logger.debug('根据ID下载文件', f"{fileinfo}",  )
            data =await self._storage_rule.get_file_data(info.file_name, '',info.scene,file_direct_url=fileinfo)
            logger.debug('根据URL解析数据', f"{data}",  )
            pass
        else:
            # 得到的是 3个参数   下载到本地

            data =await self._storage_rule.get_file_data(info.file_name, info.virtual_bucket_name,info.scene,file_direct_url=None)
            logger.debug('根据URL解析数据', f"{data}",  )
            pass
        return data

