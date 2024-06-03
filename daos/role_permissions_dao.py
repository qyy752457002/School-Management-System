from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.role_permissions import RolePermissions


class RolePermissionsDAO(DAOBase):

	async def add_rolepermissions(self, rolepermissions: RolePermissions):
		session = await self.master_db()
		session.add(rolepermissions)
		await session.commit()
		await session.refresh(rolepermissions)
		return rolepermissions

	async def get_rolepermissions_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(RolePermissions))
		return result.scalar()

	async def delete_rolepermissions(self, rolepermissions: RolePermissions):
		session = await self.master_db()
		await session.delete(rolepermissions)
		await session.commit()

	async def get_rolepermissions_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(RolePermissions).where(RolePermissions.id == id))
		return result.scalar_one_or_none()

	async def query_rolepermissions_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(RolePermissions)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_rolepermissions(self, rolepermissions, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(rolepermissions, *args)
		query = update(RolePermissions).where(RolePermissions.id == rolepermissions.id).values(**update_contents)
		return await self.update(session, query, rolepermissions, update_contents, is_commit=is_commit)
