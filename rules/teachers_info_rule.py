from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from views.common.common_view import page_none_deal
from views.models.teachers import TeacherInfo as TeachersInfoModel
from views.models.teachers import NewTeacher, NewTeacherRe, TeacherInfoSaveModel, TeacherInfoSubmit, \
    CurrentTeacherQuery, CurrentTeacherQueryRe, CurrentTeacherInfoSaveModel, NewTeacherInfoSaveModel, \
    TeacherInfoCreateModel, TeacherApprovalQuery, TeacherApprovalQueryRe
from sqlalchemy import select, func, update
from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError, TeacherInfoExitError
from daos.teachers_dao import TeachersDao
from views.models.organization import OrganizationMembers
from rules.organization_memebers_rule import OrganizationMembersRule


@dataclass_inject
class TeachersInfoRule(object):
    teachers_info_dao: TeachersInfoDao
    teachers_dao: TeachersDao
    organization_members_rule: OrganizationMembersRule

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

    async def add_teachers_info(self, teachers_info: TeacherInfoSaveModel):
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
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

    async def update_teachers_info(self, teachers_info):
        print(teachers_info.teacher_id)
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

    async def query_teacher_with_page(self, query_model: NewTeacher, page_request: PageRequest):
        print(query_model)
        paging = await self.teachers_info_dao.query_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, NewTeacherRe)
        return paging_result

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
