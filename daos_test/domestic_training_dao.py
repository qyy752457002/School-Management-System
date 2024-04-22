from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.domestic_training import DomesticTraining


class DomesticTrainingDAO(DAOBase):

	async def add_domestic_training(self, domestic_training: DomesticTraining):
		session = await self.master_db()
		session.add(domestic_training)
		await session.commit()
		await session.refresh(domestic_training)
		return domestic_training

	async def get_domestic_training_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(DomesticTraining))
		return result.scalar()

	async def delete_domestic_training(self, domestic_training: DomesticTraining):
		session = await self.master_db()
		await session.delete(domestic_training)
		await session.commit()

	async def get_domestic_training_by_domestic_training_id(self, domestic_training_id):
		session = await self.slave_db()
		result = await session.execute(select(DomesticTraining).where(DomesticTraining.domestic_training_id == domestic_training_id))
		return result.scalar_one_or_none()

	async def query_domestic_training_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(DomesticTraining)
		

		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_domestic_training(self, domestic_training, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(domestic_training, *args)
		query = update(DomesticTraining).where(DomesticTraining.domestic_training_id == domestic_training.domestic_training_id).values(**update_contents)
		return await self.update(session, query, domestic_training, update_contents, is_commit=is_commit)
