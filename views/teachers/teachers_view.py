from views.models.teachers import NewTeacher, TeacherInfo
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from sqlalchemy import select
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from rules.teachers_rule import TeachersRule
from rules.teachers_info_rule import TeachersInfoRule
from views.models.teachers import Teachers, TeacherInfo,TeachersCreatModel,TeacherInfoCreateModel


class TeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)

    async def get_teacher(self, teacher_id: int = Query(..., title="教师编号", description="教师编号")):
        """
        获取单个教职工信息
        """
        res = await self.teacher_rule.get_teachers_by_id(teacher_id)
        return res

    # 编辑新教职工登记信息
    async def put_teacher(self, teachers: Teachers):
        print(teachers)
        res = await self.teacher_rule.update_teachers(teachers)
        return res

    async def page(self, new_teacher = Depends(NewTeacher), page_request=Depends(PageRequest)):
        """
        老师分页查询
        """
        paging_result = await self.teacher_info_rule.query_teacher_with_page(new_teacher,page_request)
        return paging_result


    # 获取教职工基本信息
    async def get_newteacherinfo(self, teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                       example=123)):
        res = await self.teacher_info_rule.get_teachers_info_by_id(teacher_id)
        return res

    # 编辑教职工基本信息
    async def put_newteacherinfo(self, teacher_info: TeacherInfoCreateModel):
        res = await self.teacher_info_rule.update_teachers_info(teacher_info)
        return res

    # 删除教职工基本信息
    async def delete_teacherinfo(self,
                                 teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                         example=123)):
        await self.teacher_info_rule.delete_teachers_info(teacher_id)
        return str(teacher_id)


    async def patch_submitting(self,
                               teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.submitting(teacher_id)
        return teacher_id

    async def patch_submitted(self,
                              teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.submitted(teacher_id)
        return teacher_id

    async def patch_approved(self,
                             teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.approved(teacher_id)
        return teacher_id

    async def patch_rejected(self,
                             teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.rejected(teacher_id)
        return teacher_id

