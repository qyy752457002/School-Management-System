from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionQueryModel
from models.teachers_info import TeacherInfo
from models.teachers import Teacher
from models.school import School


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
        result = await session.execute(
            select(TeacherTransaction).where(TeacherTransaction.transaction_id == teacher_transaction_id))
        return result.scalar_one_or_none()



    async def update_teacher_transaction(self, teacher_transaction, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_transaction, *args)
        query = update(TeacherTransaction).where(
            TeacherTransaction.transaction_id == teacher_transaction.transaction.id).values(
            **update_contents)
        return await self.update(session, query, teacher_transaction, update_contents, is_commit=is_commit)

    async def query_transaction_with_page(self, query_model: TeacherTransactionQueryModel,
                                          page_request: PageRequest) -> Paging:
        """
        异动查询
        """

        query = select(TeacherTransaction, Teacher.teacher_name, Teacher.teacher_employer, School.school_name,
                       TeacherInfo.teacher_number).join(Teacher, Teacher.teacher_id == TeacherTransaction.teacher_id,
                                                        isouter=True).join(
            TeacherInfo, TeacherInfo.teacher_id == TeacherTransaction.teacher_id, isouter=True).join(School,
                                                                                                     School.id == Teacher.teacher_employer,
                                                                                                     isouter=True)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.teacher_employer:
            if query_model.teacher_employer != 0:
                query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
            else:
                pass
        if query_model.teacher_number:
            query = query.where(TeacherInfo.teacher_number == query_model.teacher_number)
        if query_model.operator_name:
            query = query.where(TeacherTransaction.operator_name.like(f"%{query_model.operator_name}%"))
        if query_model.approval_name:
            query = query.where(TeacherTransaction.approval_name.like(f"%{query_model.approval_name}%"))
        query = query.order_by(TeacherTransaction.transaction_time.desc())
        paging = await self.query_page(query, page_request)
        return paging


    async def get_all_transfer(self,teacher_id):
        session = await self.slave_db()
        query = select(TeacherTransaction).join(Teacher, TeacherTransaction.teacher_id == Teacher.teacher_id).where(
            TeacherTransaction.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
