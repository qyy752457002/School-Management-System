from typing import List

from mini_framework.web.views import BaseView

from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date
from views.models.students import GraduationStudents


class GraduationStudentsView(BaseView):

    # 分页查询
    async def page(self, student_name: str = Query(None, title="学生姓名", description="学生姓名", example="John Doe"),
                   school_id: str = Query(None, title="", description="学校", example="John Doe"),
                   gender: str = Query(None, title="性别", description="性别", example="Male"),
                   edu_number: str = Query(None, title="", description="学籍号码", example="ID Card"),
                   class_id: str = Query(None, title="", description="班级", example=""),

                   page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = GraduationStudents(student_name='xxx', gender='1', school='xxx', edu_number='fsdfsd', class_id='12', county='行政属地')

        for i in range(0, page_request.per_page):
            items.append(res)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
                                 per_page=page_request.per_page, total=100, items=items)
