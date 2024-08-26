import traceback

from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from rules.institution_rule import InstitutionRule


# from web_test.rules.planning_school_rule import InstitutionRule
# from web_test.views.models.account import InstitutionCreateModel
from models.institution import Institution as Institutions
from rules.school_communication_rule import SchoolCommunicationRule
from rules.school_rule import SchoolRule
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.common.common_view import map_keys
from views.models.institutions import Institutions as InstitutionsModel, InstitutionsImport
from views.models.school import SchoolBaseInfoOptional
from views.models.school_communications import SchoolCommunications


class InstitutionExecutor(TaskExecutor):
    def __init__(self):
        self.institution_rule = get_injector(InstitutionRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        self.school_communication_rule = get_injector(SchoolCommunicationRule)

        super().__init__()

    async def execute(self, context: 'Task'):
        task: Task = context
        print(task)
        # 读取 文件内容  再解析到 各个的 插入 库
        try:
            print('开始执行task')
            info = task.payload
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
            # 枚举值等的查询
            psr = await self.institution_rule.init_enum_value_rule()


            # data =await self._storage_rule.get_file_data(info.file_name, info.bucket,info.scene)
            for item in data:
                itemd= dict()

                if isinstance(item, dict):
                    # db模型
                    institution_import: Institutions = Institutions(**item)
                elif isinstance(item, Institutions):
                    institution_import: Institutions = item
                elif isinstance(item, InstitutionsImport):
                    # 视图模型
                    institution_import: InstitutionsImport = item
                    itemd = institution_import.dict()
                    # 检查每个值如果有右侧换行符 去掉
                    for key, value in itemd.items():
                        if value and isinstance(value, str) and value.endswith('\n'):
                            itemd[key] = value.rstrip('\n')

                    itemd = map_keys(itemd, self.institution_rule.other_mapper)
                    # todo 需要进行 映射转换  选择的是汉字  根据映射转换英文枚举写入
                    institution_import = SchoolBaseInfoOptional(**itemd)
                    await psr.convert_school_to_import_format(institution_import)
                else:
                    raise ValueError("Invalid payload type")
                res = await self.institution_rule.add_school(institution_import)
                print('插入数据res',res)
                logger.debug( f"{res}",  )
                itemd.update({'school_id': int(res.id)})
                resc =  SchoolCommunications(**itemd)
                resc.id= 0
                newid = str(res.id)
                print(resc, '模型23', res.id, type(res.id))
                logger.debug('得到的结果视图模型 communication', f"{resc}",  )

                resc.school_id = int(newid)
                print(resc, newid, '||||||||')

                # 保存通信信息
                res_comm = await self.school_communication_rule.add_school_communication(resc,
                                                                                         convertmodel=True)
                print(res_comm, '模型2 res')
                logger.debug('得到的结果视图模型 communication', f"{res_comm}",  )
            logger.info(f"Institution   created")
            # context.task.result_file=''
            # task.result_file=''
        except Exception as e:
            print(e,'异常')
            logger.error(f"Institution   create failed")
            logger.error(e)


# 导出  todo
class InstitutionExportExecutor(TaskExecutor):
    def __init__(self):
        self.institution_rule = get_injector(InstitutionRule)
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)
        super().__init__()
    async def execute(self, task: 'Task'):
        print("test")
        print(dict(task))
        task: Task = task

        try:
            logger.info("负载" ,task.payload)

            task_result = await self.institution_rule.institution_export(task)
            task.result_file = task_result.result_file
            task.result_bucket = task_result.result_bucket
            logger.info("负载" ,task.payload)

        except Exception as e:
            logger.error(f"任务   create failed")
            traceback.print_exc()
            logger.debug( f"任务   exe failed", traceback.format_exception(e))
            print(e,'异常')
