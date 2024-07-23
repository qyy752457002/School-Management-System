import datetime

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
import traceback
# from rules.new_student_rule import PlanningNewStudentRule
# from rules.new_student_rule import NewStudentRule
from rules.storage_rule import StorageRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_family_info_rule import StudentsFamilyInfoRule
from rules.students_rule import StudentsRule
from rules.system_rule import SystemRule
from views.models.students import NewStudents, NewBaseInfoCreate, NewStudentsQuery, StudentsFamilyInfoCreate, \
    NewStudentImport
from views.tasks.base_task import BaseExecutor


# from views.models.students import NewStudent

class NewStudentExecutor(BaseExecutor):
    def __init__(self):
        self.new_student_rule = get_injector(StudentsRule)
        self.system_rule = get_injector(SystemRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        super().__init__()

    async def execute(self, context: 'Task'):
        task: Task = context
        print(task)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            print('开始执行task')

            info = task.payload
            data =await self.parse_payload_to_data(info)

            # 枚举值等的查询 todo 这个初始的 和转换需要涉及每个都有 考虑调整为数组 批量处理
            psr = await self.new_student_rule.init_enum_value()

            for item in data:
                itemd= dict()
                if isinstance(item, dict):
                    data_import: NewStudents = NewStudents(**item)
                elif isinstance(item, NewStudents):
                    data_import: NewStudents = item
                elif isinstance(item, NewStudentImport):
                    # 视图模型
                    data_import: NewStudentImport = item
                    itemd = data_import.dict()
                    # 检查每个值如果有右侧换行符 去掉
                    for key, value in itemd.items():
                        if value and isinstance(value, str) and value.endswith('\n'):
                            itemd[key] = value.rstrip('\n')

                    # itemd = map_keys(itemd, self.institution_rule.other_mapper)
                    # todo 需要进行 映射转换  选择的是汉字  根据映射转换英文枚举写入
                    data_import = NewStudentImport(**itemd)
                    # todo 这个转换函数 也需要加 下面方法改为装饰器

                    await psr.convert_import_format_to_view_model(data_import)
                else:
                    raise ValueError("Invalid payload type")
                students = data_import
                res = await self.new_student_rule.add_students(data_import)
                students.student_id = res.student_id
                special_date = datetime.datetime.now()
                # todo 更多的字段 转换到base里 需要写入

                vm2 = NewBaseInfoCreate(student_id=students.student_id, school_id=students.school_id,
                                        registration_date=special_date.strftime("%Y-%m-%d"),**data_import.__dict__)
                res2 = await self.students_base_info_rule.add_students_base_info(vm2)
                print('插入数据res', res)
            logger.info(f"任务   created")
        except Exception as e:
            print(e, '异常')
            traceback.print_exc()
            logger.error(f"任务   create failed")

class NewStudentFamilyInfoImportExecutor(TaskExecutor):
    """
    导入新生家庭成员信息
    """
    def __init__(self):
        self.new_student_rule = get_injector(StudentsRule)
        self.new_student_familyinfo_rule = get_injector(StudentsFamilyInfoRule)
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
            fileinfo =await self.system_rule.get_download_url_by_id(info.file_name)
            data =await self._storage_rule.get_file_data(info.file_name, info.bucket_name,info.scene)
            # data = await self._storage_rule.get_file_data(info.file_name, info.bucket, info.scene)

            for item in data:
                if isinstance(item, dict):
                    data_import: StudentsFamilyInfoCreate = StudentsFamilyInfoCreate(**item)
                elif isinstance(item, StudentsFamilyInfoCreate):
                    data_import: StudentsFamilyInfoCreate = item
                else:
                    raise ValueError("Invalid payload type")
                students = data_import
                res = await self.new_student_familyinfo_rule.add_students_family_info(data_import)
                students.student_id = res.student_id
                special_date = datetime.datetime.now()

                print('插入数据res', res)
            logger.info(f"任务   created")
        except Exception as e:
            print(e, '异常')
            traceback.print_exc()
            logger.error(f"任务   create failed")



# 导出  todo 新生在校生的导出在这里
class NewStudentExportExecutor(TaskExecutor):
    def __init__(self):
        self.student_rule = get_injector(StudentsRule)
        super().__init__()

    async def execute(self,  task: "Task"):
        try:
            # task = context.task  在字段 "result_file_id" 中空值违反了非空约束
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

