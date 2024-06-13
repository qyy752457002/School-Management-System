from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.course import Course
from models.course_school_nature import CourseSchoolNature


class CourseDAO(DAOBase):

	async def add_course(self, course: Course):
		session = await self.master_db()
		session.add(course)
		await session.commit()
		await session.refresh(course)
		return course

	async def get_course_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(Course))
		return result.scalar()

	async def delete_course(self, course: Course):
		session = await self.master_db()
		await session.delete(course)
		await session.commit()

	async def get_course_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Course).where(Course.id == id))
		return result.scalar_one_or_none()


	async def get_course_by_school_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Course).where(Course.school_id == id,Course.is_deleted == False))
		return result.scalar_one_or_none()

	async def query_course_with_page(self,  page_request: PageRequest,**kwargs):
		query = select(Course).select_from(Course).join(CourseSchoolNature, CourseSchoolNature.course_no == Course.course_no,isouter=True).where(Course.is_deleted == False)
		for key, value in kwargs.items():
			query = query.where(getattr(Course, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_course(self, course, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(course, *args)
		query = update(Course).where(Course.id == course.id).values(**update_contents)
		return await self.update(session, query, course, update_contents, is_commit=is_commit)

	async def softdelete_course(self, course):
		session = await self.master_db()
		deleted_status= True
		update_stmt = update(Course).where(Course.id == course.id).values(
			is_deleted= deleted_status,
		)
		await session.execute(update_stmt)
		await session.commit()
		return course

	async def softdelete_course_by_school_id(self, school_id):
		session = await self.master_db()
		deleted_status= True
		update_stmt = update(Course).where(Course.school_id == school_id).values(
			is_deleted= deleted_status,
		)
		await session.execute(update_stmt)
		await session.commit()
		return school_id
	async def softdelete_course_by_district(self, district):
		session = await self.master_db()
		deleted_status= True
		update_stmt = update(Course).where(Course.district == district).values(
			is_deleted= deleted_status,
		)
		await session.execute(update_stmt)
		await session.commit()
		return district
	async def get_course_by_name(self, name,course=None):
		session = await self.slave_db()
		query = select(Course).where(Course.course_name == name)
		if course.city:
			query = query.where(Course.city == course.city)
		if course.district:
			query = query.where(Course.district == course.district)
		result = await session.execute( query)
		return result.scalar_one_or_none()



	async def get_all_course(self,filterdict):
		session = await self.slave_db()
		temodel=select(Course)
		if filterdict:
			for key, value in filterdict.items():
				temodel=temodel.where(getattr(Course, key) == value)
				# result = await session.execute(select(Course).where(getattr(Course, key) == value))
				# return result.scalars().all()
		result = await session.execute(temodel)
		return result.scalars().all()