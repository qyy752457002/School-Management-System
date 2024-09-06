# from fastapi import Field
from fastapi import Query, Depends, Body
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.views import BaseView

from rules.graduation_student_rule import GraduationStudentRule
from views.models.student_graduate import GraduateStudentQueryModel, CountySchoolArchiveQueryModel
from views.models.students import StudentGraduation


class GraduationStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.graduation_student_rule = get_injector(GraduationStudentRule)

    # 分页查询
    async def page(self, query_model: GraduateStudentQueryModel,
                   page_request=Depends(PageRequest)):
        res = await self.graduation_student_rule.query_graduation_student_by_model_with_page(page_request, query_model)
        return res

    # 发起毕业
    async def get_graduation_student_by_school_id(self, school_id: int | str = Query(..., title="教师编号",
                                                                                     description="教师编号")):
        res = await self.graduation_student_rule.update_graduation_student_by_school_id(school_id)
        return res

    async def post_student_graduate_status_by_student_id(self, student_id: int | str = Body(..., title="学生编号",
                                                                                            description="学生编号"),
                                                         status: str = Body(..., title="毕业状态",
                                                                            description="毕业状态")):
        res = await self.graduation_student_rule.update_graduation_student_status(student_id, status)
        return res

    async def post_student_graduate_archive_status_by_school_id(self, school_id: int | str = Body(..., title="学校编号",
                                                                                                  description="学校编号")):
        res = await self.graduation_student_rule.update_archive_status_and_year_by_student_id(school_id)
        return res

    async def page_school_archive_status(self, query_model: CountySchoolArchiveQueryModel,
                                         page_request=Depends(PageRequest)):
        res = await self.graduation_student_rule.query_school_archive_status_with_page(page_request, query_model)
        return res

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
        res = await self.graduation_student_rule.update_graduation_student(student.student_id, None, None,
                                                                           student.graduation_photo,
                                                                           student.credential_notes)

        # res = await self.graduation_student_rule.update_graduation_student(graduation_student)

        return res
