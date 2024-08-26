from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.overseas_study import OverseasStudy


class OverseasStudyDAO(DAOBase):

	async def add_overseas_study(self, overseas_study: OverseasStudy):
		session = await self.master_db()
		session.add(overseas_study)
		await session.commit()
		await session.refresh(overseas_study)
		return overseas_study

	async def get_overseas_study_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(OverseasStudy))
		return result.scalar()

	async def delete_overseas_study(self, overseas_study: OverseasStudy):
		session = await self.master_db()
		await session.delete(overseas_study)
		await session.commit()

	async def get_overseas_study_by_overseas_study_id(self, overseas_study_id):
		session = await self.slave_db()
		result = await session.execute(select(OverseasStudy).where(OverseasStudy.overseas_study_id == overseas_study_id))
		return result.scalar_one_or_none()

	async def query_overseas_study_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(OverseasStudy)
		
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_overseas_study(self, overseas_study, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(overseas_study, *args)
		query = update(OverseasStudy).where(OverseasStudy.overseas_study_id == overseas_study.overseas_study_id).values(**update_contents)
		return await self.update(session, query, overseas_study, update_contents, is_commit=is_commit)
