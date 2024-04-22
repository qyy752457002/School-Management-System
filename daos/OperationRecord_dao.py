from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.operation_record import OperationRecord


class OperationRecordDAO(DAOBase):

	async def add_operationrecord(self, operationrecord: OperationRecord):
		session = await self.master_db()
		session.add(operationrecord)
		await session.commit()
		await session.refresh(operationrecord)
		return operationrecord

	async def get_operationrecord_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(OperationRecord))
		return result.scalar()

	async def delete_operationrecord(self, operationrecord: OperationRecord):
		session = await self.master_db()
		await session.delete(operationrecord)
		await session.commit()

	async def get_operationrecord_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(OperationRecord).where(OperationRecord.id == id))
		return result.scalar_one_or_none()

	async def query_operationrecord_with_page(self,  page_request: PageRequest,**kwargs):
		query = select(OperationRecord)
		for key, value in kwargs.items():
		   query = query.where(getattr(OperationRecord, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_operationrecord(self, operationrecord, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(operationrecord, *args)
		query = update(OperationRecord).where(OperationRecord.id == operationrecord.id).values(**update_contents)
		return await self.update(session, query, operationrecord, update_contents, is_commit=is_commit)
