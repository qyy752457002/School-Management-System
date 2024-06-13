from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.subject import Subject


class SubjectDAO(DAOBase):

	async def add_subject(self, subject: Subject):
		session = await self.master_db()
		session.add(subject)
		await session.commit()
		await session.refresh(subject)
		return subject

	async def get_subject_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(Subject))
		return result.scalar()

	async def delete_subject(self, subject: Subject):
		session = await self.master_db()
		await session.delete(subject)
		await session.commit()

	async def get_subject_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Subject).where(Subject.id == id))
		return result.scalar_one_or_none()

	async def query_subject_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(Subject)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_subject(self, subject, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(subject, *args)
		query = update(Subject).where(Subject.id == subject.id).values(**update_contents)
		return await self.update(session, query, subject, update_contents, is_commit=is_commit)
