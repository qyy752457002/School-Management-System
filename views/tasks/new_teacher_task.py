from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task import Task
from mini_framework.async_task.task.task_context import Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.teachers_rule import TeachersRule
from views.models.teachers import  TeacherFileStorageModel, CurrentTeacherQuery
from rules.teacher_import_rule import TeacherImportRule


class TeacherImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_import_rule = get_injector(TeacherImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task = context
            operator = task.operator
            logger.info("Test")
            logger.info("Teacher import begins")
            task: Task = task
            logger.info("Test2")
            logger.info(f"{task.payload.virtual_bucket_name}")
            if isinstance(task.payload, dict):
                account_export: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                account_export: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_import_rule.import_teachers(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
        except Exception as e:
            logger.error(f"Teacher import failed")
            logger.error(e)
            raise e


class TeacherSaveImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_import_rule = get_injector(TeacherImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task = context
            operator = task.operator
            logger.info("Test")
            logger.info("Teacher_save import begins")
            task: Task = task
            logger.info("Test2")
            if isinstance(task.payload, dict):
                account_export: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                account_export: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            file_storage_resp = await self.teacher_import_rule.import_teachers_save(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name

        except Exception as e:
            logger.error(f"Teacher import failed")
            logger.error(e)
            raise e


# 导出  todo
class TeacherExportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_import_rule = get_injector(TeacherImportRule)
        super().__init__()

    async def execute(self, context: Context):
        try:
            task = context.task
            logger.info("Test")
            logger.info("Teacher export begins")
            task: Task = task
            logger.info("Test2")
            if isinstance(task.payload, dict):
                teacher_export: CurrentTeacherQuery = CurrentTeacherQuery(**task.payload)
            elif isinstance(task.payload, CurrentTeacherQuery):
                teacher_export: CurrentTeacherQuery = task.payload
            else:
                raise ValueError("Invalid payload type")
            task_result = await self.teacher_rule.teachers_export(task)
            task.result_file = task_result.file_name
            task.result_bucket = task_result.bucket_name
            logger.info(f"Teacher import to {task_result.result_file}")
        except Exception as e:
            logger.error("Teacher export failed")
            logger.error(e)
            raise e
