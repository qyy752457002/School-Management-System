from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from views.models.campus import Campus, CampusBaseInfo,CampusKeyInfo
# from fastapi import Field

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from rules.campus_rule import CampusRule
from views.models.campus_communications import CampusCommunications
from rules.campus_communication_rule import CampusCommunicationRule


class CampusView(BaseView):
    def __init__(self):
        super().__init__()
        self.campus_rule = get_injector( CampusRule)
        self.campus_communication_rule = get_injector( CampusCommunicationRule)



    async def get(self,
                  campus_id: int = Query(..., description="校区id", example='1'),

                  ):
        res =await self.campus_rule.get_campus_by_id(campus_id)
        return  res

    async def post(self,campus:Campus):
        print(campus)
        res =await  self.campus_rule.add_campus(campus)

        return  res

    # 修改 关键信息
    async def put(self,
                  campus_keyinfo:CampusKeyInfo
                  ):
        # print(campus)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.campus_rule.update_campus(campus_keyinfo)

        return  res
    # 删除
    async def delete(self, campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1'),):
        print(campus_id)
        res = await self.campus_rule.softdelete_campus(campus_id)

        return  res
    # 修改 变更 基本信息
    async def patch_baseinfo(self, campus_baseinfo:CampusBaseInfo
                               ):
        # print(campus)
        res = await self.campus_rule.update_campus(campus_baseinfo,2)
        return   res




    async def page(self,
                   page_request= Depends(PageRequest),
                   campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),

                   ):
        print(page_request)
        items=[]
        res = await self.campus_rule.query_campus_with_page(page_request , campus_name,None,campus_no,)
        return res




    # 开办
    async def patch_open(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1')):
        # print(campus)
        res = await self.campus_rule.update_campus_status(campus_id , 1)

        return  res

    # 关闭
    async def patch_close(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1')):
        # print(campus)
        res = await self.campus_rule.update_campus_status(campus_id , 2)

        return  res

    # 导入 todo 任务队列的
    async def importing(self,campus:Campus):
        print(campus)
        return  campus
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
    # 新增 通信信息
    async def post_comminfo(self,
                            campus: CampusCommunications,

                            ):

        res = await self.campus_communication_rule.add_campus_communication(campus)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res
