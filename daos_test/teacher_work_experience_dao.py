from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_work_experience import TeacherWorkExperience


class TeacherWorkExperienceDAO(DAOBase):

	async def add_teacherworkexperience(self, teacherworkexperience: TeacherWorkExperience):
		session = await self.master_db()
		session.add(teacherworkexperience)
		await session.commit()
		await session.refresh(teacherworkexperience)
		return teacherworkexperience

	async def get_teacherworkexperience_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherWorkExperience))
		return result.scalar()

	async def delete_teacherworkexperience(self, teacherworkexperience: TeacherWorkExperience):
		session = await self.master_db()
		await session.delete(teacherworkexperience)
		await session.commit()

	async def get_teacherworkexperience_by_teacher_work_experience_id(self, teacher_work_experience_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherWorkExperience).where(TeacherWorkExperience.teacher_work_experience_id == teacher_work_experience_id))
		return result.scalar_one_or_none()

	async def query_teacherworkexperience_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherWorkExperience)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherworkexperience(self, teacherworkexperience, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherworkexperience, *args)
		query = update(TeacherWorkExperience).where(TeacherWorkExperience.teacher_work_experience_id == teacherworkexperience.teacher_work_experience_id).values(**update_contents)
		return await self.update(session, query, teacherworkexperience, update_contents, is_commit=is_commit)
