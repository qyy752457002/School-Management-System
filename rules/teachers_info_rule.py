from datetime import datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError, TeacherInfoExitError, QueryError
from daos.operation_record_dao import OperationRecordDAO
from daos.school_dao import SchoolDAO
from daos.teacher_approval_log_dao import TeacherApprovalLogDao
from daos.teacher_change_dao import TeacherChangeLogDAO
from daos.teacher_key_info_approval_dao import TeacherKeyInfoApprovalDao
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from rules.common.common_rule import convert_fields_to_str
from rules.operation_record import OperationRecordRule
from rules.organization_memebers_rule import OrganizationMembersRule
from rules.teacher_change_rule import TeacherChangeRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.teachers_rule import TeachersRule
from views.common.common_view import compare_modify_fields
from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from views.models.organization import OrganizationMembers
from views.models.teachers import NewTeacher, NewTeacherRe, TeacherInfoSaveModel, TeacherInfoSubmit, \
    CurrentTeacherQuery, CurrentTeacherQueryRe, CurrentTeacherInfoSaveModel, NewTeacherInfoSaveModel, \
    TeacherInfoCreateModel, NewTeacherApprovalCreate, TeacherInfoImportSubmit
from views.models.teachers import TeacherInfo as TeachersInfoModel


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
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO
    school_dao: SchoolDAO

    # 查询单个教职工基本信息
    async def get_teachers_info_by_teacher_id(self, teachers_id):
        teachers_id = int(teachers_id)
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_id)
        if not teachers_info_db:
            raise TeacherInfoNotFoundError()
        teachers_info = orm_model_to_view_model(teachers_info_db, NewTeacherInfoSaveModel, exclude=[""])
        return teachers_info

    async def get_teachers_info_by_teacher_id_exit(self, teachers_id):
        teachers_id = int(teachers_id)
        exits = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_id)
        return exits

    async def get_teachers_info_by_id(self, teachers_base_id):
        teachers_base_id = int(teachers_base_id)
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_id(teachers_base_id)
        if not teachers_info_db:
            raise TeacherInfoNotFoundError()
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def add_teachers_info(self, teachers_info: TeacherInfoSaveModel, user_id):
        teachers_info.teacher_id = int(teachers_info.teacher_id)
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo)
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        # teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        # teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
        #                                                  exclude=[""])
        # params = {"process_code": "t_entry", "applicant_name": user_id}
        # await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
        #     teachers_info.teacher_id)
        # await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
        # organization = OrganizationMembers()
        # organization.id = None
        # organization.org_id = teachers_info.org_id
        # organization.teacher_id = teachers_info.teacher_id
        # organization.member_type = None
        # organization.identity = None
        # await self.organization_members_rule.add_organization_members(organization)
        return teachers_info

    async def add_teachers_info_import(self, teachers_info: TeacherInfoCreateModel):
        teachers_info.teacher_id = int(teachers_info.teacher_id)
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo)
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def add_teachers_info_valid(self, teachers_info: TeacherInfoSubmit, user_id):
        teachers_info.teacher_id = int(teachers_info.teacher_id)
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teachers_info.teacher_id)
        teacher_main_status = exits_teacher.teacher_main_status
        if not exits_teacher:
            raise TeacherNotFoundError()
        exits_teacher_base = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers_info.teacher_id)
        if exits_teacher_base:
            raise TeacherInfoExitError()
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)

        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        if teacher_main_status == "unemployed":
            await self.teacher_submitted(teachers_info.teacher_id)
            teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
            if not teacher_entry_approval_db:
                raise QueryError()
            teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                             exclude=[""])
            params = {"process_code": "t_entry", "applicant_name": user_id}
            await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
                teacher_entry_approval.teacher_id)
            work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
            teacher_entry_save_to_submit_log = OperationRecord(  # 这个是转在职的
                action_target_id=teacher_entry_approval.teacher_id,
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.NEW_ENTRY.value,
                change_detail="转在职",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=work_flow_instance["process_instance_id"])
            await self.operation_record_rule.add_operation_record(teacher_entry_save_to_submit_log)
        organization = OrganizationMembers()
        organization.id = SnowflakeIdGenerator(1, 1).generate_id()
        organization.org_id = int(teachers_info.org_id)
        organization.teacher_id = int(teachers_info.teacher_id)
        organization.member_type = None
        organization.identity = None
        if teachers_info.org_id:
            await self.organization_members_rule.add_organization_members(organization)
        return teachers_info

    async def update_teachers_info(self, teachers_info: TeacherInfoSubmit, user_id):
        teachers_info.teacher_id = int(teachers_info.teacher_id)

        exits_teacher = await self.teachers_dao.get_teachers_by_id(teachers_info.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_employer = exits_teacher.teacher_employer
        teacher_id = teachers_info.teacher_id
        current_post_type = teachers_info.current_post_type
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_base_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        old_teachers_info = orm_model_to_view_model(exists_teachers_info, TeachersInfoModel, exclude=[""])
        old_teachers_info.teacher_id = int(old_teachers_info.teacher_id)
        old_teachers_info.teacher_base_id = int(old_teachers_info.teacher_base_id)
        if old_teachers_info.org_id:
            old_teachers_info.org_id = int(old_teachers_info.org_id)
        need_update_list = []
        for key, value in teachers_info.dict().items():
            if value:
                need_update_list.append(key)
        teachers_info_db = await self.teachers_info_dao.update_teachers_info(teachers_info, *need_update_list)
        fields_list = ["teacher_id", "teacher_base_id"]
        teachers_info_db = await convert_fields_to_str(teachers_info_db, fields_list)
        teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                         exclude=[""])
        teachers_main_status = teacher_entry_approval.teacher_main_status
        res = compare_modify_fields(teachers_info, old_teachers_info)
        if teachers_main_status == "unemployed":
            params = {"process_code": "t_entry", "applicant_name": user_id}
            teacher_entry_approval.teacher_sub_status = "submitted"
            await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
                teacher_entry_approval.teacher_id)
            work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
            teacher_entry_save_to_submit_log = OperationRecord(  # 这个是转在职的
                action_target_id=int(teacher_entry_approval.teacher_id),
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.NEW_ENTRY.value,
                change_detail="转在职",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=int(work_flow_instance["process_instance_id"]))
            await self.operation_record_rule.add_operation_record(teacher_entry_save_to_submit_log)
            await self.teacher_submitted(teacher_id)
            teachers_rule = get_injector(TeachersRule)
            await teachers_rule.teacher_progressing(teacher_id)
        if teachers_main_status == "employed":
            teacher_base_info_log = OperationRecord(
                action_target_id=int(teacher_entry_approval.teacher_id),
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data=str(res),
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.BASIC_INFO_CHANGE.value,
                change_detail="详情",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=0)
            await self.operation_record_rule.add_operation_record(teacher_base_info_log)
        organization = OrganizationMembers()
        organization.id = SnowflakeIdGenerator(1, 1).generate_id()
        organization.org_id = int(teachers_info.org_id)
        organization.teacher_id = int(teachers_info.teacher_id)
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.update_organization_members_by_teacher_id(organization)
        return teachers_info_db

    async def update_teachers_info_import(self, teachers_info: TeacherInfoImportSubmit, user_id):
        teacher_id = int(teachers_info.teacher_id)
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_base_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        need_update_list = []
        for key, value in teachers_info.dict().items():
            if value:
                need_update_list.append(key)
        teachers_info.org_id = int(teachers_info.org_id)
        teachers_info_db = await self.teachers_info_dao.update_teachers_info(teachers_info, *need_update_list)
        teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
                                                         exclude=[""])
        teachers_main_status = teacher_entry_approval.teacher_main_status
        if teachers_main_status == "unemployed":
            params = {"process_code": "t_entry", "applicant_name": user_id}
            teacher_entry_approval.teacher_sub_status = "submitted"
            await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
                teacher_entry_approval.teacher_id)
            work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
            teacher_entry_save_to_submit_log = OperationRecord(  # 这个是转在职的
                action_target_id=int(teacher_entry_approval.teacher_id),
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.NEW_ENTRY.value,
                change_detail="转在职",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=int(work_flow_instance["process_instance_id"]))
            await self.operation_record_rule.add_operation_record(teacher_entry_save_to_submit_log)
            await self.teacher_submitted(teacher_id)
            teachers_rule = get_injector(TeachersRule)
            await teachers_rule.teacher_progressing(teacher_id)
        organization = OrganizationMembers()
        organization.id = SnowflakeIdGenerator(1, 1).generate_id()
        organization.org_id = int(teachers_info.org_id)
        organization.teacher_id = int(teachers_info.teacher_id)
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.update_organization_members_by_teacher_id(organization)
        return True

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
        # fields_list = ["teacher_id", "teacher_base_id"]
        # teachers_info_db = await convert_fields_to_str(teachers_info, fields_list)
        # await self.teacher_unsubmitted(teachers_info.teacher_id)
        # if exits_teacher.teacher_main_status == "unemployed":
        #     teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        #     teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
        #                                                      exclude=[""])
        #     params = {"process_code": "t_entry", "applicant_name": user_id}
        #     await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
        #         teacher_entry_approval.teacher_id)
        #     await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)
        # if exits_teacher.teacher_main_status == "employed":
        # teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers_info.teacher_id)
        # teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
        #                                                  exclude=[""])
        # params = {"process_code": "t_keyinfo", "applicant_name": user_id}
        # await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
        #     teacher_entry_approval.teacher_id)
        # await self.teacher_work_flow_rule.add_teacher_work_flow(teacher_entry_approval, params)

        organization = OrganizationMembers()
        organization.id = SnowflakeIdGenerator(1, 1).generate_id()
        organization.org_id = int(teachers_info.org_id)
        organization.teacher_id = int(teachers_info.teacher_id)
        organization.member_type = None
        organization.identity = None
        await self.organization_members_rule.update_organization_members_by_teacher_id(organization)
        return True

    # 删除单个教职工基本信息
    async def delete_teachers_info(self, teachers_info_id):
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
        teachers_info_db = await self.teachers_info_dao.delete_teachers_info(exists_teachers_info)
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def query_teacher_with_page(self, query_model: NewTeacher, page_request: PageRequest, extend_param):
        params = {"process_code": "t_entry", "approval_status": "t_query"}
        params.update(extend_param)
        paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                      NewTeacherRe, params)
        return paging

    async def query_current_teacher_with_page(self, query_model: CurrentTeacherQuery, page_request: PageRequest,extend_params):
        paging = await self.teachers_info_dao.query_current_teacher_with_page(query_model, page_request,
                                                                              extend_params)
        paging_result = PaginatedResponse.from_paging(paging, CurrentTeacherQueryRe)
        return paging_result

    async def teacher_submitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "submitted":
            teachers.teacher_sub_status = "submitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")

    async def teacher_unsubmitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "unsubmitted":
            teachers.teacher_sub_status = "unsubmitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")
