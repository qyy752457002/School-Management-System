from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.subject import Subject
from views.models.subject import Subject  as SubjectModel




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
		await self.delete(session,subject)
		await session.commit()
		return subject

	async def get_subject_by_id(self, id,use_master=False):
		if use_master:
			session = await self.master_db()
		else:
			session = await self.slave_db()
		result = await session.execute(select(Subject).where(Subject.id == int(id)))
		return result.scalar_one_or_none()
	async def get_subject_by_param(self, subject: SubjectModel):
		session = await self.slave_db()
		query = select(Subject).where(Subject.is_deleted == False)
		if subject.id:
			query = query.where(Subject.id == int(subject.id))

		if subject.subject_name:
			query = query.where(Subject.subject_name == subject.subject_name)
		if subject.course_no:
			query = query.where(Subject.course_no == subject.course_no)
		if subject.school_id:
			query = query.where(Subject.school_id ==int(subject.school_id) )
		if subject.grade_id:
			query = query.where(Subject.grade_id == int(subject.grade_id))


		result = await session.execute( query)
		return result.scalar_one_or_none()
	async def query_subject_with_page(self,  page_request: PageRequest , school_id=None,subject_name=None,city=None,district=None):
		query = select(Subject).where(Subject.is_deleted == False)
		
		### �˴���д��ѯ����
		if school_id:
			query = query.where(Subject.school_id == int(school_id))
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_subject(self, subject, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(subject, *args)
		query = update(Subject).where(Subject.id ==int(subject.id) ).values(**update_contents)
		return await self.update(session, query, subject, update_contents, is_commit=is_commit)
