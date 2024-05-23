from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.graduation_student_rule import GraduationStudentRule
from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo, StudentGraduation
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date
from views.models.students import GraduationStudents


class GraduationStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.graduation_student_rule = get_injector(GraduationStudentRule)

    #
    # async def post(self, graduation_student: GraduationStudents):
    #     print(graduation_student)
    #     res =await self.graduation_student_rule.add_graduation_student(graduation_student)
    #
    #     return res

    # 分页查询
    async def page(self, student_name: str = Query(None, title="学生姓名", description="学生姓名", example=""),
                   school_id: str = Query(None, title="", description="学校", example=""),
                   student_gender: str = Query(None, title="性别", description="性别", example="Male"),
                   edu_number: str = Query(None, title="", description="学籍号码", example=""),
                   class_id: str = Query(None, title="", description="班级", example=""),
                   borough: str = Query('', title="", description="行政属地", example=""),
                   page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = await self.graduation_student_rule.query_graduation_student_with_page(page_request, student_name,
                                                                                    school_id, student_gender,
                                                                                    edu_number, class_id,borough)
        return res

        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
        #                          per_page=page_request.per_page, total=100, items=items)

    #
    #     # 删除
    # async def delete(self, graduation_student_id:int= Query(..., title="", description="毕业生id", example='1'),):
    #     # print(graduation_student_id)
    #     # return  graduation_student_id
    #     res = await self.graduation_student_rule.softdelete_graduation_student(graduation_student_id)
    #
    #     return  res
    #
    # # 修改 关键信息
    # async def put(self,graduation_student:GraduationStudents
    #               ):
    #     # print(planning_school)
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #     res = await self.graduation_student_rule.update_graduation_student(graduation_student)
    #
    #
    #     return  res

    # 毕业 制证  毕业证url  备注
    async def patch_graduation_credential(self,
                                          student: StudentGraduation,
                                       # student_id: int = Query(..., description="学生ID",
                                       #                         example='1'),
                                       # graduation_photo: str = Query(..., description="毕业照", min_length=1,
                                       #                               max_length=200,
                                       #                               example=''),
                                       # credential_notes: str = Query('', description="备注", min_length=1,
                                       #                               max_length=250,
                                       #                               example=''),
                                       ):
        # print(graduation_photo, credential_notes)
        res = await self.graduation_student_rule.update_graduation_student(student.student_id, None, None, student.graduation_photo,
                                                                           student.credential_notes)

        # res = await self.graduation_student_rule.update_graduation_student(graduation_student)

        return res
