from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.leader_info_rule import LeaderInfoRule
from views.models.leader_info import LeaderInfo
from views.models.grades import Grades

from fastapi import Query, Depends


class LeaderInfoView(BaseView):
    def __init__(self):
        super().__init__()
        self.leader_info_rule = get_injector( LeaderInfoRule)

    async def post(self, leader_info: LeaderInfo):
        print(leader_info)
        res =await self.leader_info_rule.add_leader_info(leader_info)

        return res




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        res = await self.leader_info_rule.query_leader_info_with_page(page_request , )
        return res


        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, leader_info_id:int= Query(..., title="", description="专业id", )):
        print(leader_info_id)
        res = await self.leader_info_rule.softdelete_leader_info(leader_info_id)

        return  res

    # 修改 关键信息
    async def put(self,leader_info:LeaderInfo
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.leader_info_rule.update_leader_info(leader_info)


        return  res