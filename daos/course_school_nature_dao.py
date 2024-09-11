from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.course_school_nature import CourseSchoolNature


class CourseSchoolNatureDAO(DAOBase):

	async def add_course_school_nature(self, course_school_nature: CourseSchoolNature):
		session = await self.master_db()
		session.add(course_school_nature)
		await session.commit()
		await session.refresh(course_school_nature)
		return course_school_nature

	async def get_course_school_nature_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(CourseSchoolNature))
		return result.scalar()

	async def delete_course_school_nature(self, course_school_nature: CourseSchoolNature):
		session = await self.master_db()
		await session.delete(course_school_nature)
		await session.commit()

	async def get_course_school_nature_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(CourseSchoolNature).where(CourseSchoolNature.id == id))
		return result.scalar_one_or_none()
	async def get_course_school_nature_by_school_nature(self, school_nature):
		session = await self.slave_db()
		result = await session.execute(select(CourseSchoolNature).where(CourseSchoolNature.school_nature == school_nature).where(CourseSchoolNature.is_deleted == False))
		return result.scalars().all()
	async def query_course_school_nature_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(CourseSchoolNature)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_course_school_nature(self, course_school_nature, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(course_school_nature, *args)
		query = update(CourseSchoolNature).where(CourseSchoolNature.id == course_school_nature.id).values(**update_contents)
		return await self.update(session, query, course_school_nature, update_contents, is_commit=is_commit)
