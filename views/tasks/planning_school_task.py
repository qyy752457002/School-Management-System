import traceback

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule
from rules.planning_school_rule import PlanningSchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.common.common_view import map_keys
from views.models.planning_school import PlanningSchool, PlanningSchoolOptional, PlanningSchoolPageSearch, \
    PlanningSchoolImport
from views.models.planning_school_communications import PlanningSchoolCommunications

class PlanningSchoolExecutor(TaskExecutor):
    def __init__(self):
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)

        super().__init__()

    async def execute(self, context: 'Task'):

        print('入参 context',context)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            task: Task = context
            print('入参task',task)

            info = task.payload
            print('开始执行task',info)

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


            for item in data:
                itemd= dict()

                if isinstance(item, dict):
                    data_import: PlanningSchoolOptional = PlanningSchoolOptional(**item)
                    print('得到字典')

                elif isinstance(item, PlanningSchoolOptional):
                    data_import: PlanningSchoolOptional = item
                    print('得到对象2')

                elif isinstance(item, PlanningSchoolImport):
                    data_import: PlanningSchoolImport = item
                    print('得到对象3')
                    if data_import.school_type != '学校':
                        continue
                    else:
                        itemd = data_import.dict()
                        itemd = map_keys(itemd, self.planning_school_rule.other_mapper)
                        data_import = PlanningSchoolOptional(**itemd)

                        pass

                else:
                    raise ValueError("Invalid payload type")
                # 这需要转换模型  后面会校验 导致没有规划校名程报错
                res = await self.planning_school_rule.add_planning_school(data_import)
                print('得到的结果视图模型 ', res, '模型1')
                logger.debug('得到的结果视图模型', f"{res}",  )

                # 解析 拆分到第二个模型
                # item.id =    0

                # item.planning_school_id =   int(res.id)
                itemd.update({'planning_school_id': int(res.id)})
                resc =  PlanningSchoolCommunications(**itemd)
                resc.id= 0
                newid = str(res.id)
                print(resc, '模型23', res.id, type(res.id))
                logger.debug('得到的结果视图模型 communication', f"{resc}",  )

                resc.planning_school_id = int(newid)
                print(resc, newid, '||||||||')

                # 保存通信信息
                res_comm = await self.planning_school_communication_rule.add_planning_school_communication(resc,
                                                                                                           convertmodel=True)
                print(res_comm, '模型2 res')
                logger.debug('得到的结果视图模型 communication', f"{res_comm}",  )

                task.result_file =  ''
                task.result_bucket =  ''

                print('插入数据res',res)
                logger.debug( f"{res}",  )

            logger.info(f"任务   success")
        except Exception as e:
            traceback.print_exc()
            print(e,'异常')
            logger.debug( f"任务   执行 failed", traceback.format_exception(e))
            logger.error(e)

            # logger.error(f"任务   create failed")


# 导出  todo
class PlanningSchoolExportExecutor(TaskExecutor):
    def __init__(self):
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        super().__init__()
    async def execute(self, task: 'Task'):
        try:
            print("test")
            print(dict(task))
            task: Task = task
            logger.info("负载的数据" ,task.payload)
            if isinstance(task.payload, dict):
                student_export: PlanningSchoolPageSearch = PlanningSchoolPageSearch(**task.payload)
            elif isinstance(task.payload, PlanningSchoolPageSearch):
                student_export: PlanningSchoolPageSearch = task.payload
            else:
                raise ValueError("Invalid payload type")
            task_result = await self.planning_school_rule.planning_school_export(task)
            task.result_file = task_result.result_file
            task.result_bucket = task_result.result_bucket
            logger.debug("导入规划校的结果" ,task)
        except Exception as e:
            traceback.print_exc()
            logger.debug( f"任务   exe failed", traceback.format_exception(e))



        # task.result_file =  ''
        # task.result_bucket =  ''
