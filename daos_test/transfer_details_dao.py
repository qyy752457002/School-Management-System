from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.transfer_details import TransferDetails


class TransferDetailsDAO(DAOBase):

	async def add_transferdetails(self, transferdetails: TransferDetails):
		session = await self.master_db()
		session.add(transferdetails)
		await session.commit()
		await session.refresh(transferdetails)
		return transferdetails

	async def get_transferdetails_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TransferDetails))
		return result.scalar()

	async def delete_transferdetails(self, transferdetails: TransferDetails):
		session = await self.master_db()
		await session.delete(transferdetails)
		await session.commit()

	async def get_transferdetails_by_transfer_details_id(self, transfer_details_id):
		session = await self.slave_db()
		result = await session.execute(select(TransferDetails).where(TransferDetails.transfer_details_id == transfer_details_id))
		return result.scalar_one_or_none()

	async def query_transferdetails_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TransferDetails)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_transferdetails(self, transferdetails, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(transferdetails, *args)
		query = update(TransferDetails).where(TransferDetails.transfer_details_id == transferdetails.transfer_details_id).values(**update_contents)
		return await self.update(session, query, transferdetails, update_contents, is_commit=is_commit)
