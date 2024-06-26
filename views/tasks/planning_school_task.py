import traceback

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule
from rules.planning_school_rule import PlanningSchoolRule
from rules.storage_rule import StorageRule
from views.models.planning_school import PlanningSchool
from views.models.planning_school_communications import PlanningSchoolCommunications


class PlanningSchoolExecutor(TaskExecutor):
    def __init__(self):
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)

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
                    data_import: PlanningSchool = PlanningSchool(**item)

                elif isinstance(item, PlanningSchool):
                    data_import: PlanningSchool = item
                else:
                    raise ValueError("Invalid payload type")
                res = await self.planning_school_rule.add_planning_school(data_import)
                print('得到的结果视图模型 ', res, '模型1')
                # 解析 拆分到第二个模型
                data_import.id =    0

                data_import.planning_school_id =   int(res.id)
                resc =  PlanningSchoolCommunications(**data_import.__dict__)
                resc.id= 0
                newid = str(res.id)
                print(resc, '模型23', res.id, type(res.id))

                resc.planning_school_id = int(newid)
                print(resc, newid, '||||||||')

                # 保存通信信息
                res_comm = await self.planning_school_communication_rule.add_planning_school_communication(resc,
                                                                                                           convertmodel=False)
                print(res_comm, '模型2 res')

                print('插入数据res',res)
            logger.info(f"任务   created")
        except Exception as e:
            traceback.print_exc()
            print(e,'异常')
            logger.error(f"任务   create failed")


# 导出  todo
class PlanningSchoolExportExecutor(TaskExecutor):
    async def execute(self, task: 'FileTask'):
        print("test")
        print(dict(task))
