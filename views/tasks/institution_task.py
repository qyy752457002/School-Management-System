from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.institution_rule import InstitutionRule
from views.models.institutions import Institutions


# from web_test.rules.account_rule import InstitutionRule
# from web_test.views.models.account import InstitutionCreateModel


class InstitutionExecutor(TaskExecutor):
    def __init__(self):
        self.account_rule = get_injector(InstitutionRule)
        super().__init__()

    async def execute(self, context: 'Context'):
        task: Task = context.task
        if isinstance(task.payload, dict):
            account_create: Institutions = Institutions(**task.payload)
        elif isinstance(task.payload, Institutions):
            account_create: Institutions = task.payload
        else:
            raise ValueError("Invalid payload type")
        await self.account_rule.add_account(account_create)
        logger.info(f"Institution {account_create.username} created")


class InstitutionExportExecutor(TaskExecutor):
    async def execute(self, task: 'Task'):
        print("test")
        print(dict(task))
