from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.databases.queries.pages import Pagination, Paging
from daos.transfer_details_dao import TransferDetailsDAO
from daos.teachers_dao import TeachersDao
from models.transfer_details import TransferDetails
from views.models.teacher_transaction import TransferDetailsModel
from views.models.teacher_transaction import TeacherTransactionQuery, TeacherTransactionQueryRe, \
    TransferDetailsReModel, TransferDetailsGetModel, TeacherTransferQueryModel, TeacherTransferQueryReModel
from business_exceptions.teacher import TeacherNotFoundError, ApprovalStatusError
from models.teacher_change_log import TeacherChangeLog
from daos.teacher_change_dao import TeacherChangeLogDAO
from rules.teacher_change_rule import TeacherChangeRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from daos.enum_value_dao import EnumValueDAO
from rules.enum_value_rule import EnumValueRule

from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO
from rules.teachers_rule import TeachersRule

from datetime import datetime


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

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        transfer_details_db = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel)
        return transfer_details

    async def add_transfer_in_inner_details(self, transfer_details: TransferDetailsModel, user_id):
        """
        系统内调入
        """
        original_unit_id = transfer_details.original_unit_id
        current_unit_id = transfer_details.current_unit_id
        exists_teachers = await self.teachers_dao.get_teachers_by_id(transfer_details.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        is_approval = exists_teachers.is_approval
        if is_approval:
            raise ApprovalStatusError()
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details_work = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
        params = {"process_code": "t_transfer_in_inner", "applicant_name": user_id}
        work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(transfer_details_work, params)
        teacher_entry_log = OperationRecord(
            action_target_id=transfer_details_work.teacher_id,
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.TRANSFER.value,
            change_detail=f"从{original_unit_id}调入到{current_unit_id}",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=work_flow_instance["process_instance_id"])
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        return transfer_details

    async def add_transfer_in_outer_details(self, add_teacher, user_id):
        pass




    async def add_transfer_out_details(self, transfer_details: TransferDetailsModel):
        """
        调出
        """
        # todo 需要增加获取调出流程实例id
        # todo 变更日志没写
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
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
        transfer_details_db = await self.transfer_details_dao.get_all_transfer_details(teacher_id)
        transfer_details = []
        for item in transfer_details_db:
            transfer_details.append(orm_model_to_view_model(item, TransferDetailsGetModel))
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
                                           page_request: PageRequest):
        params = {"original_district_area_id": "original_district_area_name",
                  "original_district_city_id": "original_district_city_name",
                  "original_district_province_id": "original_region_province_name",
                  "original_region_area_id": "current_district_area_name",
                  "original_region_city_id": "original_region_city_name",
                  "original_region_province_id": "original_region_province_name",
                  "current_district_area_id": "current_district_area_name",
                  "current_district_city_id": "current_district_city_name",
                  "current_district_province_id": "current_region_province_name",
                  "current_region_area_id": "current_district_area_name",
                  "current_region_city_id": "current_region_city_name",
                  "current_region_province_id": "current_region_province_name",
                  }
        if type == "launch":
            teacher_transaction_db = await self.transfer_details_dao.query_transfer_out_launch_with_page(query_model,
                                                                                                         page_request)
            teacher_transaction_page = await self.query_deal(teacher_transaction_db)
            paging_result = PaginatedResponse.from_paging(teacher_transaction_page, TeacherTransferQueryReModel,
                                                          other_mapper=params)

            # for item in teacher_transaction_db.items:
            #     original_district_area_id = item.original_district_area_id
            #     current_district_area_id = item.current_district_area_id
            #     original_region_area_id = item.original_region_area_id
            #     current_region_area_id = item.current_region_area_id
            #
            #     original_district_province_name, original_district_city_name, original_district_area_name = self.enum_value_rule.get_district_name(
            #         original_district_area_id)
            #     item.original_region_province_id = original_district_province_name
            #     item.original_district_city_id = original_district_city_name
            #     item.original_district_area_id = original_district_area_name
            #
            #     current_district_province_name, current_district_city_name, current_district_area_name = self.enum_value_rule.get_district_name(
            #         current_district_area_id)
            #     item.current_region_province_id = current_district_province_name
            #     item.current_district_city_id = current_district_city_name
            #     item.current_district_area_id = current_district_area_name
            #
            #     original_region_province_name, original_region_city_name, original_region_area_name = self.enum_value_rule.get_district_name(
            #         original_region_area_id)
            #     item.original_region_province_id = original_region_province_name
            #     item.original_region_city_id = original_region_city_name
            #     item.original_region_area_id = original_region_area_name
            #
            #     current_region_province_name, current_region_city_name, current_region_area_name = self.enum_value_rule.get_district_name(
            #         current_region_area_id)
            #     item.current_region_province_id = current_region_province_name
            #     item.current_region_city_id = current_region_city_name
            #     item.current_region_area_id = current_region_area_name
        elif type == "approval":
            teacher_transaction_db = await self.transfer_details_dao.query_transfer_out_approval_with_page(query_model,
                                                                                                           page_request)
            teacher_transaction_page = await self.query_deal(teacher_transaction_db)
            paging_result = PaginatedResponse.from_paging(teacher_transaction_page, TeacherTransferQueryReModel,
                                                          other_mapper=params)
        return paging_result

    async def query_transfer_in_with_page(self, type, query_model: TeacherTransferQueryModel,
                                          page_request: PageRequest):
        if type == "launch":
            teacher_transaction_db = await self.transfer_details_dao.query_transfer_in_launch_with_page(query_model,
                                                                                                        page_request)
        elif type == "approval":
            teacher_transaction_db = await self.transfer_details_dao.query_transfer_in_approval_with_page(query_model,
                                                                                                          page_request)
        paging_result = PaginatedResponse.from_paging(teacher_transaction_db, TeacherTransferQueryReModel)
        return paging_result

    async def query_deal(self, page: Paging):
        for item in page.items:
            original_district_area_id = item.original_district_area_id
            current_district_area_id = item.current_district_area_id
            original_region_area_id = item.original_region_area_id
            current_region_area_id = item.current_region_area_id

            original_district_province_name, original_district_city_name, original_district_area_name = self.enum_value_rule.get_district_name(
                original_district_area_id)
            item.original_region_province_id = original_district_province_name
            item.original_district_city_id = original_district_city_name
            item.original_district_area_id = original_district_area_name

            current_district_province_name, current_district_city_name, current_district_area_name = self.enum_value_rule.get_district_name(
                current_district_area_id)
            item.current_region_province_id = current_district_province_name
            item.current_district_city_id = current_district_city_name
            item.current_district_area_id = current_district_area_name

            original_region_province_name, original_region_city_name, original_region_area_name = self.enum_value_rule.get_district_name(
                original_region_area_id)
            item.original_region_province_id = original_region_province_name
            item.original_region_city_id = original_region_city_name
            item.original_region_area_id = original_region_area_name

            current_region_province_name, current_region_city_name, current_region_area_name = self.enum_value_rule.get_district_name(
                current_region_area_id)
            item.current_region_province_id = current_region_province_name
            item.current_region_city_id = current_region_city_name
            item.current_region_area_id = current_region_area_name
        return page

    # 调动管理审批相关
    async def transfer_approved(self, teacher_id, process_instance_id, user_id, reason):
        user_id = user_id
        await self.teachers_rule.teacher_progressing(teacher_id)
        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            result = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result, TransferDetailsReModel)
            teachers_db = await self.teachers_dao.get_teachers_by_id(teacher_id)
            await self.teachers_dao.update_teachers(teachers_db, "teacher_sub_status")
        else:
            transfer_details.approval_status = "processing"
            await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")
        # todo 审批日志没写

    async def transfer_rejected(self, transfer_details_id, process_instance_id, user_id, reason):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        user_id = user_id
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            transfer_details.approval_status = "rejected"
            await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")
        # todo 审批日志没写

    async def transfer_revoked(self, transfer_details_id, process_instance_id, user_id, reason):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "revoked":
            transfer_details.approval_status = "revoked"
            await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")
        # todo 审批日志没写
