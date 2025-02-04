from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_transaction import TeacherTransaction


class TeacherTransactionDAO(DAOBase):

	async def add_teachertransaction(self, teachertransaction: TeacherTransaction):
		session = await self.master_db()
		session.add(teachertransaction)
		await session.commit()
		await session.refresh(teachertransaction)
		return teachertransaction

	async def get_teachertransaction_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherTransaction))
		return result.scalar()

	async def delete_teachertransaction(self, teachertransaction: TeacherTransaction):
		session = await self.master_db()
		await session.delete(teachertransaction)
		await session.commit()

	async def get_teachertransaction_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherTransaction).where(TeacherTransaction.id == id))
		return result.scalar_one_or_none()

	async def query_teachertransaction_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherTransaction)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teachertransaction(self, teachertransaction, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teachertransaction, *args)
		query = update(TeacherTransaction).where(TeacherTransaction.id == teachertransaction.id).values(**update_contents)
		return await self.update(session, query, teachertransaction, update_contents, is_commit=is_commit)
