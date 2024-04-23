from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.leader_info import LeaderInfo


class LeaderInfoDAO(DAOBase):

	async def add_leader_info(self, leader_info: LeaderInfo):
		session = await self.master_db()
		session.add(leader_info)
		await session.commit()
		await session.refresh(leader_info)
		return leader_info

	async def get_leader_info_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(LeaderInfo))
		return result.scalar()

	async def delete_leader_info(self, leader_info: LeaderInfo):
		session = await self.master_db()
		await session.delete(leader_info)
		await session.commit()

	async def get_leader_info_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(LeaderInfo).where(LeaderInfo.id == id))
		return result.scalar_one_or_none()

	async def get_leader_info_by_leader_info_name(self, id):
		session = await self.slave_db()
		result = await session.execute(select(LeaderInfo).where(LeaderInfo.leader_name == id))
		return result.scalar_one_or_none()

	async def query_leader_info_with_page(self,  page_request: PageRequest,**kwargs):
		query = select(LeaderInfo)
		for key, value in kwargs.items():
		   query = query.where(getattr(LeaderInfo, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_leader_info(self, leader_info, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(leader_info, *args)
		query = update(LeaderInfo).where(LeaderInfo.id == leader_info.id).values(**update_contents)
		return await self.update(session, query, leader_info, update_contents, is_commit=is_commit)


	async def update_leader_info_byargs(self, leader_info: LeaderInfo, *args, is_commit: bool = True):
		session = await self.master_db()
		update_contents = get_update_contents(leader_info, *args)
		query = update(LeaderInfo).where(LeaderInfo.id == leader_info.id).values(**update_contents)
		return await self.update(session, query, leader_info, update_contents, is_commit=is_commit)

	async def softdelete_leader_info(self, exists_leader_info):
		session = await self.master_db()
		deleted_status= 1
		update_stmt = update(LeaderInfo).where(LeaderInfo.id == exists_leader_info.id).values(
			is_deleted= deleted_status,
		)
		await session.execute(update_stmt)
		# await session.delete(leader_info)
		await session.commit()
		return exists_leader_info