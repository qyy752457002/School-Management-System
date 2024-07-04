from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

# from rules.school_rule import PlanningSchoolRule
from rules.school_rule import SchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.models.school import School

class SchoolExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
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
            data= [ ]
            fileinfo = self.system_rule.get_download_url_by_id(info.file_name)
            data =await self._storage_rule.get_file_data(fileinfo.file_name, fileinfo.bucket_name,info.scene)

            for item in data:

                if isinstance(item, dict):
                    data_import: School = School(**item)

                elif isinstance(item, School):
                    data_import: School = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.school_rule.add_school(data_import)
                print('插入数据res',res)
            logger.info(f"任务   created")
        except Exception as e:
            print(e,'异常')
            logger.error(f"任务   create failed")


# 导出  todo
class SchoolExportExecutor(TaskExecutor):
    async def execute(self, task: 'FileTask'):
        print("test")
        print(dict(task))
