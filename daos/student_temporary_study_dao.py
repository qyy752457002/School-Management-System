from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.student_temporary_study import StudentTemporaryStudy


class StudentTemporaryStudyDAO(DAOBase):

	async def add_student_temporary_study(self, student_temporary_study: StudentTemporaryStudy):
		session = await self.master_db()
		session.add(student_temporary_study)
		await session.commit()
		await session.refresh(student_temporary_study)
		return student_temporary_study

	async def get_student_temporary_study_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(StudentTemporaryStudy))
		return result.scalar()

	async def delete_student_temporary_study(self, student_temporary_study: StudentTemporaryStudy):
		session = await self.master_db()
		await session.delete(student_temporary_study)
		await session.commit()

	async def get_student_temporary_study_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(StudentTemporaryStudy).where(StudentTemporaryStudy.id == id))
		return result.scalar_one_or_none()

	async def query_student_temporary_study_with_page(self,  page_request: PageRequest, **kwargs):
		query = select(StudentTemporaryStudy)
		for key, value in kwargs.items():
			query = query.where(getattr(StudentTemporaryStudy, key) == value)
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_student_temporary_study(self, student_temporary_study, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(student_temporary_study, *args)
		query = update(StudentTemporaryStudy).where(StudentTemporaryStudy.id == student_temporary_study.id).values(**update_contents)
		return await self.update(session, query, student_temporary_study, update_contents, is_commit=is_commit)
	async def get_student_temporary_study_by_args(self, **kwargs):
		session = await self.slave_db()
		query = select(StudentTemporaryStudy)
		for key, value in kwargs.items():
			query = query.where(getattr(StudentTemporaryStudy, key) == value)
		result = await session.execute(query)
		return result.scalar()