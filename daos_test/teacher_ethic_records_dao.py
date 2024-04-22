from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_ethic_records import TeacherEthicRecords


class TeacherEthicRecordsDAO(DAOBase):

	async def add_teacherethicrecords(self, teacherethicrecords: TeacherEthicRecords):
		session = await self.master_db()
		session.add(teacherethicrecords)
		await session.commit()
		await session.refresh(teacherethicrecords)
		return teacherethicrecords

	async def get_teacherethicrecords_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherEthicRecords))
		return result.scalar()

	async def delete_teacherethicrecords(self, teacherethicrecords: TeacherEthicRecords):
		session = await self.master_db()
		await session.delete(teacherethicrecords)
		await session.commit()

	async def get_teacherethicrecords_by_teacher_ethic_records_id(self, teacher_ethic_records_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherEthicRecords).where(TeacherEthicRecords.teacher_ethic_records_id == teacher_ethic_records_id))
		return result.scalar_one_or_none()

	async def query_teacherethicrecords_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherEthicRecords)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherethicrecords(self, teacherethicrecords, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherethicrecords, *args)
		query = update(TeacherEthicRecords).where(TeacherEthicRecords.teacher_ethic_records_id == teacherethicrecords.teacher_ethic_records_id).values(**update_contents)
		return await self.update(session, query, teacherethicrecords, update_contents, is_commit=is_commit)
