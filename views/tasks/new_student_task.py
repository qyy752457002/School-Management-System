from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

# from rules.new_student_rule import PlanningNewStudentRule
# from rules.new_student_rule import NewStudentRule
from rules.storage_rule import StorageRule
from rules.students_rule import StudentsRule
from views.models.students import NewStudents


# from views.models.students import NewStudent

class NewStudentExecutor(TaskExecutor):
    def __init__(self):
        self.new_student_rule = get_injector(StudentsRule)
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
            data =await self._storage_rule.get_file_data(info.file_name, info.bucket,info.scene)

            for item in data:

                if isinstance(item, dict):
                    data_import: NewStudents = NewStudents(**item)

                elif isinstance(item, NewStudents):
                    data_import: NewStudents = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.new_student_rule.add_students(data_import)
                print('插入数据res',res)
            logger.info(f"任务   created")
        except Exception as e:
            print(e,'异常')
            logger.error(f"任务   create failed")


# 导出  todo
class NewStudentExportExecutor(TaskExecutor):
    async def execute(self, task: 'FileTask'):
        print("test")
        print(dict(task))
