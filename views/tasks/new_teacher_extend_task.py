from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.teacher_work_experience_rule import TeacherWorkExperienceRule
from views.models.teachers import TeacherFileStorageModel
from rules.teacher_extend_import_rule import TeacherExtendImportRule


class TeacherWorkExperienceImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_work_experience_rule = get_injector(TeacherWorkExperienceRule)
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task = context
            logger.info("Test")
            logger.info("Teacher work experience import begins")
            task: Task = task
            logger.info("Test2")
            if isinstance(task.payload, dict):
                teacher_work_experience_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_work_experience_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            await self.teacher_extend_import_rule.import_teacher_work_experience(task)

        except Exception as e:
            logger.error(f"Teacher work experience import failed")
            logger.error(e)
            raise e
