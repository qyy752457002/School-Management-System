from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.graduation_student import GraduationStudent


class GraduationStudentDAO(DAOBase):

	async def add_graduationstudent(self, graduationstudent: GraduationStudent):
		session = await self.master_db()
		session.add(graduationstudent)
		await session.commit()
		await session.refresh(graduationstudent)
		return graduationstudent

	async def get_graduationstudent_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(GraduationStudent))
		return result.scalar()

	async def delete_graduationstudent(self, graduationstudent: GraduationStudent):
		session = await self.master_db()
		await session.delete(graduationstudent)
		await session.commit()

	async def get_graduationstudent_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(GraduationStudent).where(GraduationStudent.id == id))
		return result.scalar_one_or_none()

	async def query_graduationstudent_with_page(self, page_request: PageRequest, **kwargs):
		query = select(GraduationStudent)
		for key, value in kwargs.items():
		   query = query.where(getattr(GraduationStudent, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_graduationstudent(self, graduationstudent, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(graduationstudent, *args)
		query = update(GraduationStudent).where(GraduationStudent.id == graduationstudent.id).values(**update_contents)
		return await self.update(session, query, graduationstudent, update_contents, is_commit=is_commit)
