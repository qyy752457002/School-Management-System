from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
from rules.storage_rule import StorageRule
from rules.teachers_rule import TeachersRule
from models.teachers import Teacher as Teachers
from views.models.teachers import TeachersCreatModel


class TeacherExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_rule = get_injector(TeachersRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        super().__init__()

    async def execute(self, context: 'Context'):

        task: Task = context.task
        print(task)
        try:
            print('开始执行task')
            info = task.payload
            data = []
            data = await self._storage_rule.get_file_data(info.file_name, info.bucket, info.scene)
            for item in data:
                if isinstance(item, dict):
                    teacher_import: Teachers = Teachers(**item)
                elif isinstance(item, Teachers):
                    teacher_import: Teachers = item
                elif isinstance(item, TeachersCreatModel):
                    teacher_import: TeachersCreatModel = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.teacher_rule.add_teachers(teacher_import)
                print('插入数据res', res)
            logger.info(f"Teacher created")
        except Exception as e:
            print(e, '异常')
            logger.error(f"Teacher create failed")

# 导出  todo
