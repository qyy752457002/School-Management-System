from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionQuery
from models.teachers_info import TeacherInfo
from models.teachers import Teacher


class TeacherTransactionDAO(DAOBase):

    async def add_teacher_transaction(self, teacher_transaction: TeacherTransaction):
        session = await self.master_db()
        session.add(teacher_transaction)
        await session.commit()
        await session.refresh(teacher_transaction)
        return teacher_transaction

    async def get_teacher_transaction_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherTransaction))
        return result.scalar()

    async def delete_teacher_transaction(self, teacher_transaction: TeacherTransaction):
        session = await self.master_db()
        await session.delete(teacher_transaction)
        await session.commit()

    async def get_teacher_transaction_by_teacher_transaction_id(self, teacher_transaction_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherTransaction).where(TeacherTransaction.id == teacher_transaction_id))
        return result.scalar_one_or_none()

    async def query_teacher_transaction_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherTransaction)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_transaction(self, teacher_transaction, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_transaction, *args)
        query = update(TeacherTransaction).where(TeacherTransaction.id == teacher_transaction.id).values(
            **update_contents)
        return await self.update(session, query, teacher_transaction, update_contents, is_commit=is_commit)
