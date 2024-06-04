from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.roles import Role


class RolesDAO(DAOBase):

	async def add_roles(self, roles: Role):
		session = await self.master_db()
		session.add(roles)
		await session.commit()
		await session.refresh(roles)
		return roles

	async def get_roles_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(Role))
		return result.scalar()

	async def delete_roles(self, roles: Role):
		session = await self.master_db()
		await session.delete(roles)
		await session.commit()

	async def get_roles_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Role).where(Role.id == id))
		return result.scalar_one_or_none()

	async def query_roles_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(Role)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_roles(self, roles, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(roles, *args)
		query = update(Role).where(Role.id == roles.id).values(**update_contents)
		return await self.update(session, query, roles, update_contents, is_commit=is_commit)
