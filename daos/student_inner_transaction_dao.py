from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.student_inner_transaction import StudentInnerTransaction


class StudentInnerTransactionDAO(DAOBase):

	async def add_student_inner_transaction(self, student_inner_transaction: StudentInnerTransaction):
		session = await self.master_db()
		session.add(student_inner_transaction)
		await session.commit()
		await session.refresh(student_inner_transaction)
		return student_inner_transaction

	async def get_student_inner_transaction_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(StudentInnerTransaction))
		return result.scalar()

	async def delete_student_inner_transaction(self, student_inner_transaction: StudentInnerTransaction):
		session = await self.master_db()
		await session.delete(student_inner_transaction)
		await session.commit()

	async def get_student_inner_transaction_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(StudentInnerTransaction).where(StudentInnerTransaction.id == id))
		return result.scalar_one_or_none()

	async def query_student_inner_transaction_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(StudentInnerTransaction)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_student_inner_transaction(self, student_inner_transaction, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(student_inner_transaction, *args)
		query = update(StudentInnerTransaction).where(StudentInnerTransaction.id == student_inner_transaction.id).values(**update_contents)
		return await self.update(session, query, student_inner_transaction, update_contents, is_commit=is_commit)
