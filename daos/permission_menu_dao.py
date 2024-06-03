from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import select, func, update, desc, asc
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.permission_menu import PermissionMenu
from models.role_permissions import RolePermissions
from models.roles import Roles


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
		query = select(PermissionMenu).join(RolePermissions, RolePermissions.menu_id == PermissionMenu.id, isouter=True).order_by(desc(RolePermissions.id)).join(Roles, Roles.id == RolePermissions.role_id,  isouter=True)
		query = query.where(PermissionMenu.is_deleted == False)


		if unit_type:
			query = query.where(Roles.unit_type == unit_type)

		if edu_type:
			query = query.where(Roles.edu_type == edu_type)

		if role_id:
			query = query.where(Roles.id == role_id)

		if system_type:
			query = query.where(Roles.system_type == system_type)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def query_permission_menu_with_args(self,  unit_type, edu_type, system_type, role_id: int = None,parent_id=0):
		query = (select(PermissionMenu.id,
						PermissionMenu.menu_name,
						PermissionMenu.menu_path,
						PermissionMenu.menu_type,
						PermissionMenu.menu_code,
						PermissionMenu.parent_id,
						PermissionMenu.permission_id,
						PermissionMenu.sort_order,
						PermissionMenu.created_at,
						PermissionMenu.updated_at,
						PermissionMenu.created_uid,
						PermissionMenu.updated_uid,
						Roles.app_name
					   ).select_from( PermissionMenu).join(RolePermissions, RolePermissions.menu_id == PermissionMenu.id, isouter=True).join(Roles, Roles.id == RolePermissions.role_id,  isouter=True).order_by(asc(RolePermissions.sort_order)))
		query = query.where(PermissionMenu.is_deleted == False).where(Roles.is_deleted == False)

		if unit_type:
			query = query.where(Roles.unit_type == unit_type)

		if edu_type:
			query = query.where(Roles.edu_type == edu_type)

		if role_id:
			query = query.where(Roles.id == role_id)
		if parent_id:
			query = query.where(PermissionMenu.parent_id == parent_id)
		if system_type:
			query = query.where(Roles.system_type == system_type)

		session = await self.slave_db()
		columns=query.columns.keys()

		result = await session.execute(query)
		# columns=result.keys()
		result_items= result.all()


# 将元组列表转换为字典列表
		dict_result_items = [dict(zip(columns, item)) for item in result_items]

		return dict_result_items



	async def update_permission_menu(self, permission_menu, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(permission_menu, *args)
		query = update(PermissionMenu).where(PermissionMenu.id == permission_menu.id).values(**update_contents)
		return await self.update(session, query, permission_menu, update_contents, is_commit=is_commit)
