import json
from datetime import datetime

from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.authentication.config import authentication_config
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.common import IdCardError
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from daos.operation_record_dao import OperationRecordDAO
from daos.school_dao import SchoolDAO
from daos.teacher_approval_log_dao import TeacherApprovalLogDao
from daos.teacher_change_dao import TeacherChangeLogDAO
from daos.teacher_entry_dao import TeacherEntryApprovalDao
from daos.teacher_key_info_approval_dao import TeacherKeyInfoApprovalDao
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from daos.user_org_relation_dao import UserOrgRelationDao
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from rules.common.common_rule import get_identity_by_job
from rules.operation_record import OperationRecordRule
from rules.organization_memebers_rule import OrganizationMembersRule
from rules.system_rule import SystemRule
from rules.teacher_change_rule import TeacherChangeRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.user_org_relation_rule import UserOrgRelationRule
from views.common.common_view import check_id_number
from views.common.common_view import compare_modify_fields
from views.common.common_view import orgcenter_service_config
from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from views.models.organization import OrganizationMembers
from views.models.school import School as SchoolModel
from views.models.teachers import TeacherApprovalQuery, TeacherApprovalQueryRe, TeacherChangeLogQueryModel, \
    CurrentTeacherInfoSaveModel, TeacherRe, TeacherAdd, TeachersSchool
from views.models.teachers import Teachers as TeachersModel
from views.models.teachers import TeachersCreatModel, TeacherInfoSaveModel, TeacherFileStorageModel, \
    NewTeacherApprovalCreate, TeachersSaveImportCreatModel, EducateUserModel, IdentityType, \
    TeachersSaveImportCreatTestModel


@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao
    teachers_info_dao: TeachersInfoDao
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    # teachers_info_rule: TeachersInfoRule
    teacher_entry_approval_dao: TeacherEntryApprovalDao
    teacher_work_flow_rule: TeacherWorkFlowRule
    teacher_key_info_approval_dao: TeacherKeyInfoApprovalDao
    teacher_change_log: TeacherChangeLogDAO
    teacher_change_detail: TeacherChangeRule
    teacher_approval_log: TeacherApprovalLogDao
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO
    school_dao: SchoolDAO
    organization_members_rule: OrganizationMembersRule
    user_org_relation_dao: UserOrgRelationDao

    async def get_teachers_by_id(self, teachers_id):
        teachers_id = int(teachers_id)
        teacher_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teacher_db:
            raise TeacherNotFoundError()
        # 可选 ,
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        if teachers.teacher_avatar:
            sysrule = get_injector(SystemRule)
            fileurl = await sysrule.get_download_url_by_id(teachers.teacher_avatar)
            teachers.teacher_avatar_url = fileurl
        return teachers

    # async def get_teachers_by_username(self, username):
    #     teacher_db = await self.teachers_dao.get_teachers_by_username(username)
    #     teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
    #     return teachers
    async def get_teachers_by_teacher_id_number(self, teacher_id_number):
        teacher_db = await self.teachers_dao.get_teachers_by_teacher_id_number(teacher_id_number)
        if not teacher_db:
            raise TeacherNotFoundError()
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def add_teachers(self, teachers: TeachersCreatModel, user_id):
        teacher_id_number = teachers.teacher_id_number
        teacher_id_type = teachers.teacher_id_type
        teacher_name = teachers.teacher_name
        teacher_gender = teachers.teacher_gender
        length = await self.teachers_dao.get_teachers_info_by_prams(teacher_id_number, teacher_id_type,
                                                                    teacher_name, teacher_gender)
        if length > 0:
            raise TeacherExistsError()
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[])
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers_work = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        school = await self.school_dao.get_school_by_id(teachers.teacher_employer)
        school_name = ""
        borough = ""
        if school:
            school_name = school.school_name
            borough = school.borough
        params = {"process_code": "t_entry", "applicant_name": user_id, "school_name": school_name, "borough": borough}
        await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
            teachers_work.teacher_id)
        work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teachers_work, params)
        # update_params = {"teacher_sub_status": "submitted"}
        # await self.teacher_work_flow_rule.update_work_flow_by_param(work_flow_instance["process_instance_id"],
        #                                                             update_params)
        teacher_entry_log = OperationRecord(
            action_target_id=int(teachers_work.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.NEW_ENTRY.value,
            change_detail="入职登记",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=int(work_flow_instance["process_instance_id"]))
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        teachers_info = TeacherInfoSaveModel(teacher_id=teachers_work.teacher_id)
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        teacher_base_id = teachers_info.teacher_base_id
        return teachers_work, teacher_base_id

    async def add_teachers_import_save(self, teachers: TeachersSaveImportCreatModel, user_id):
        teacher_id_number = teachers.teacher_id_number
        teacher_id_type = teachers.teacher_id_type
        teacher_name = teachers.teacher_name
        teacher_gender = teachers.teacher_gender
        length = await self.teachers_dao.get_teachers_info_by_prams(teacher_id_number, teacher_id_type,
                                                                    teacher_name, teacher_gender)
        if length > 0:
            raise TeacherExistsError()
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[])
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers_work = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        school = await self.school_dao.get_school_by_id(teachers.teacher_employer)
        school_name = ""
        borough = ""
        if school:
            school_name = school.school_name
            borough = school.borough
        params = {"process_code": "t_entry", "applicant_name": user_id, "school_name": school_name, "borough": borough}
        await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
            teachers_work.teacher_id)
        work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teachers_work, params)
        # update_params = {"teacher_sub_status": "submitted"}
        # await self.teacher_work_flow_rule.update_work_flow_by_param(work_flow_instance["process_instance_id"],
        #                                                             update_params)
        teacher_entry_log = OperationRecord(
            action_target_id=int(teachers_work.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.NEW_ENTRY.value,
            change_detail="入职登记",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=int(work_flow_instance["process_instance_id"]))
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        teachers_info = TeacherInfoSaveModel(teacher_id=teachers_work.teacher_id)
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        teacher_base_id = teachers_info.teacher_base_id
        return teachers_work, teacher_base_id

    async def add_teachers_import_save_test(self, teachers: TeachersSaveImportCreatTestModel):
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[])
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_db.teacher_main_status = "employed"
        teachers_db.teacher_sub_status = "active"
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers_work = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        teachers_info = TeacherInfoSaveModel(teacher_id=teachers_work.teacher_id, org_id=teachers.org_id,
                                             department=str(teachers.org_id), )
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        # await self.add_teacher_organization_members(int(teachers_work.teacher_id))
        return teachers_work.teacher_id

    async def query_teacher_operation_record_with_page(self, query_model: TeacherChangeLogQueryModel,
                                                       page_request: PageRequest):
        """
        查询教师操作记录
        """
        paging = await self.operation_record_dao.query_teacher_operation_record_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, OperationRecord)
        return paging_result

    async def add_transfer_teachers(self, teachers: TeacherAdd):
        """
        系统外调入系统内时使用
        """
        teachers.teacher_main_status = "employed"
        teachers.teacher_sub_status = "submitted"
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        teachers_db.is_approval = True
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        # 获取老师信息
        teachers = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        return teachers

    async def update_teachers(self, teachers, user_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        old_teachers = orm_model_to_view_model(exists_teachers, TeachersModel, exclude=["hash_password"])
        old_teachers.teacher_id = int(old_teachers.teacher_id)
        old_teachers.teacher_employer = int(old_teachers.teacher_employer)
        teachers_main_status = exists_teachers.teacher_main_status
        if teachers_main_status == "employed":
            # teacher_info_db= await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers.teacher_id)
            # teacher_info = orm_model_to_view_model(teacher_info_db, CurrentTeacherInfoSaveModel, exclude=[""])
            # model_list=[teachers,teacher_info]

            # teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers.teacher_id)
            # teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
            #                                                  exclude=[""])
            res = compare_modify_fields(teachers, old_teachers)
            params = {"process_code": "t_keyinfo", "teacher_id": teachers.teacher_id, "applicant_name": user_id}
            school = await self.school_dao.get_school_by_id(teachers.teacher_employer)
            school_name = ""
            borough = ""
            if school:
                school_name = school.school_name
                borough = school.borough
            teachers_school = TeachersSchool(school_name=school_name, teacher_main_status="employed",
                                             teacher_sub_status="active", borough=borough)
            model_list = [teachers, teachers_school]
            work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
            await self.teacher_progressing(teachers.teacher_id)
            teacher_change_log = OperationRecord(
                action_target_id=int(teachers.teacher_id),
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.MODIFY.value,
                ip="127.0.0.1",
                change_data=str(res),
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.KEY_INFO_CHANGE.value,
                change_detail="详情",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=int(work_flow_instance["process_instance_id"]))
            await self.operation_record_rule.add_operation_record(teacher_change_log)

        elif teachers_main_status == "unemployed":
            need_update_list = []
            for key, value in teachers.dict().items():
                if value:
                    need_update_list.append(key)
            teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return str(teachers.teacher_id)

    async def delete_teachers(self, teachers_id, user_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        teachers_db = await self.teachers_dao.delete_teachers(exists_teachers)
        await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
            teachers_id)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        teacher_entry_log = OperationRecord(
            action_target_id=int(teachers.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.DELETE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.NEW_ENTRY.value,
            change_detail="删除",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=0)
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        return True

    async def get_all_teachers(self):
        teachers_db = await self.teachers_dao.get_all_teachers()
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def get_teachers_count(self):
        teachers_count = await self.teachers_dao.get_teachers_count()
        return teachers_count

    # async def submitting(self, teachers_id):
    #     teachers = await self.teacher_entry_approval_dao.get_teacher_entry_by_teacher_id(teachers_id)
    #     if not teachers:
    #         raise TeacherNotFoundError()
    #     teachers.approval_status = "submitting"
    #     return await self.teacher_entry_approval_dao.update_teachers(teachers, "approval_status")
    #

    async def entry_approved(self, teachers_id, process_instance_id, user_id, reason):
        await self.teacher_progressing(teachers_id)
        user_id = user_id
        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            teachers_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teachers_db.teacher_main_status = "employed"
            teachers_db.teacher_sub_status = "active"
            teachers_db.is_approval = False
            params = {"teacher_main_status": "employed", "teacher_sub_status": "active"}
            await self.teacher_work_flow_rule.update_work_flow_by_param(process_instance_id, params)
            await self.teachers_dao.update_teachers(teachers_db, "teacher_main_status", "teacher_sub_status",
                                                    "is_approval")
            await self.add_teacher_organization_members(int(teachers_id))
            return "该老师入职审批已通过"

    async def entry_rejected(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            teacher = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teacher.teacher_main_status = "unemployed"
            teacher.teacher_sub_status = "unsubmitted"
            teacher.is_approval = False
            await self.teachers_dao.update_teachers(teacher, "teacher_main_status", "teacher_sub_status",
                                                    "is_approval")
            return "该老师入职审批已拒绝"

    async def entry_revoked(self, teachers_id, process_instance_id, user_id):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke"}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "revoked":
            teacher = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teacher.teacher_sub_status = "unsubmitted"
            teacher.is_approval = False
            await self.teachers_dao.update_teachers(teacher, "teacher_sub_status", "is_approval")
            return "该老师入职审批已撤回"

    # 关键信息审批相关
    async def teacher_info_change_approved(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id

        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            result = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result, TeachersModel)
            need_update_list = []
            for key, value in teacher.dict().items():
                if value:
                    need_update_list.append(key)
            await self.teachers_dao.update_teachers(teacher, *need_update_list)
            await self.teacher_pending(teachers_id)
            await self.teacher_active(teachers_id)
            return "该老师关键信息变更审批已通过"

    async def teacher_info_change_rejected(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            await self.teacher_active(teachers_id)
            await self.teacher_pending(teachers_id)
            return "该老师关键信息变更审批已拒绝"

    async def teacher_info_change_revoked(self, teachers_id, process_instance_id, user_id):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke"}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "revoked":
            await self.teacher_active(teachers_id)
            await self.teacher_pending(teachers_id)
            return "该老师关键信息变更审批已撤回"

    # 审批相关
    async def query_teacher_approval_with_page(self, type, query_model: TeacherApprovalQuery,
                                               page_request: PageRequest, extend_param):
        if type == "launch":
            # params = {"applicant_name": user_id, "process_code": "t_entry", "teacher_sub_status": "submitted"}
            params = {"process_code": "t_entry", "teacher_sub_status": "submitted"}
            params.update(extend_param)
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        elif type == "approval":
            params = {"process_code": "t_entry", "teacher_sub_status": "submitted"}
            params.update(extend_param)
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        return paging

    async def query_teacher_info_change_approval(self, type, query_model: TeacherApprovalQuery,
                                                 page_request: PageRequest, extend_param):
        if type == "launch":
            params = {"process_code": "t_keyinfo", "teacher_main_status": "employed"}
            params.update(extend_param)
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        elif type == "approval":
            params = {"process_code": "t_keyinfo", "teacher_main_status": "employed"}
            params.update(extend_param)
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        return paging

    async def get_teacher_approval_by_teacher_id(self, teacher_id):
        teacher_approval_db = await self.teachers_info_dao.get_teacher_approval(teacher_id)
        teacher_approval = orm_model_to_view_model(teacher_approval_db, NewTeacherApprovalCreate)
        return teacher_approval

    async def teacher_progressing(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if not teachers.is_approval:
            teachers.is_approval = True
        else:
            return
        return await self.teachers_dao.update_teachers(teachers, "is_approval")

    async def teacher_submitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_sub_status = "submitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")

    async def teacher_pending(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.is_approval:
            teachers.is_approval = False
        else:
            return
        return await self.teachers_dao.update_teachers(teachers, "is_approval")

    async def teacher_active(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "active":
            teachers.teacher_sub_status = "active"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")

    async def get_task_model_by_id(self, id):
        fileinfo = await self.file_storage_dao.get_file_by_id(int(id))
        fileinfo = fileinfo._asdict()['FileStorage']
        task_model = TeacherFileStorageModel(file_name=fileinfo.file_name,
                                             virtual_bucket_name=fileinfo.virtual_bucket_name,
                                             file_size=fileinfo.file_size)
        return task_model

    async def send_teacher_to_org_center(self, teacher_id):
        teacher_info = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teacher_id)
        org_id = teacher_info.org_id
        teacher_db = await self.teachers_dao.get_teachers_arg_by_id(teacher_id, org_id)
        if not teacher_db:
            raise Exception("未找到符合要求的老师")
        dict_data = orm_model_to_view_model(teacher_db, EducateUserModel, exclude=[""])
        id_card_type = IdentityType.from_to_org(dict_data.idCardType)
        dict_data_dict = dict_data.dict()
        dict_data_dict["idCardType"] = id_card_type
        params_data = JsonUtils.dict_to_json_str(dict_data_dict)
        httpreq = HTTPRequest()
        url = orgcenter_service_config.orgcenter_config.get("url")
        api_name = '/api/add-educate-user'
        url = url + api_name
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = await httpreq.post(url, params_data, headerdict)
        result = JsonUtils.json_str_to_dict(response)
        print(result)
        if result["status"] != "ok":
            raise Exception(response)
        user_id = result["data2"]
        user_org_relation_rule = get_injector(UserOrgRelationRule)
        await user_org_relation_rule.add_user_org_relation(int(teacher_id), user_id)
        await self.send_user_department_to_org_center(teacher_id, user_id)
        return result

    async def send_user_department_to_org_center(self, teacher_id, user_id):
        teacher_info = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teacher_id)
        org_id = teacher_info.org_id
        teacher_db = await self.teachers_dao.get_teachers_arg_by_id(teacher_id, org_id)
        if not teacher_db:
            raise Exception("未找到符合要求的老师")
        dict_data = orm_model_to_view_model(teacher_db, EducateUserModel, exclude=[""])
        dict_data_dict = dict_data.dict()
        unitId = dict_data_dict["currentUnit"]
        department_id = dict_data_dict["departmentId"]
        identity = dict_data_dict["identity"]
        identityType = dict_data_dict["identityType"]
        depart_parm = {"unitId": unitId,
                       "departmentId": department_id,
                       "identity": identity,
                       "identityType": identityType,
                       "userId": user_id,
                       "clientId": authentication_config.oauth2.client_id,
                       "clientSecret": authentication_config.oauth2.client_secret,
                       }
        depart_parm_list = [depart_parm]
        httpreq = HTTPRequest()
        url = orgcenter_service_config.orgcenter_config.get("url")
        api_name = '/api/add-educate-user-department-identitys'
        url = url + api_name
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            json_data = json.dumps(depart_parm_list)
            print(json_data)
            response = await httpreq.post(url, json_data, headerdict)
            result = JsonUtils.json_str_to_dict(response)
            return result
        except Exception as e:
            return e

    async def get_teacher_identity(self, teacher_id):
        current_post_type = ""
        teacher_db = await self.teachers_dao.get_teachers_by_id(teacher_id)
        teacher_employer = teacher_db.teacher_employer
        teacher_info_db = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teacher_id)
        if teacher_info_db:
            current_post_type = teacher_info_db.current_post_type
        school = await self.school_dao.get_school_by_id(int(teacher_employer))
        school_operation_type = []
        if school:
            school = orm_model_to_view_model(school, SchoolModel)
            if school.school_edu_level:
                school_operation_type.append(school.school_edu_level)
            if school.school_category:
                school_operation_type.append(school.school_category)
            if school.school_operation_type:
                school_operation_type.append(school.school_operation_type)
        identity_type, identity = await get_identity_by_job(school_operation_type, current_post_type)
        return identity_type, identity

    async def add_teacher_organization_members(self, teacher_id):
        identity_type, identity = await self.get_teacher_identity(teacher_id)
        teacher_info_db = await self.teachers_info_dao.get_teachers_info_by_teacher_id(teacher_id)
        org_id = teacher_info_db.org_id
        organization = OrganizationMembers()
        organization.id = SnowflakeIdGenerator(1, 1).generate_id()
        organization.org_id = int(org_id)
        organization.teacher_id = int(teacher_id)
        organization.member_type = identity_type
        organization.identity = identity
        return await self.organization_members_rule.add_organization_members(organization)
