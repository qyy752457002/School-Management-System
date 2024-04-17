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
                  school_id: int = Query(None, title="学校ID", description="学校ID"  ),
                  grade_no: str = Query(None, description="年级编号", min_length=1, max_length=20, example=''),
                  grade_id: int = Query(None, title="", description="年级ID"),
                  ):
        account = await self.grade_rule.get_grade_by_id(grade_id)

        return account

    async def post(self, grades: Grades):
        print(grades)
        res = await self.grade_rule.add_grade(grades)
        return res




    async def page(self,
                   page_request= Depends(PageRequest),
                   school_id: int = Query(None, title="学校ID", description="学校ID"  ),
                   ):
        print(page_request)
        paging_result = await self.grade_rule.query_grade_with_page( page_request,None,school_id)


        items=[]
        # for i in range(page_request.per_page):
        #     items.append(Grades(
        #         school_id="SC2032633",
        #         grade_no="SC2032633",
        #         grade_name="A school management system",
        #         grade_alias="Lfun technical",
        #     ))
        #
        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
        return paging_result


    # todo 搜索的 待处理  
    async def query(self, grade_name: str = Query(..., description="年级名称", min_length=1, max_length=20)):
        from mini_framework.databases.conn_managers.db_manager import db_connection_manager
        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(Grade))

        lst = []
        for row in result:
            account = Grades(school_id=row.school_id,
                             grade_no=row.grade_no,
                             grade_name=row.grade_name,
                             grade_alias=row.grade_alias,
                             description=row.description)
            lst.append(account)
        return lst