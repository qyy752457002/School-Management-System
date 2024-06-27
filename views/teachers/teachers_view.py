from views.models.teachers import NewTeacher, TeacherInfo, RetireTeacherQuery
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
    CurrentTeacherInfoSaveModel,TeacherApprovalQuery


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

        user_id = "asdfasdf"
        new_fields = await self.teacher_rule.update_teachers(teachers, user_id)
        return new_fields

    async def page(self, current_teacher=Depends(CurrentTeacherQuery), page_request=Depends(PageRequest)):
        """
        老师分页查询
        """
        paging_result = await self.teacher_info_rule.query_current_teacher_with_page(current_teacher, page_request)
        return paging_result

    async def page_teacher_info_change_launch(self, teacher_approval_query=Depends(TeacherApprovalQuery),
                                      page_request=Depends(PageRequest)):
        """
        分页查询
        """
        type = 'launch'
        user_id = "asdfasdf"
        paging_result = await self.teacher_rule.query_teacher_info_change_approval(type, teacher_approval_query,
                                                                                 page_request, user_id)
        return paging_result

    async def page_teacher_info_change_approval(self, teacher_approval_query=Depends(TeacherApprovalQuery),
                                        page_request=Depends(PageRequest)):
        """
        分页查询
        """
        type = 'approval'
        user_id = "asdfasdf"
        paging_result = await self.teacher_rule.query_teacher_info_change_approval(type, teacher_approval_query,

                                                                                 page_request, user_id)
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
        res = await self.teacher_info_rule.update_teachers_info_save(teacher_info)
        return res

    async def put_teacherinfo(self, teacher_info: TeacherInfo):
        """
        提交教职工基本信息
        """
        user_id = "asdfasdf"
        res = await self.teacher_info_rule.update_teachers_info(teacher_info, user_id)
        return res

    # 删除教职工基本信息
    async def delete_teacherinfo(self,
                                 teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                         example=123)):
        await self.teacher_info_rule.delete_teachers_info(teacher_id)
        return str(teacher_id)

    async def patch_teacher_info_change_approved(self,
                                                 teacher_id: int = Query(..., title="教师编号", description="教师编号",
                                                                         example=123),
                                                 process_instance_id: int = Query(..., title="流程实例id",
                                                                                  description="流程实例id",
                                                                                  example=123),
                                                 reason: str = Query(None, title="审批意见", description="审批意见",
                                                                     example="同意")):
        user_id = "asdfasdf"
        reason = reason
        await self.teacher_rule.teacher_info_change_approved(teacher_id, process_instance_id, user_id, reason)
        return teacher_id

    async def patch_teacher_info_change_rejected(self,
                                                 teacher_id: int = Query(..., title="教师编号", description="教师编号",
                                                                         example=123),
                                                 process_instance_id: int = Query(..., title="流程实例id",
                                                                                  description="流程实例id",
                                                                                  example=123),
                                                 reason: str = Query("", title="reason",
                                                                     description="审核理由")):
        user_id = "asdfasdf"
        reason = reason
        await self.teacher_rule.teacher_info_change_rejected(teacher_id, process_instance_id, user_id, reason)
        return teacher_id

    async def patch_teacher_info_change_revoked(self,
                                                teacher_id: int = Query(..., title="教师编号", description="教师编号",
                                                                        example=123),
                                                process_instance_id: int = Query(..., title="流程实例id",
                                                                                 description="流程实例id",
                                                                                 example=123),
                                                ):
        user_id = "asdfasdf"
        await self.teacher_rule.teacher_info_change_revoked(teacher_id, process_instance_id, user_id)
        return teacher_id

    # 离退休接口-使用 异动的接口 这里不使用
    # async def patch_teacher_retire(self,
    #                                teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123),
    #                                act: str = Query(..., title="", description="", example='离休'),
    #
    #                                ):
    #     await self.teacher_rule.teacher_active(teacher_id)
    #     return teacher_id
    async def page_teacher_retire(self, current_teacher=Depends(RetireTeacherQuery), page_request=Depends(PageRequest)):
        """
        退休老师分页查询
        """
        paging_result = await self.teacher_info_rule.query_retire_teacher_with_page(current_teacher, page_request)
        return paging_result
