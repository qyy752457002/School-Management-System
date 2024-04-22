from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_professional_titles import TeacherProfessionalTitles


class TeacherProfessionalTitlesDAO(DAOBase):

	async def add_teacherprofessionaltitles(self, teacherprofessionaltitles: TeacherProfessionalTitles):
		session = await self.master_db()
		session.add(teacherprofessionaltitles)
		await session.commit()
		await session.refresh(teacherprofessionaltitles)
		return teacherprofessionaltitles

	async def get_teacherprofessionaltitles_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherProfessionalTitles))
		return result.scalar()

	async def delete_teacherprofessionaltitles(self, teacherprofessionaltitles: TeacherProfessionalTitles):
		session = await self.master_db()
		await session.delete(teacherprofessionaltitles)
		await session.commit()

	async def get_teacherprofessionaltitles_by_teacher_professional_titles_id(self, teacher_professional_titles_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherProfessionalTitles).where(TeacherProfessionalTitles.teacher_professional_titles_id == teacher_professional_titles_id))
		return result.scalar_one_or_none()

	async def query_teacherprofessionaltitles_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherProfessionalTitles)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherprofessionaltitles(self, teacherprofessionaltitles, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherprofessionaltitles, *args)
		query = update(TeacherProfessionalTitles).where(TeacherProfessionalTitles.teacher_professional_titles_id == teacherprofessionaltitles.teacher_professional_titles_id).values(**update_contents)
		return await self.update(session, query, teacherprofessionaltitles, update_contents, is_commit=is_commit)
