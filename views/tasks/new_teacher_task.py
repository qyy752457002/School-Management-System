from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
from rules.storage_rule import StorageRule
from rules.storage_rule import TestExcelReader
from rules.teachers_rule import TeachersRule
from models.teachers import Teacher as Teachers
from views.models.teachers import TeachersCreatModel
import pandas as pd


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
            SampleModel = TeachersCreatModel
            source_file = task.source_file
            excel_file = pd.ExcelFile(source_file)
            sheet_name = excel_file.sheet_names[0]

            data = []
            data = TestExcelReader(source_file, sheet_name, SampleModel).read_valid()
            print(len(data), 'data')
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
