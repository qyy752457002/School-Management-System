from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_qualifications import TeacherQualifications


class TeacherQualificationsDAO(DAOBase):

	async def add_teacherqualifications(self, teacherqualifications: TeacherQualifications):
		session = await self.master_db()
		session.add(teacherqualifications)
		await session.commit()
		await session.refresh(teacherqualifications)
		return teacherqualifications

	async def get_teacherqualifications_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherQualifications))
		return result.scalar()

	async def delete_teacherqualifications(self, teacherqualifications: TeacherQualifications):
		session = await self.master_db()
		await session.delete(teacherqualifications)
		await session.commit()

	async def get_teacherqualifications_by_teacher_qualifications_id(self, teacher_qualifications_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherQualifications).where(TeacherQualifications.teacher_qualifications_id == teacher_qualifications_id))
		return result.scalar_one_or_none()

	async def query_teacherqualifications_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherQualifications)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherqualifications(self, teacherqualifications, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherqualifications, *args)
		query = update(TeacherQualifications).where(TeacherQualifications.teacher_qualifications_id == teacherqualifications.teacher_qualifications_id).values(**update_contents)
		return await self.update(session, query, teacherqualifications, update_contents, is_commit=is_commit)
