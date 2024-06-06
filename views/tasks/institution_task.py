from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.institution_rule import InstitutionRule


# from web_test.rules.institution_rule import InstitutionRule
# from web_test.views.models.account import InstitutionCreateModel
from models.institution import Institution as Institutions
from views.models.institutions import Institutions as InstitutionsModel

class InstitutionExecutor(TaskExecutor):
    def __init__(self):
        self.institution_rule = get_injector(InstitutionRule)
        super().__init__()

    async def execute(self, context: 'Context'):
        print('开始执行task')
        task: Task = context.task
        print(task)
        if isinstance(task.payload, dict):
            institution_import: Institutions = Institutions(**task.payload)
        elif isinstance(task.payload, Institutions):
            institution_import: Institutions = task.payload
        elif isinstance(task.payload, InstitutionsModel):
            institution_import: InstitutionsModel = task.payload
        else:
            raise ValueError("Invalid payload type")
        res = await self.institution_rule.add_institution(institution_import)
        print('插入数据res',res)
        logger.info(f"Institution {institution_import.username} created")

# 导出  todo
class InstitutionExportExecutor(TaskExecutor):
    async def execute(self, task: 'Task'):
        print("test")
        print(dict(task))
