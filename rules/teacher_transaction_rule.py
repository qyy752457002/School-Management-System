from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_transaction_dao import TeacherTransactionDAO
from daos.teachers_dao import TeachersDao
from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQueryModel, TeacherTransactionQueryReModel, TeacherTransactionGetModel, TransactionType
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from business_exceptions.teacher_transction import TransactionError
from rules.work_flow_instance_rule import WorkFlowNodeInstanceRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.enum_value_rule import EnumValueRule
from daos.enum_value_dao import EnumValueDAO
from models.enum_value import EnumValue
from mini_framework.utils.http import HTTPRequest
from urllib.parse import urlencode
from views.common.common_view import workflow_service_config

from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO
from views.common.common_view import compare_modify_fields
from mini_framework.utils.snowflake import SnowflakeIdGenerator

from datetime import datetime


@dataclass_inject
class TeacherTransactionRule(object):
    teacher_transaction_dao: TeacherTransactionDAO
    teachers_dao: TeachersDao
    work_flow_instance_rule: WorkFlowNodeInstanceRule
    teacher_work_flow_rule: TeacherWorkFlowRule
    enum_value_dao: EnumValueDAO
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO

    async def get_teacher_transaction_by_teacher_transaction_id(self, teacher_transaction_id):
        teacher_transaction_db = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionModel)
        return teacher_transaction

    async def add_teacher_transaction(self, teacher_transaction: TeacherTransactionModel):
        """
        添加教师异动
        """
        teacher_transaction_db = view_model_to_orm_model(teacher_transaction, TeacherTransaction)

        teacher_db = await self.teachers_dao.get_teachers_by_id(teacher_transaction_db.teacher_id)
        if not teacher_db:
            raise TeacherNotFoundError()
        # teacher_transaction_db.transaction_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_transaction_db = await self.teacher_transaction_dao.add_teacher_transaction(teacher_transaction_db)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionUpdateModel)
        return teacher_transaction

    async def add_teacher_transaction_except_retire(self, teacher_transaction: TeacherTransactionModel, user_id):
        """
        添加教师异动
        """
        transaction_type = teacher_transaction.transaction_type
        teacher_transaction_db = view_model_to_orm_model(teacher_transaction, TeacherTransaction)
        # teacher_transaction_db.transaction_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_db = await self.teachers_dao.get_teachers_by_id(teacher_transaction_db.teacher_id)
        teacher_sub_status = teacher_db.teacher_sub_status
        if not teacher_db:
            raise TeacherNotFoundError()
        if teacher_sub_status != "active":
            raise TransactionError()
        if transaction_type != TransactionType.INTERNAL.value:
            teacher_db.teacher_sub_status = transaction_type
            await self.teachers_dao.update_teachers(teacher_db, "teacher_sub_status")
            # teacher_transaction_db.transaction_id = SnowflakeIdGenerator(1, 1).generate_id()
            teacher_transaction_db = await self.teacher_transaction_dao.add_teacher_transaction(teacher_transaction_db)
            teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionUpdateModel)
            teacher_transaction_log = OperationRecord(
                action_target_id=teacher_transaction.teacher_id,
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.TRANSACTION.value,
                change_detail=f'{teacher_transaction.transaction_type}',
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=0)
        else:
            teacher_db.teacher_sub_status = transaction_type
            await self.teachers_dao.update_teachers(teacher_db, "teacher_sub_status")
            # teacher_transaction_db.transaction_id = SnowflakeIdGenerator(1, 1).generate_id()
            teacher_transaction_db = await self.teacher_transaction_dao.add_teacher_transaction(teacher_transaction_db)
            teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionUpdateModel)
            teacher_transaction_log = OperationRecord(
                action_target_id=teacher_transaction.teacher_id,
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data=f'{{"原岗位":{teacher_transaction.original_position}, "新岗位":{teacher_transaction.current_position}}}',
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.TRANSACTION.value,
                change_detail=f'{teacher_transaction.transaction_type}',
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=0)
        await self.operation_record_rule.add_operation_record(teacher_transaction_log)
        return teacher_transaction

    async def delete_teacher_transaction(self, teacher_transaction_id):
        exists_teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        if not exists_teacher_transaction:
            raise Exception(f"编号为的{teacher_transaction_id}teacher_transaction不存在")
        teacher_transaction_db = await self.teacher_transaction_dao.delete_teacher_transaction(
            exists_teacher_transaction)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionModel, exclude=[""])
        return teacher_transaction

    async def update_teacher_transaction(self, teacher_transaction: TeacherTransactionUpdateModel):
        exists_teacher_transaction_info = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction.transaction_id)
        if not exists_teacher_transaction_info:
            raise Exception(f"编号为{teacher_transaction.transaction_id}的teacher_transaction不存在")
        need_update_list = []
        for key, value in teacher_transaction.dict().items():
            if value:
                need_update_list.append(key)
        teacher_transaction = await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction,
                                                                                            *need_update_list)
        return teacher_transaction

    async def get_all_teacher_transaction(self, teacher_id):
        teacher_transaction_db = await self.teacher_transaction_dao.get_all_transfer(teacher_id)
        teacher_transaction = []
        for item in teacher_transaction_db:
            teacher_transaction.append(orm_model_to_view_model(item, TeacherTransactionGetModel))
        return teacher_transaction

    async def query_transaction_with_page(self, query_model: TeacherTransactionQueryModel, page_request: PageRequest):

        teacher_transaction_db = await self.teacher_transaction_dao.query_transaction_with_page(query_model,
                                                                                                page_request)
        paging_result = PaginatedResponse.from_paging(teacher_transaction_db, TeacherTransactionQueryReModel)
        return paging_result

    # async def submitted(self, teacher_transaction_id):
    #     teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
    #         teacher_transaction_id)
    #     if not teacher_transaction:
    #         raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    #     teacher_transaction.approval_status = "submitted"
    #     return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")
    #
    # async def approved(self, teacher_transaction_id):
    #     teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
    #         teacher_transaction_id)
    #     if not teacher_transaction:
    #         raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    #     teacher_transaction.approval_status = "approved"
    #     return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")
    #
    # async def rejected(self, teacher_transaction_id):
    #     teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
    #         teacher_transaction_id)
    #     if not teacher_transaction:
    #         raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    #     teacher_transaction.approval_status = "rejected"
    #     return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")

    async def revoked(self, teacher_transaction_id):
        teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        if not teacher_transaction:
            raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
        teacher_transaction.approval_status = "revoked"
        return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")

    async def transaction_teacher_active(self, teachers_id, transaction_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "active":
            teachers.teacher_main_status = "employed"
            teachers.teacher_sub_status = "active"
        await self.teachers_dao.update_teachers(teachers, "teacher_sub_status", "teacher_main_status")
        await self.change_is_active(transaction_id)
        return

    async def change_is_active(self, teacher_transaction_id):
        teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        teacher_transaction.is_active = True
        return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "is_active")
