from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.grades import Grades

from fastapi import Query, Depends,Body
from sqlalchemy import select
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.grade import Grade
from rules.grade_rule import GradeRule
from views.models.grades import Grades

class GradesView(BaseView):
    def __init__(self):
        super().__init__()
        self.grade_rule = get_injector(GradeRule)

    async def get(self,
                  school_id: str = Query(None, title="学校ID", description="学校ID", min_length=1, max_length=20,
                                         example='SC2032633'),
                  grade_no: str = Query(None, description="年级编号", min_length=1, max_length=20, example=''),
                  grade_id: str = Query(None, title="", description="年级ID", min_length=1, max_length=20,
                                         example='SC2032633'),
                  ):
        account = await self.grade_rule.get_grade_by_id(grade_id)

        res = Grades(
            school_id=school_id,
            grade_no=grade_no,
            grade_name="A school management system",
            grade_alias="Lfun technical",
        )
        return account

    async def post(self, grades: Grades):
        print(grades)
        return grades




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(Grades(
                school_id="SC2032633",
                grade_no="SC2032633",
                grade_name="A school management system",
                grade_alias="Lfun technical",
            ))




        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
