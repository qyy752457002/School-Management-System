from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.system_config import SystemConfig
from views.models.system import SystemConfig as SystemConfigModel

class SystemConfigDAO(DAOBase):

	async def add_system_config(self, system_config: SystemConfig):
		session = await self.master_db()
		session.add(system_config)
		await session.commit()
		await session.refresh(system_config)
		return system_config

	async def get_system_config_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(SystemConfig))
		return result.scalar()

	async def delete_system_config(self, system_config: SystemConfig):
		session = await self.master_db()
		await session.delete(system_config)
		await session.commit()

	async def get_system_config_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(SystemConfig).where(SystemConfig.id == id))
		return result.scalar_one_or_none()

	async def get_system_config_by_name(self, id,system_config:SystemConfigModel=None):
		session = await self.slave_db()
		query= select(SystemConfig).where(SystemConfig.config_name == id).where(SystemConfig.is_deleted == False)
		if system_config.school_id:
			query=query.where(SystemConfig.school_id == system_config.school_id)
		result = await session.execute(query)
		return result.scalar_one_or_none()
	async def query_system_config_with_page(self,  page_request: PageRequest,config_name,school_id):
		query = select(SystemConfig).where(SystemConfig.is_deleted == False)
		if config_name:
			query = query.where(SystemConfig.config_name == config_name)
		if school_id:
			query = query.where(SystemConfig.school_id == school_id)
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_system_config(self, system_config, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(system_config, *args)
		query = update(SystemConfig).where(SystemConfig.id == system_config.id).values(**update_contents)
		return await self.update(session, query, system_config, update_contents, is_commit=is_commit)
