from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.students_key_info_change import StudentKeyInfoChange


class StudentKeyInfoChangeDAO(DAOBase):

	async def add_student_key_info_change(self, student_key_info_change: StudentKeyInfoChange):
		session = await self.master_db()
		session.add(student_key_info_change)
		await session.commit()
		await session.refresh(student_key_info_change)
		return student_key_info_change

	async def get_student_key_info_change_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(StudentKeyInfoChange))
		return result.scalar()

	async def delete_student_key_info_change(self, student_key_info_change: StudentKeyInfoChange):
		session = await self.master_db()
		await session.delete(student_key_info_change)
		await session.commit()

	async def get_student_key_info_change_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(StudentKeyInfoChange).where(StudentKeyInfoChange.id == id))
		return result.scalar_one_or_none()

	async def query_student_key_info_change_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(StudentKeyInfoChange)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_student_key_info_change(self, student_key_info_change, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(student_key_info_change, *args)
		query = update(StudentKeyInfoChange).where(StudentKeyInfoChange.id == student_key_info_change.id).values(**update_contents)
		return await self.update(session, query, student_key_info_change, update_contents, is_commit=is_commit)
