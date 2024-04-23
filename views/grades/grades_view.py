from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.grades import Grades

from fastapi import Query, Depends, Body
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
                  # school_id: int = Query(None, title="学校ID", description="学校ID"  ),
                  # grade_no: str = Query(None, description="年级编号", min_length=1, max_length=20, example=''),
                  grade_id: int = Query(None, title="", description="年级ID"),
                  ):
        account = await self.grade_rule.get_grade_by_id(grade_id)

        return account

    async def post(self, grades: Grades):
        print(grades)
        res = await self.grade_rule.add_grade(grades)
        return res

    async def page(self,
                   page_request=Depends(PageRequest),
                   school_id: int = Query(None, title="学校ID", description="学校ID"),
                   grade_name: str = Query(None, description="年级名称", min_length=1, max_length=20)
                   ):
        print(page_request)
        paging_result = await self.grade_rule.query_grade_with_page(page_request, grade_name, school_id)

        items = []
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

    #   搜索的 待处理
    async def query(self, grade_name: str = Query(..., description="年级名称", min_length=1, max_length=20)):
        lst = await self.grade_rule.query_grade(grade_name)

        return lst

    # 删除
    async def delete(self, grade_id: int = Query(..., title="", description="年级id", example='1'), ):
        print(grade_id)
        # return  grade_id
        res = await self.grade_rule.delete_grade(grade_id)

        return res

    # 修改 关键信息
    async def put(self,
                  grades: Grades,
                  grade_id: int = Query(..., title="", description="年级id", example='1'),

                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        grades.id = grade_id
        res = await self.grade_rule.update_grade(grades)

        return res
