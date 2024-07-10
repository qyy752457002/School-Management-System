from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.institution_rule import InstitutionRule


# from web_test.rules.planning_school_rule import InstitutionRule
# from web_test.views.models.account import InstitutionCreateModel
from models.institution import Institution as Institutions
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.models.institutions import Institutions as InstitutionsModel

class InstitutionExecutor(TaskExecutor):
    def __init__(self):
        self.institution_rule = get_injector(InstitutionRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
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
            # data =await self._storage_rule.get_file_data(info.file_name, info.bucket,info.scene)
            for item in data:
                if isinstance(item, dict):
                    institution_import: Institutions = Institutions(**item)
                elif isinstance(item, Institutions):
                    institution_import: Institutions = item
                elif isinstance(item, InstitutionsModel):
                    institution_import: InstitutionsModel = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.institution_rule.add_school(institution_import)
                print('插入数据res',res)
            logger.info(f"Institution   created")
            context.task.result_file=''
            task.result_file=''
        except Exception as e:
            print(e,'异常')
            logger.error(f"Institution   create failed")


# 导出  todo
class InstitutionExportExecutor(TaskExecutor):
    async def execute(self, task: 'FileTask'):
        print("test")
        print(dict(task))
