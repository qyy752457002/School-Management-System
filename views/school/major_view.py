from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.majors import Majors
from views.models.grades import Grades

from fastapi import Query, Depends


class MajorView(BaseView):

    async def post(self, major: Majors):
        print(major)
        return major




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(Majors( school_id='SC2032633',major_name='XXX',major_id='123',major_type='XXX',major_id_lv2='123',major_id_lv3='123',))




        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, major_id:str= Query(..., title="", description="专业id",min_length=1,max_length=20,example='SC2032633'),):
        print(major_id)
        return  major_id

    # 修改 关键信息
    async def put(self,major:Majors
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return  major