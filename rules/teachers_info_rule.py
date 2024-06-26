from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from views.common.common_view import page_none_deal
from views.models.teachers import TeacherInfo as TeachersInfoModel
from views.models.teachers import NewTeacher, NewTeacherRe, TeacherInfoSaveModel, TeacherInfoSubmit, \
    CurrentTeacherQuery, CurrentTeacherQueryRe, CurrentTeacherInfoSaveModel, NewTeacherInfoSaveModel, \
    TeacherInfoCreateModel, TeacherApprovalQuery, TeacherApprovalQueryRe, NewTeacherApprovalCreate
from sqlalchemy import select, func, update
from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError, TeacherInfoExitError
from daos.teachers_dao import TeachersDao
from views.models.organization import OrganizationMembers
from rules.organization_memebers_rule import OrganizationMembersRule
from models.teacher_key_info_approval import TeacherKeyInfoApproval
from models.teacher_entry_approval import TeacherEntryApproval
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from daos.teacher_entry_dao import TeacherEntryApprovalDao
from models.teacher_change_log import TeacherChangeLog
from daos.teacher_change_dao import TeacherChangeLogDAO
from models.teacher_approval_log import TeacherApprovalLog
from daos.teacher_approval_log_dao import TeacherApprovalLogDao
from rules.teacher_change_rule import TeacherChangeRule
from daos.teacher_key_info_approval_dao import TeacherKeyInfoApprovalDao
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from datetime import datetime


@dataclass_inject
class TeachersInfoRule(object):
    teachers_info_dao: TeachersInfoDao
    teachers_dao: TeachersDao
    organization_members_rule: OrganizationMembersRule
    teacher_work_flow_rule: TeacherWorkFlowRule
    teacher_change_log: TeacherChangeLogDAO
    teacher_approval_log: TeacherApprovalLogDao
    teacher_change_detail: TeacherChangeRule
    teacher_key_info_approval_dao: TeacherKeyInfoApprovalDao
    teacher_work_flow_rule: TeacherWorkFlowRule

    # 查询单个教职工基本信息
    async def get_teachers_info_by_teacher_id(self, teachers_id):
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_id)
        if not teachers_info_db:
            raise TeacherInfoNotFoundError()
        teachers_info = orm_model_to_view_model(teachers_info_db, NewTeacherInfoSaveModel, exclude=[""])
        return teachers_info

    async def get_teachers_info_by_teacher_id_exit(self, teachers_id):
        exits = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_id)
        return exits

    async def get_teachers_info_by_id(self, teachers_base_id):
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info_db:
            raise TeacherInfoNotFoundError()
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def add_teachers_info(self, teachers_info: TeacherInfoSaveModel, user_id):
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                         exclude=[""])
        params = {"process_code": "t_entry", "applicant_name": user_id}
        await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
        organization = OrganizationMembers()
        organization.id = None
        organization.org_id = teachers_info.org_id
        organization.teacher_id = teachers_info.teacher_id
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.add_organization_members(organization)
        return teachers_info

    async def add_teachers_info_import(self, teachers_info: TeacherInfoCreateModel):
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo)
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def add_teachers_info_valid(self, teachers_info: TeacherInfoSubmit):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teachers_info.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        organization = OrganizationMembers()
        organization.id = None
        organization.org_id = teachers_info.org_id
        organization.teacher_id = teachers_info.teacher_id
        organization.member_type = None
        organization.identity = None
        if teachers_info.org_id:
            await self.organization_members_rule.add_organization_members(organization)
        return teachers_info

    async def update_teachers_info(self, teachers_info, user_id):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teachers_info.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_base_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        need_update_list = []
        for key, value in teachers_info.dict().items():
            if value:
                need_update_list.append(key)
        teachers_info = await self.teachers_info_dao.update_teachers_info(teachers_info, *need_update_list)

        teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)

        teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                         exclude=[""])
        params = {"process_code": "t_entry", "applicant_name": user_id}
        await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)

        organization = OrganizationMembers()
        organization.id = None
        organization.org_id = teachers_info.org_id
        organization.teacher_id = teachers_info.teacher_id
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.update_organization_members_by_teacher_id(organization)
        return teachers_info

    async def update_teachers_info_save(self, teachers_info, user_id):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teachers_info.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_base_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        need_update_list = []
        for key, value in teachers_info.dict().items():
            if value:
                need_update_list.append(key)
        teachers_info = await self.teachers_info_dao.update_teachers_info(teachers_info, *need_update_list)

        teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                         exclude=[""])
        params = {"process_code": "t_entry", "applicant_name": user_id}
        await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
        organization = OrganizationMembers()
        organization.id = None
        organization.org_id = teachers_info.org_id
        organization.teacher_id = teachers_info.teacher_id
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.update_organization_members_by_teacher_id(organization)
        return teachers_info

    # 删除单个教职工基本信息
    async def delete_teachers_info(self, teachers_info_id):
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info_db = await self.teachers_info_dao.delete_teachers_info(exists_teachers_info)
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def query_teacher_with_page(self, query_model: NewTeacher, page_request: PageRequest, user_id):
        params = {"applicant_name": user_id, "process_code": "t_entry", }
        paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                      NewTeacherRe, params)
        return paging

    async def query_current_teacher_with_page(self, query_model: CurrentTeacherQuery, page_request: PageRequest):
        # todo 需要加一个返回一个能否变动的状态
        print(query_model)
        paging = await self.teachers_info_dao.query_current_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, CurrentTeacherQueryRe)
        return paging_result

    async def submitting(self, teachers_base_id):
        teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info.approval_status = "submitting"
        return await self.teachers_info_dao.update_teachers_info(teachers_info, "approval_status")

    async def submitted(self, teachers_base_id):
        teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info.approval_status = "submitted"
        return await self.teachers_info_dao.update_teachers_info(teachers_info, "approval_status")

    async def approved(self, teachers_base_id):
        teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info.approval_status = "approved"
        return await self.teachers_info_dao.update_teachers_info(teachers_info, "approval_status")

    async def rejected(self, teachers_base_id):
        teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info.approval_status = "rejected"
        return await self.teachers_info_dao.update_teachers_info(teachers_info, "approval_status")
