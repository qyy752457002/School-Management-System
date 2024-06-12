from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
from rules.storage_rule import StorageRule
from rules.storage_rule import TestExcelReader
from rules.teachers_rule import TeachersRule
from models.teachers import Teacher as Teachers
from views.models.teachers import TeachersCreatModel,TeacherFileStorageModel
import pandas as pd


class TeacherImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        super().__init__()

    async def execute(self, task: "Task"):

        logger.info("Teacher import begins")
        task: Task = task
        if isinstance(task.payload, dict):
            account_export: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
        elif isinstance(task.payload, TeacherFileStorageModel):
            account_export: TeacherFileStorageModel = task.payload
        else:
            raise ValueError("Invalid payload type")
        task_result = await self.teacher_rule.import_teachers(task)
        logger.info(f"Teacher import to {task_result.result_file}")

# 导出  todo
