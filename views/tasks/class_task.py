import traceback

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.classes_rule import ClassesRule
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule
from rules.planning_school_rule import PlanningSchoolRule
# from rules.school_rule import PlanningSchoolRule
from rules.school_rule import SchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.models.classes import Classes
from views.models.school import School

class ClassExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
        self.class_rule = get_injector(ClassesRule)
        self.system_rule = get_injector(SystemRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)

        super().__init__()

    async def execute(self, context: 'Context'):
        task: Task = context.task
        print(task)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            print('开始执行task')

            info = task.payload
            logger.debug( f"{info}",  )

            data= [ ]
            fileinfo =await self.system_rule.get_download_url_by_id(info.file_name)
            logger.debug( f"{fileinfo}",  )

            data =await self._storage_rule.get_file_data(fileinfo.file_name, fileinfo.bucket_name,info.scene,file_direct_url=fileinfo)
            logger.debug( f"{data}",  )

            for item in data:

                if isinstance(item, dict):
                    data_import: Classes = Classes(**item)

                elif isinstance(item, Classes):
                    data_import: Classes = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.class_rule.add_classes(data_import)
                print('插入数据res',res)
                logger.debug( f"{res}",  )

            logger.info(f"任务   created")
        except Exception as e:
            print(e,'异常')
            logger.debug( f"任务   create failed", traceback.format_exception(e))

            # logger.error(f"任务   create failed")


# 导出  todo
class ClassExportExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        super().__init__()
    async def execute(self, task: 'Task'):
        print("test")
        print(dict(task))
        task: Task = task
        logger.info("负载" ,task.payload)

        task_result = await self.school_rule.school_export(task)
        task.result_file = task_result.result_file
        task.result_bucket = task_result.result_bucket
