
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.views import BaseView
from starlette.requests import Request
from mini_framework.web.request_context import request_context_manager
from rules.teachers_info_rule import TeachersInfoRule
from rules.teachers_rule import TeachersRule
from views.common.common_view import get_extend_params
from views.models.system import UnitType
from views.models.teachers import Teachers, TeacherInfo, CurrentTeacherQuery, \
    CurrentTeacherInfoSaveModel, TeacherApprovalQuery
from fastapi import Query, Depends, Body
from mini_framework.utils.json import JsonUtils
from common.decorators import require_role_permission
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO


class TeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)

    @require_role_permission("teacherInfo", "view")
    async def get_teacher(self, teacher_id: int | str = Query(..., title="教师编号", description="教师编号")):
        """
        获取单个教职工信息
        """
        teacher_id = int(teacher_id)
        res = await self.teacher_rule.get_teachers_by_id(teacher_id)
        return res

    # 编辑新教职工登记信息
    @require_role_permission("teacherInfo", "edit")
    async def put_teacher(self, teachers: Teachers):
        user_id = request_context_manager.current().current_login_account.name
        new_fields = await self.teacher_rule.update_teachers(teachers, user_id)
        return new_fields

    @require_role_permission("teacherInfo", "view")
    async def page(self, request: Request, current_teacher=Depends(CurrentTeacherQuery),
                   page_request=Depends(PageRequest)):
        """
        老师分页查询
        """
        ob = await get_extend_params(request)
        paging_result = await self.teacher_info_rule.query_current_teacher_with_page(current_teacher, page_request, ob)
        return paging_result

    @require_role_permission("teacherKeyInfo", "view")
    async def page_teacher_info_change_launch(self, request: Request,
                                              teacher_approval_query=Depends(TeacherApprovalQuery),
                                              page_request=Depends(PageRequest)):
        """
        分页查询
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                #如果是事业单位，则就是自己查询自己事业单位的信息
                if school.institution_category == "institution":
                    teacher_approval_query.teacher_employer = tenant.origin_id
                # 如果是行政单位，则查询行政单位下的所有学校的信息
                elif school.institution_category == "institution":
                    extend_param["borough"] = school.borough
                else:
                    teacher_approval_query.teacher_employer = tenant.origin_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            extend_param["borough"] = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = 'launch'
        paging_result = await self.teacher_rule.query_teacher_info_change_approval(type, teacher_approval_query,
                                                                                   page_request, extend_param)
        return paging_result

    @require_role_permission("teacherKeyInfo", "view")
    async def page_teacher_info_change_approval(self, request: Request,
                                                teacher_approval_query=Depends(TeacherApprovalQuery),
                                                page_request=Depends(PageRequest)):
        """
        分页查询
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                #如果是事业单位，则就是自己查询自己事业单位的信息
                if school.institution_category == "institution":
                    teacher_approval_query.teacher_employer = tenant.origin_id
                # 如果是行政单位，则查询行政单位下的所有学校的信息
                elif school.institution_category == "institution":
                    extend_param["borough"] = school.borough
                else:
                    teacher_approval_query.teacher_employer = tenant.origin_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            extend_param["borough"] = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = 'approval'
        paging_result = await self.teacher_rule.query_teacher_info_change_approval(type, teacher_approval_query,

                                                                                   page_request, extend_param)
        return paging_result

    # 获取教职工基本信息
    @require_role_permission("teacherInfo", "view")
    async def get_teacherinfo(self, teacher_id: int | str = Query(..., title="姓名", description="教师名称",
                                                                  example=123)):
        teacher_id = int(teacher_id)
        res = await self.teacher_info_rule.get_teachers_info_by_teacher_id(teacher_id)
        return res

    # 编辑教职工基本信息
    @require_role_permission("teacherInfo", "edit")
    async def put_teacherinfosave(self, teacher_info: CurrentTeacherInfoSaveModel):
        """
        保存不经过验证
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_info_rule.update_teachers_info_save(teacher_info, user_id)
        return res

    @require_role_permission("teacherInfo", "edit")
    async def put_teacherinfo(self, teacher_info: TeacherInfo):
        """
        提交教职工基本信息
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_info_rule.update_teachers_info(teacher_info, user_id)
        return res

    # 删除教职工基本信息
    @require_role_permission("teacherInfo", "delete")
    async def delete_teacherinfo(self,
                                 teacher_id: int | str = Query(..., title="姓名", description="教师名称",
                                                               example=123)):
        teacher_id = int(teacher_id)
        await self.teacher_info_rule.delete_teachers_info(teacher_id)
        return str(teacher_id)

    @require_role_permission("teacherKeyInfo", "approval")
    async def patch_teacher_info_change_approved(self,
                                                 teacher_id: int | str = Body(..., title="教师编号",
                                                                              description="教师编号",
                                                                              example=123),
                                                 process_instance_id: int | str = Body(..., title="流程实例id",
                                                                                       description="流程实例id",
                                                                                       example=123),
                                                 reason: str = Body(None, title="审批意见", description="审批意见",
                                                                    example="同意")):
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        user_id = request_context_manager.current().current_login_account.name
        reason = reason

        return await self.teacher_rule.teacher_info_change_approved(teacher_id, process_instance_id, user_id, reason)

    @require_role_permission("teacherKeyInfo", "reject")
    async def patch_teacher_info_change_rejected(self,
                                                 teacher_id: int | str = Body(..., title="教师编号",
                                                                              description="教师编号",
                                                                              example=123),
                                                 process_instance_id: int | str = Body(..., title="流程实例id",
                                                                                       description="流程实例id",
                                                                                       example=123),
                                                 reason: str = Body("", title="reason",
                                                                    description="审核理由")):
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        return await self.teacher_rule.teacher_info_change_rejected(teacher_id, process_instance_id, user_id, reason)

    @require_role_permission("teacherKeyInfo", "revoke")
    async def patch_teacher_info_change_revoked(self,
                                                teacher_id: int | str = Body(..., title="教师编号",
                                                                             description="教师编号",
                                                                             example=123),
                                                process_instance_id: int | str = Body(..., title="流程实例id",
                                                                                      description="流程实例id",
                                                                                      example=123),
                                                ):
        user_id = request_context_manager.current().current_login_account.name
        await self.teacher_rule.teacher_info_change_revoked(teacher_id, process_instance_id, user_id)
        return teacher_id
