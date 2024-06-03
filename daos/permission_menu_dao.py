from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.permission_menu import PermissionMenu


class PermissionMenuDAO(DAOBase):

	async def add_permission_menu(self, permission_menu: PermissionMenu):
		session = await self.master_db()
		session.add(permission_menu)
		await session.commit()
		await session.refresh(permission_menu)
		return permission_menu

	async def get_permission_menu_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(PermissionMenu))
		return result.scalar()

	async def delete_permission_menu(self, permission_menu: PermissionMenu):
		session = await self.master_db()
		await session.delete(permission_menu)
		await session.commit()

	async def get_permission_menu_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(PermissionMenu).where(PermissionMenu.id == id))
		return result.scalar_one_or_none()

	async def query_permission_menu_with_page(self,  page_request: PageRequest,unit_type, edu_type, system_type, role_id: int = None,):
		query = select(PermissionMenu)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_permission_menu(self, permission_menu, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(permission_menu, *args)
		query = update(PermissionMenu).where(PermissionMenu.id == permission_menu.id).values(**update_contents)
		return await self.update(session, query, permission_menu, update_contents, is_commit=is_commit)
