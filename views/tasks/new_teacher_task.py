from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.teachers_rule import TeachersRule
from models.teachers import Teacher as Teachers
from views.models.teachers import Teachers as TeachersModel
from views.models.teachers import TeachersCreatModel

class NewTeacherExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        super().__init__()

    async def execute(self, context: 'Context'):
        print('开始执行task')
        task: Task = context.task
        print(task)
        if isinstance(task.payload, dict):
            teacher_import: Teachers = Teachers(**task.payload)
        elif isinstance(task.payload, Teachers):
            teacher_import: Teachers = task.payload
        elif isinstance(task.payload, TeachersModel):
            teacher_import: TeachersModel = task.payload
        else:
            raise ValueError("Invalid payload type")
        res = await self.teacher_rule.add_teachers(teacher_import)
        print('插入数据res',res)
        logger.info(f"Teacher {teacher_import.username} created")

# 导出  todo





