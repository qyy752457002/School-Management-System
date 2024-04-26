from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.class_division_records import ClassDivisionRecords


class ClassDivisionRecordsDAO(DAOBase):

	async def add_class_division_records(self, class_division_records: ClassDivisionRecords):
		session = await self.master_db()
		session.add(class_division_records)
		await session.commit()
		await session.refresh(class_division_records)
		return class_division_records

	async def get_class_division_records_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(ClassDivisionRecords))
		return result.scalar()

	async def delete_class_division_records(self, class_division_records: ClassDivisionRecords):
		session = await self.master_db()
		await session.delete(class_division_records)
		await session.commit()

	async def get_class_division_records_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(ClassDivisionRecords).where(ClassDivisionRecords.id == id))
		return result.scalar_one_or_none()

	async def query_class_division_records_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(ClassDivisionRecords)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_class_division_records(self, class_division_records, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(class_division_records, *args)
		query = update(ClassDivisionRecords).where(ClassDivisionRecords.id == class_division_records.id).values(**update_contents)
		return await self.update(session, query, class_division_records, update_contents, is_commit=is_commit)
