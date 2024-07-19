import traceback

from mini_framework.async_task.consumers import TaskExecutor
# from mini_framework.async_task.task.task import Task
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.classes_rule import ClassesRule
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule
from rules.planning_school_rule import PlanningSchoolRule
# from rules.school_rule import PlanningSchoolRule
from rules.school_rule import SchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.common.common_view import map_keys
from views.models.classes import Classes, ClassesImport
from views.models.school import School

class ClassExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
        self.class_rule = get_injector(ClassesRule)
        self.system_rule = get_injector(SystemRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)

        super().__init__()

    async def execute(self, context: 'Task'):
        task: Task = context
        print(task)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            print('开始执行task')

            info = task.payload
            logger.debug( f"{info}",  )

            data= [ ]
            if info.file_name.isdecimal():
                # 得到的是下载链接  下载到本地
                fileinfo =await self.system_rule.get_download_url_by_id(info.file_name)
                logger.debug('根据ID下载文件', f"{fileinfo}",  )
                data =await self._storage_rule.get_file_data(info.file_name, '',info.scene,file_direct_url=fileinfo)
                logger.debug('根据URL解析数据', f"{data}",  )
                pass
            else:
                # 得到的是 3个参数   下载到本地

                data =await self._storage_rule.get_file_data(info.file_name, info.virtual_bucket_name,info.scene,file_direct_url=None)
                logger.debug('根据URL解析数据', f"{data}",  )
                pass
            # 枚举值等的查询 todo 这个初始的 和转换需要涉及每个都有 考虑调整为数组 批量处理
            psr = await self.class_rule.init_enum_value_rule()


            for item in data:
                itemd= dict()
                if isinstance(item, dict):
                    data_import: Classes = Classes(**item)

                elif isinstance(item, Classes):
                    data_import: Classes = item
                elif isinstance(item, ClassesImport):
                    # 视图模型
                    data_import: ClassesImport = item
                    itemd = data_import.dict()
                    # 检查每个值如果有右侧换行符 去掉
                    for key, value in itemd.items():
                        if value and isinstance(value, str) and value.endswith('\n'):
                            itemd[key] = value.rstrip('\n')

                    # itemd = map_keys(itemd, self.institution_rule.other_mapper)
                    # todo 需要进行 映射转换  选择的是汉字  根据映射转换英文枚举写入
                    data_import = Classes(**itemd)
                    # todo 这个转换函数 也需要加
                    await psr.convert_school_to_import_format(data_import)

                else:
                    raise ValueError("Invalid payload type")
                res = await self.class_rule.add_classes(data_import)
                print('插入数据res',res)
                logger.debug( f"{res}",  )

            logger.info(f"任务   created")
        except Exception as e:
            print(e,'异常')
            logger.debug( f"任务   create failed", traceback.format_exception(e))

            # logger.error(f"任务   create failed")

# 导出
class ClassExportExecutor(TaskExecutor):
    def __init__(self):
        self.school_rule = get_injector(SchoolRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        super().__init__()
    async def execute(self, task: 'Task'):
        pass
