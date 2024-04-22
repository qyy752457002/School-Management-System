from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.student_transaction_flow import StudentTransactionFlow


class StudentTransactionFlowDAO(DAOBase):

	async def add_studenttransactionflow(self, studenttransactionflow: StudentTransactionFlow):
		session = await self.master_db()
		session.add(studenttransactionflow)
		await session.commit()
		await session.refresh(studenttransactionflow)
		return studenttransactionflow

	async def get_studenttransactionflow_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(StudentTransactionFlow))
		return result.scalar()

	async def delete_studenttransactionflow(self, studenttransactionflow: StudentTransactionFlow):
		session = await self.master_db()
		await session.delete(studenttransactionflow)
		await session.commit()

	async def get_studenttransactionflow_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(StudentTransactionFlow).where(StudentTransactionFlow.id == id))
		return result.scalar_one_or_none()

	async def query_studenttransactionflow_with_page(self,  page_request: PageRequest,**kwargs,):
		query = select(StudentTransactionFlow)
		for key, value in kwargs.items():
		   query = query.where(getattr(StudentTransactionFlow, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_studenttransactionflow(self, studenttransactionflow, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(studenttransactionflow, *args)
		query = update(StudentTransactionFlow).where(StudentTransactionFlow.id == studenttransactionflow.id).values(**update_contents)
		return await self.update(session, query, studenttransactionflow, update_contents, is_commit=is_commit)
