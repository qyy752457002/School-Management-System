from fastapi.params import Query
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.storage_rule import StorageRule


class StorageView(BaseView):
    def __init__(self):
        super().__init__()
        self._storage_rule: StorageRule = get_injector(StorageRule)

    async def get_school_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_school_info_token_uri(filename, file_size)

    async def get_student_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_student_info_token_uri(filename, file_size)

    async def get_teacher_upload_uri(self, filename: str, file_size: int):
        return await self._storage_rule.get_upload_teacher_info_token_uri(filename, file_size)

#     解析 文件和桶  返回 数据结构
    async def get_file_data_preview(self, filename: str, bucket,sence=''):
        res = await self._storage_rule.get_file_data(filename, bucket,sence)
        print('解析的结构',res )
        # 存在ID的tuple 过滤掉
        data = [ ]
        for i,value  in  enumerate(res):
            if isinstance(value.id, (Query,tuple)):
                value.id = 0
                # value.model_fields['id'] = 0
                pass

            changeitems = dict()
            # 使用视图模型
            for key, v in value.model_fields:
                # changeitems.append(key)
                key_cn = v.model_fields[key].title
                changeitems[key_cn] = value.key
            data.append(changeitems)




        print(data)
        return {"data":data}


