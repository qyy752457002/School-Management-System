from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.sub_system import SubSystem


class SubSystemDAO(DAOBase):

	async def add_subsystem(self, subsystem: SubSystem):
		session = await self.master_db()
		session.add(subsystem)
		await session.commit()
		await session.refresh(subsystem)
		return subsystem

	async def get_subsystem_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(SubSystem))
		return result.scalar()

	async def delete_subsystem(self, subsystem: SubSystem):
		session = await self.master_db()
		await session.delete(subsystem)
		await session.commit()

	async def get_subsystem_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(SubSystem).where(SubSystem.id ==int(id) ))
		return result.scalar_one_or_none()

	async def get_subsystem_by_name(self, id):
		session = await self.slave_db()
		result = await session.execute(select(SubSystem).where(SubSystem.system_name ==int(id) ))
		return result.scalar_one_or_none()

	async def query_subsystem_with_page(self, page_request: PageRequest, **kwargs):
		query = select(SubSystem)
		for key, value in kwargs.items():
		   query = query.where(getattr(SubSystem, key) == value)
		paging = await self.query_page(query, page_request)
		return paging

	async def update_subsystem(self, subsystem, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(subsystem, *args)
		query = update(SubSystem).where(SubSystem.id ==int(subsystem.id) ).values(**update_contents)
		return await self.update(session, query, subsystem, update_contents, is_commit=is_commit)
