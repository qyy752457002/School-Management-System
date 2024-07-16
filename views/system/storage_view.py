import traceback
from os.path import join

from fastapi.params import Query
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model
from mini_framework.web.views import BaseView

from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule


class StorageView(BaseView):
    def __init__(self):
        super().__init__()
        self._storage_rule: StorageRule = get_injector(StorageRule)
        self.system_rule = get_injector(SystemRule)

    async def get_school_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_school_info_token_uri(filename, file_size)

    async def get_student_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_student_info_token_uri(filename, file_size)

    async def get_teacher_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_teacher_info_token_uri(filename, file_size)

#     解析 文件和桶  返回 数据结构
    async def get_file_data_preview(self, filename: str, bucket:str,
                                    sence:str=Query('',alias='scene',description="", example='1')
                                    ):
        # data = dict()
        data = [ dict()]

        try:
            print('解析的文件',filename,bucket,sence)
            buckets = bucket.split('/')
            filepath = '/'. join( [buckets[1],filename])

            infos = await self._storage_rule.get_file_by_name(filename, buckets[1],filepath )
            # classes = orm_model_to_view_model(info, ClassesModel)
            info = infos._asdict()['FileStorage']

            print('查询文件', f"{info}",)
            logger.debug('查询文件', f"{info}",  )

            fileinfo =await self.system_rule.get_download_url_by_id(str(info.file_id))
            logger.debug('根据ID下载文件', f"{fileinfo}",  )
            res =await self._storage_rule.get_file_data('',  '',sence,file_direct_url=fileinfo)
            logger.debug('根据URL解析数据', f"{data}",  )

            # res = await self._storage_rule.get_file_data(filename, bucket,sence)
            print('解析的结构',res )
            # 存在ID的tuple 过滤掉
            data = [ ]
            for i,value  in  enumerate(res):
                if hasattr(value,'id') and  isinstance(value.id, (Query,tuple)):
                    value.id = 0
                    pass
                print('数据的数下',value.__fields__)
                # 使用视图模型
                print('类的map',value.__class__,)
                # 获取模型的属性和title
                fields_dict = {i:field.title for i,field in value.__class__.__fields__.items()}
                print('map22',fields_dict)
                logger.debug( f"数据的栏位", value.__fields__,value.__class__, fields_dict)

                changeitems= value.__dict__
                needdel= []
                cndict=dict()
                for ka,va in changeitems.items():

                    for k,v in fields_dict.items():
                        if k==ka  and  v:
                            cndict[v] = va
                            needdel.append(ka)
                            # del changeitems[ka]
                    pass

                # changeitems= {**changeitems,**cndict}
                for i in needdel:
                    del changeitems[i]
                changeitems= { **cndict}
                data.append(changeitems)
                logger.debug( f"解析到的预览数据",changeitems)

                print(data)
            return {"data":data}

        except Exception as e:
            traceback.print_exc()
            print('解析文件报错  ',e,e.__traceback__)
            logger.debug( f"发生异常", traceback.format_exception(e))

        return data
    async def get_download_url(self, id: str):
        return await self.system_rule.get_download_url_by_id(id)

