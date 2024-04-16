from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.grades import Grades
from views.models.graduation_year import GraduationYear

from fastapi import Query, Depends


class GraduationYearView(BaseView):

    async def post(self, graduationyear: GraduationYear):
        print(graduationyear)
        return graduationyear

    async def put(self, graduationyear: GraduationYear ,graduationyear_id:str = Query(...,   description="届别id",min_length=1,max_length=20,example='SC2032633'), ):
        print(graduationyear)
        return graduationyear





    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(GraduationYear(graduation_year='2003',description='届别描述',status='已开启'))




        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
