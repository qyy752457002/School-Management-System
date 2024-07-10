import datetime

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
import traceback
# from rules.new_student_rule import PlanningNewStudentRule
# from rules.new_student_rule import NewStudentRule
from rules.storage_rule import StorageRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from rules.system_rule import SystemRule
from views.models.students import NewStudents, NewBaseInfoCreate, NewStudentsQuery


# from views.models.students import NewStudent

class NewStudentExecutor(TaskExecutor):
    def __init__(self):
        self.new_student_rule = get_injector(StudentsRule)
        self.system_rule = get_injector(SystemRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        super().__init__()

    async def execute(self, context: 'Context'):
        task: Task = context.task
        print(task)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            print('开始执行task')

            info = task.payload
            data = []
            fileinfo = self.system_rule.get_download_url_by_id(info.file_name)
            data =await self._storage_rule.get_file_data(fileinfo.file_name, fileinfo.bucket_name,info.scene)
            # data = await self._storage_rule.get_file_data(info.file_name, info.bucket, info.scene)

            for item in data:
                if isinstance(item, dict):
                    data_import: NewStudents = NewStudents(**item)
                elif isinstance(item, NewStudents):
                    data_import: NewStudents = item
                else:
                    raise ValueError("Invalid payload type")
                students = data_import
                res = await self.new_student_rule.add_students(data_import)
                students.student_id = res.student_id
                special_date = datetime.datetime.now()

                vm2 = NewBaseInfoCreate(student_id=students.student_id, school_id=students.school_id,
                                        registration_date=special_date.strftime("%Y-%m-%d"))
                res2 = await self.students_base_info_rule.add_students_base_info(vm2)
                print('插入数据res', res)
            logger.info(f"任务   created")
        except Exception as e:
            print(e, '异常')
            logger.error(f"任务   create failed")


# 导出  todo 新生的导出在这里
class NewStudentExportExecutor(TaskExecutor):
    def __init__(self):
        self.student_rule = get_injector(StudentsRule)
        super().__init__()

    async def execute(self,  context: 'Context'):
        try:
            task = context.task
            logger.info("Test")
            logger.info(" export begins")
            task: Task = task
            logger.info("负载" ,task.payload)
            if isinstance(task.payload, dict):
                student_export: NewStudentsQuery = NewStudentsQuery(**task.payload)
            elif isinstance(task.payload, NewStudentsQuery):
                student_export: NewStudentsQuery = task.payload
            else:
                raise ValueError("Invalid payload type")
            task_result = await self.student_rule.student_export(task)
            task.result_file = task_result.result_file
            task.result_bucket = task_result.result_bucket
            logger.info(f" res  {task_result}")
            print('rule的结构', task_result)
            print('task结果',task)
            logger.info(f" import to {task_result.result_file}")
        except Exception as e:
            logger.error(f" export failed")
            logger.error(e,)
            traceback.print_exc()
            raise e

