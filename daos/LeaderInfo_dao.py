from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.leader_info import LeaderInfo


class LeaderInfoDAO(DAOBase):

	async def add_leaderinfo(self, leaderinfo: LeaderInfo):
		session = await self.master_db()
		session.add(leaderinfo)
		await session.commit()
		await session.refresh(leaderinfo)
		return leaderinfo

	async def get_leaderinfo_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(LeaderInfo))
		return result.scalar()

	async def delete_leaderinfo(self, leaderinfo: LeaderInfo):
		session = await self.master_db()
		await session.delete(leaderinfo)
		await session.commit()

	async def get_leaderinfo_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(LeaderInfo).where(LeaderInfo.id == id))
		return result.scalar_one_or_none()

	async def query_leaderinfo_with_page(self,  page_request: PageRequest,**kwargs):
		query = select(LeaderInfo)
		for key, value in kwargs.items():
		   query = query.where(getattr(LeaderInfo, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_leaderinfo(self, leaderinfo, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(leaderinfo, *args)
		query = update(LeaderInfo).where(LeaderInfo.id == leaderinfo.id).values(**update_contents)
		return await self.update(session, query, leaderinfo, update_contents, is_commit=is_commit)
