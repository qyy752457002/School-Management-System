from views.models.teachers import  NewTeacher, TeacherInfo
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from sqlalchemy import select
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from rules.teachers_rule import TeachersRule
from views.models.teachers import Teachers, TeacherInfo
from rules.teachers_info_rule import TeachersInfoRule


class TeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)

    # 分页查询
    async def page(self,  page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = NewTeacher(
            name="张三",
            id_number="123456789",
            gender="男",
            employer="xx学校",
            highest_education="本科",
            political_status="党员",
            in_post="是",
            employment_form="合同",
            enter_school_time="2021-10-10",
            approval_status="通过"
        )

        for i in range(0, page_request.per_page):
            items.append(res)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
                                 per_page=page_request.per_page, total=100, items=items)

    # 在职教职工信息
    # 获取教职工基本信息
    async def get_teacherinfo(self, id: str = Query(None, title="教师名称", description="教师名称", min_length=1,
                                                       max_length=20,
                                                       example='张三')):
        res = await self.teacher_info_rule.get_teachers_info_by_id(id)
        return res


    # 编辑教职工基本信息
    async def put_teacherinfo(self, teacherinfo: TeacherInfo):
        print(teacherinfo)
        res = await self.teacher_info_rule.add_teachers_info(teacherinfo)
        return res

    # 删除教职工基本信息
    async def delete_teacherinfo(self, id: str = Query(None, title="教师名称", description="教师名称", min_length=1,
                                                       max_length=20,
                                                       example='张三')):
        res = await self.teacher_info_rule.delete_teachers_info(id)
        return res


