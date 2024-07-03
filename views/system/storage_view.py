from fastapi.params import Query
from mini_framework.design_patterns.depend_inject import get_injector
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
    async def get_file_data_preview(self, filename: str, bucket,sence=''):
        data = dict()

        try:
            print('解析的文件',filename,bucket)
            res = await self._storage_rule.get_file_data(filename, bucket,sence)
            print('解析的结构',res )
            # 存在ID的tuple 过滤掉
            data = [ ]
            for i,value  in  enumerate(res):
                if isinstance(value.id, (Query,tuple)):
                    value.id = 0
                    pass
                print('数据的数下',value.__fields__)
                # 使用视图模型
                print('类的map',value.__class__,)
                # 获取模型的属性和title
                fields_dict = {i:field.title for i,field in value.__class__.__fields__.items()}
                print('map22',fields_dict)
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
                print(data)
            return {"data":data}

        except Exception as e:
            print('解析文件报错',e)

        return data
    async def get_download_url(self, id: str):
        return await self.system_rule.get_download_url_by_id(id)

