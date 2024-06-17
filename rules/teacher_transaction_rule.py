from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_transaction_dao import TeacherTransactionDAO
from daos.teachers_dao import TeachersDao
from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQueryModel, TeacherTransactionApproval, TeacherTransactionGetModel
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from business_exceptions.teacher_transction import TransactionApprovalError
from rules.work_flow_instance_rule import WorkFlowNodeInstanceRule


@dataclass_inject
class TeacherTransactionRule(object):
    teacher_transaction_dao: TeacherTransactionDAO
    teachers_dao: TeachersDao
    work_flow_instance_rule: WorkFlowNodeInstanceRule

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
        result = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_id(
            teacher_transaction_db.teacher_id)
        if result.approval_status == "submitted":
            raise TransactionApprovalError()
        teacher_transaction_db = await self.teacher_transaction_dao.add_teacher_transaction(teacher_transaction_db)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionUpdateModel)
        return teacher_transaction

    async def query_transaction(self, teacher_id):
        result = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_id(
            teacher_id)
        is_transaction = True
        if not result:
            process_instance_id = result.process_instance_id
            work_flow_instance_status = await self.work_flow_instance_rule.get_work_flow_instance_status_by_work_flow_instance_id(
                process_instance_id)
            if work_flow_instance_status == "pending":
                is_transaction = False
        return is_transaction


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
        teacher_transaction.teacher_transaction_id)
    if not exists_teacher_transaction_info:
        raise Exception(f"编号为{teacher_transaction.teacher_transaction_id}的teacher_transaction不存在")
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
        if item.node_status == "pending":
            teacher_transaction.append(
                orm_model_to_view_model(item, TeacherTransactionGetModel,
                                        exclude=["approval_time", "approval_name"]))
        else:
            teacher_transaction.append(orm_model_to_view_model(item, TeacherTransactionGetModel))
    return teacher_transaction


async def query_transaction_with_page(self, query_model: TeacherTransactionQueryModel, page_request: PageRequest):
    teacher_transaction_db = await self.teacher_transaction_dao.query_transaction_with_page(query_model,
                                                                                            page_request)
    paging_result = PaginatedResponse.from_paging(teacher_transaction_db, TeacherTransactionApproval)
    return paging_result


# async def submitting(self, teacher_transaction_id):
#     teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
#         teacher_transaction_id)
#     if not teacher_transaction:
#         raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
#     teacher_transaction.approval_status = "submitting"
#     return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")

async def submitted(self, teacher_transaction_id):
    teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
        teacher_transaction_id)
    if not teacher_transaction:
        raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    teacher_transaction.approval_status = "submitted"
    return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")


async def approved(self, teacher_transaction_id):
    teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
        teacher_transaction_id)
    if not teacher_transaction:
        raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    teacher_transaction.approval_status = "approved"
    return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")


async def rejected(self, teacher_transaction_id):
    teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
        teacher_transaction_id)
    if not teacher_transaction:
        raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    teacher_transaction.approval_status = "rejected"
    return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")


async def revoked(self, teacher_transaction_id):
    teacher_transaction = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
        teacher_transaction_id)
    if not teacher_transaction:
        raise Exception(f"编号为{teacher_transaction_id}的teacher_transaction不存在")
    teacher_transaction.approval_status = "revoked"
    return await self.teacher_transaction_dao.update_teacher_transaction(teacher_transaction, "approval_status")


async def get_process_id(self, teacher_transaction: TeacherTransactionModel, process_code: str):
    pass
