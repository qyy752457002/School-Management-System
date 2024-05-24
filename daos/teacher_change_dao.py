from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_change import TeacherChange


class TeacherChangeDAO(DAOBase):

	async def add_teacher_change(self, teacher_change: TeacherChange):
		session = await self.master_db()
		session.add(teacher_change)
		await session.commit()
		await session.refresh(teacher_change)
		return teacher_change

	async def get_teacher_change_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherChange))
		return result.scalar()

	async def delete_teacher_change(self, teacher_change: TeacherChange):
		session = await self.master_db()
		await session.delete(teacher_change)
		await session.commit()

	async def get_teacher_change_by_teacher_change_id(self, teacher_change_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherChange).where(TeacherChange.teacher_change_id == teacher_change_id))
		return result.scalar_one_or_none()

	async def query_teacher_change_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherChange)
				
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacher_change(self, teacher_change, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacher_change, *args)
		query = update(TeacherChange).where(TeacherChange.teacher_change_id == teacher_change.teacher_change_id).values(**update_contents)
		return await self.update(session, query, teacher_change, update_contents, is_commit=is_commit)
