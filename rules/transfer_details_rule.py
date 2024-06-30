from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.databases.queries.pages import Pagination, Paging
from daos.transfer_details_dao import TransferDetailsDAO
from daos.teachers_dao import TeachersDao
from models.transfer_details import TransferDetails
from views.models.teacher_transaction import TransferDetailsModel
from views.models.teacher_transaction import TeacherTransactionQuery, TeacherTransactionQueryRe, \
    TransferDetailsReModel, TransferDetailsGetModel, TeacherTransferQueryModel, TeacherTransferQueryReModel, \
    TransferAndBorrowExtraModel
from business_exceptions.teacher import TeacherNotFoundError, ApprovalStatusError
from models.teacher_change_log import TeacherChangeLog
from daos.teacher_change_dao import TeacherChangeLogDAO
from rules.teacher_change_rule import TeacherChangeRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from daos.enum_value_dao import EnumValueDAO
from rules.enum_value_rule import EnumValueRule
from pydantic import BaseModel, Field
from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO
from rules.teachers_rule import TeachersRule
from views.models.teacher_transaction import TeacherAddModel, WorkflowQueryModel
from datetime import datetime
from daos.school_dao import SchoolDAO
from typing import Type


@dataclass_inject
class TransferDetailsRule(object):
    transfer_details_dao: TransferDetailsDAO
    teachers_dao: TeachersDao
    teacher_change_log: TeacherChangeLogDAO
    teacher_change_detail: TeacherChangeRule
    teacher_work_flow_rule: TeacherWorkFlowRule
    enum_value_dao: EnumValueDAO
    enum_value_rule: EnumValueRule
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO
    teachers_rule: TeachersRule
    school_dao: SchoolDAO

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        transfer_details_db = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel)
        return transfer_details

    async def add_transfer_in_inner_details(self, transfer_details: TransferDetailsModel, user_id):
        """
        系统内调入
        """
        exists_teachers = await self.teachers_dao.get_teachers_by_id(transfer_details.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        is_approval = exists_teachers.is_approval
        await self.teachers_rule.teacher_submitted(transfer_details.teacher_id)
        if is_approval:
            raise ApprovalStatusError()
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details_work = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
        transfer_and_borrow_extra_model = await self.get_transfer_and_borrow_extra(
            original_district_area_id=transfer_details_work.original_district_area_id,
            current_district_area_id=transfer_details_work.current_district_area_id,
            original_unit_id=transfer_details_work.original_unit_id,
            current_unit_id=transfer_details_work.current_unit_id)
        original_unit_name = transfer_and_borrow_extra_model.original_unit_name
        current_unit_name = transfer_and_borrow_extra_model.current_unit_name
        model_list = [exists_teachers, transfer_details_work, transfer_and_borrow_extra_model]
        params = {"process_code": "t_transfer_in_inner", "applicant_name": user_id}
        work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
        teacher_transfer_log = OperationRecord(
            action_target_id=transfer_details_work.teacher_id,
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.TRANSFER.value,
            change_detail=f"从{original_unit_name}调入到{current_unit_name}",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=work_flow_instance["process_instance_id"])
        await self.operation_record_rule.add_operation_record(teacher_transfer_log)
        return transfer_details

    async def add_transfer_in_outer_details(self, transfer_details: TransferDetailsModel, add_teacher: TeacherAddModel,
                                            user_id):
        teachers = await self.teachers_rule.add_transfer_teachers(add_teacher)
        transfer_details.teacher_id = teachers.teacher_id
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details_work = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
        transfer_and_borrow_extra_model = await self.get_transfer_and_borrow_extra(
            original_district_area_id=transfer_details_work.original_district_area_id,
            current_district_area_id=transfer_details_work.current_district_area_id,
            current_unit_id=transfer_details.current_unit_id)
        original_unit_name = transfer_details_work.original_unit_name
        current_unit_name = transfer_and_borrow_extra_model.current_unit_name
        params = {"process_code": "t_transfer_in_outer", "applicant_name": user_id}
        model_list = [transfer_details_work, teachers, transfer_and_borrow_extra_model]
        work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
        teacher_transfer_log = OperationRecord(
            action_target_id=transfer_details_work.teacher_id,
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.TRANSFER.value,
            change_detail=f"从{original_unit_name}调入到{current_unit_name}",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=work_flow_instance["process_instance_id"])
        await self.operation_record_rule.add_operation_record(teacher_transfer_log)

    async def add_transfer_out_details(self, transfer_details: TransferDetailsModel,
                                       user_id):
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details_work = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)

        transfer_and_borrow_extra_model = await self.get_transfer_and_borrow_extra(
            original_district_area_id=transfer_details_work.original_district_area_id,
            current_district_area_id=transfer_details_work.current_district_area_id,
            original_unit_id=transfer_details.original_unit_id)
        original_unit_name = transfer_details_work.original_unit_name
        current_unit_name = transfer_and_borrow_extra_model.current_unit_name
        params = {"process_code": "t_transfer_in_outer", "applicant_name": user_id}
        model_list = [transfer_details_work, transfer_and_borrow_extra_model]
        work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
        teacher_transfer_log = OperationRecord(
            action_target_id=transfer_details_work.teacher_id,
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.TRANSFER.value,
            change_detail=f"从{original_unit_name}调入到{current_unit_name}",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=work_flow_instance["process_instance_id"])
        await self.operation_record_rule.add_operation_record(teacher_transfer_log)
        return transfer_details

    async def delete_transfer_details(self, transfer_details_id):
        exists_transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not exists_transfer_details:
            raise Exception(f"编号为的{transfer_details_id}transfer_details不存在")
        transfer_details_db = await self.transfer_details_dao.delete_transfer_details(exists_transfer_details)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel, exclude=[""])
        return transfer_details

    async def update_transfer_details(self, transfer_details: TransferDetailsReModel):
        exists_transfer_details_info = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details.transfer_details_id)
        if not exists_transfer_details_info:
            raise Exception(f"编号为{transfer_details.transfer_details_id}的transfer_details不存在")
        need_update_list = []
        for key, value in transfer_details.dict().items():
            if value:
                need_update_list.append(key)
        transfer_details = await self.transfer_details_dao.update_transfer_details(transfer_details, *need_update_list)
        return transfer_details

    async def get_all_transfer_details(self, teacher_id):
        """
        详情页查询单个老师所有调动信息
        """
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        query_model = WorkflowQueryModel(teacher_id=teacher_id, process_code="transfer"),
        transfer_details = await self.teacher_work_flow_rule.get_work_flow_instance_by_query_model(query_model,
                                                                                                   TransferDetailsGetModel)
        return transfer_details

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        """
        查询老师是否在系统内
        """
        teacher_transaction_db = await self.teachers_dao.query_teacher_transfer(teacher_transaction)
        transfer_inner = True  # 系统内互转
        if teacher_transaction_db:
            teacher_transaction_db = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionQueryRe)
            return teacher_transaction_db, transfer_inner
        else:
            transfer_inner = False
            return teacher_transaction_db, transfer_inner

    # 调动管理分页查询相关
    async def query_transfer_out_with_page(self, type, query_model: TeacherTransferQueryModel,
                                           page_request: PageRequest, user_id):
        if type == "launch":
            params = {"applicant_name": user_id, "process_code": "t_transfer_out", "teacher_sub_status": "submitted"}
        elif type == "approval":
            params = {"applicant_name": user_id, "process_code": "t_transfer_out", "teacher_sub_status": "submitted"}
        result = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                      query_model,
                                                                                      TeacherTransferQueryReModel,
                                                                                      params)
        return result

    async def query_transfer_in_with_page(self, type, query_model: TeacherTransferQueryModel,
                                          page_request: PageRequest, user_id):
        result_list = []
        if type == "launch":
            params_inner = {"applicant_name": user_id, "process_code": "t_transfer_in_inner",
                            "teacher_sub_status": "submitted"}
            result_inner = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                                query_model,
                                                                                                TeacherTransferQueryReModel,
                                                                                                params_inner)
            params_outer = {"applicant_name": user_id, "process_code": "t_transfer_in_outer",
                            "teacher_sub_status": "submitted"}
            result_outer = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                                query_model,
                                                                                                TeacherTransferQueryReModel,
                                                                                                params_outer)


        elif type == "approval":
            params_inner = {"applicant_name": user_id, "process_code": "t_transfer_in_inner",
                            "teacher_sub_status": "submitted"}
            result_inner = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                                query_model,
                                                                                                TeacherTransferQueryReModel,
                                                                                                params_inner)
            params_outer = {"applicant_name": user_id, "process_code": "t_transfer_in_outer",
                            "teacher_sub_status": "submitted"}
            result_outer = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                                query_model,
                                                                                                TeacherTransferQueryReModel,
                                                                                                params_outer)
        result_list.append(result_inner)
        result_list.append(result_outer)
        return result_list

    async def get_transfer_and_borrow_extra(self, original_district_area_id=None,
                                            current_district_area_id=None, original_unit_id=None,
                                            current_unit_id=None) -> TransferAndBorrowExtraModel:
        original_district_province_name = original_district_city_name = original_district_area_name = ""
        current_district_province_name = current_district_city_name = current_district_area_name = ""
        original_unit_name = current_unit_name = ""
        if original_district_area_id:
            original_district_province_name, original_district_city_name, original_district_area_name = self.enum_value_rule.get_district_name(
                original_district_area_id)
        if current_district_area_id:
            current_district_province_name, current_district_city_name, current_district_area_name = self.enum_value_rule.get_district_name(
                current_district_area_id)
        if original_unit_id:
            school = await self.school_dao.get_school_by_id(original_unit_id)
            original_unit_name = school.school_name
        if current_unit_id:
            school = await self.school_dao.get_school_by_id(current_unit_id)
            current_unit_name = school.school_name
        return TransferAndBorrowExtraModel(original_district_province_name=original_district_province_name,
                                           original_district_city_name=original_district_city_name,
                                           original_district_area_name=original_district_area_name,
                                           current_district_province_name=current_district_province_name,
                                           current_district_city_name=current_district_city_name,
                                           current_district_area_name=current_district_area_name,
                                           original_unit_name=original_unit_name,
                                           current_unit_name=current_unit_name)

        # 调动管理审批相关

    async def transfer_approved(self, teacher_id, process_instance_id, user_id, reason):
        # todo 调动完成后，当地校的老师需要修改状态为调出或调入，同时本校的记录应该删除，另一个学校的应该copy，该老师信息并且有调入记录。
        user_id = user_id
        await self.teachers_rule.teacher_progressing(teacher_id)
        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            result = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            process_code = result.get("process_code")
            teachers_db = await self.teachers_dao.get_teachers_by_id(teacher_id)
            if process_code == "t_transfer_out":
                """需要删除本校老师"""
                # todo 需要发给两个学校消息
                teachers_db.teacher_sub_status = "transfer_out"
                await self.teachers_dao.update_teachers(teachers_db, "teacher_sub_status")
            elif process_code == "t_transfer_in_inner":
                """需要先修改本校老师状态，包括is_deleted和teacher_sub_status，然后再添加新的老师，以及增加老师的调入记录"""
                teachers_db.teacher_sub_status = "transfer_in"
                await self.teachers_dao.update_teachers(teachers_db, "teacher_sub_status")
            elif process_code == "t_transfer_in_outer":
                """增加老师再添加新老师"""
                teachers_db.teacher_sub_status = "transfer_in"
                teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result, TeacherAddModel)
                need_update_list = []
                for key, value in teacher.dict().items():
                    if value:
                        need_update_list.append(key)
                await self.teachers_dao.update_teachers(teachers_db, *need_update_list)
            await self.teachers_rule.teacher_pending(teachers_db.teachers_id)
            await self.teachers_rule.teacher_active(teachers_db.teacher_id)

            # teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result, TransferDetailsReModel)
            return "该老师调动审批已通过"
    async def transfer_rejected(self, transfer_details_id, process_instance_id, user_id, reason):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        user_id = user_id
        await self.teachers_rule.teacher_progressing(transfer_details.teacher_id)
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                   parameters)
        if node_instance == "rejected":
            await self.teachers_rule.teacher_active(transfer_details.teachers_id)
            await self.teachers_rule.teacher_pending(transfer_details.teachers_id)
            return "该老师调动审批已拒绝"

    async def transfer_revoked(self, transfer_details_id, process_instance_id, user_id, reason):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        await self.teachers_rule.teacher_progressing(transfer_details.teacher_id)
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "revoked":
            await self.teachers_rule.teacher_active(transfer_details.teachers_id)
            await self.teachers_rule.teacher_pending(transfer_details.teachers_id)
            return "该老师调动审批已撤回"
