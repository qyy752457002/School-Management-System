from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.major_rule import MajorRule
from views.models.majors import Majors
from views.models.grades import Grades

from fastapi import Query, Depends, Body


class MajorView(BaseView):
    def __init__(self):
        super().__init__()
        self.major_rule = get_injector(MajorRule)

    async def post(self,
                   school_id: int = Query(..., description="学校ID", example='1'),
                   major_list: List[Majors] = Body([], description="选择的专业", example=[
                       {  "major_name": "语文", "major_no": "19",  }]),

                   # major: Majors
                   ):
        # print(major)
        res = await self.major_rule.add_major_multi(school_id,major_list)

        return res

    async def page(self,
                   page_request=Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),
                   school_id: int = Query(0, description="学校ID", example='1'),

                   ):
        print(page_request)
        items = []
        res = await self.major_rule.query_major_with_page_param(page_request, school_id)
        return res

        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, major_id: int = Query(..., title="", description="专业id", )):
        print(major_id)
        res = await self.major_rule.softdelete_major(major_id)

        return res

    # 修改 关键信息
    async def put(self,
                  school_id: int = Query(..., description="学校ID", example='1'),
                  major_list: List[Majors] = Body([], description="选择的专业", example=[
                      {  "major_name": "语文", "major_no": "19","school_id":1 ,  "major_type": "19","major_id_lv2": "19","major_id_lv3": "19", }]),

                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.major_rule.softdelete_major_by_school_id(school_id)

        res = await self.major_rule.add_major_multi(school_id,major_list)


        return res
    #
    # # 获取所有的课程列表 给下拉
    # async def get_all(self):
    #     # print(page_request)
    #     items = []
    #
    #     res = await self.major_rule.get_major_all({'school_id': 0})
    #     return res
