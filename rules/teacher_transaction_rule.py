from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_transaction_dao import TeacherTransactionDAO
from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQuery,TeacherTransactionQueryRe


@dataclass_inject
class TeacherTransactionRule(object):
    teacher_transaction_dao: TeacherTransactionDAO

    async def get_teacher_transaction_by_teacher_transaction_id(self, teacher_transaction_id):
        teacher_transaction_db = await self.teacher_transaction_dao.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionModel)
        return teacher_transaction

    async def add_teacher_transaction(self, teacher_transaction: TeacherTransactionModel):
        teacher_transaction_db = view_model_to_orm_model(teacher_transaction, TeacherTransaction)
        teacher_transaction_db = await self.teacher_transaction_dao.add_teacher_transaction(teacher_transaction_db)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionModel)
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
        teacher_transaction_db = await self.teacher_transaction_dao.get_all_teacher_transaction(teacher_id)
        #          teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionModel, exclude=[""])
        teacher_transaction = []
        for item in teacher_transaction_db:
            teacher_transaction.append(orm_model_to_view_model(item, TeacherTransactionModel))
        return teacher_transaction

    async def query_teacher(self, teacher_transaction: TeacherTransactionQuery):
        teacher_transaction_db = await self.teacher_transaction_dao.query_teacher(teacher_transaction)
        teacher_transaction = []
        for item in teacher_transaction_db.items:
            teacher_transaction.append(orm_model_to_view_model(item, TeacherTransactionQueryRe))
        return teacher_transaction

