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
from views.models.teachers import Teachers, TeacherInfo, CurrentTeacherQueryRe, CurrentTeacherQuery, \
    CurrentTeacherInfoSaveModel


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
        teacher_id = teachers.teacher_id
        old_fields = await self.teacher_rule.get_teachers_by_id(teacher_id)

        res = await self.teacher_rule.update_teachers(teachers)
        return res

    async def page(self, current_teacher=Depends(CurrentTeacherQuery), page_request=Depends(PageRequest)):
        """
        老师分页查询
        """
        paging_result = await self.teacher_info_rule.query_current_teacher_with_page(current_teacher, page_request)
        return paging_result

    # 获取教职工基本信息
    async def get_teacherinfo(self, teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                            example=123)):
        res = await self.teacher_info_rule.get_teachers_info_by_teacher_id(teacher_id)
        return res

    # 编辑教职工基本信息
    async def put_teacherinfosave(self, teacher_info: CurrentTeacherInfoSaveModel):
        """
        保存不经过验证
        """
        res = await self.teacher_info_rule.update_teachers_info(teacher_info)
        return res

    async def put_teacherinfo(self, teacher_info: TeacherInfo):
        """
        提交教职工基本信息
        """
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

    async def patch_revoked(self, teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
        await self.teacher_rule.revoked(teacher_id)
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

    async def patch_info_submitting(self,
                                    teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                                 description="教师基本信息编号",
                                                                 example=123)):
        await self.teacher_info_rule.submitting(teacher_base_id)
        return teacher_base_id

    async def patch_info_submitted(self,
                                   teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                                description="教师基本信息编号",
                                                                example=123)):
        await self.teacher_info_rule.submitted(teacher_base_id)
        return teacher_base_id

    async def patch_info_approved(self,
                                  teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                               description="教师基本信息编号",
                                                               example=123)):
        await self.teacher_info_rule.approved(teacher_base_id)
        return teacher_base_id

    async def patch_info_rejected(self,
                                  teacher_base_id: int = Query(..., title="教师基本信息编号",
                                                               description="教师基本信息编号",
                                                               example=123)):
        await self.teacher_info_rule.rejected(teacher_base_id)
        return teacher_base_id

    async def patch_teacher_active(self,
                                   teacher_id: int = Query(..., title="教师编号", description="教师编号",
                                                           example=123), ):
        await self.teacher_rule.teacher_active(teacher_id)
        return teacher_id
