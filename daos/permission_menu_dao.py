from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import select, func, update, desc, asc
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.permission_menu import PermissionMenu
from models.role_permission import RolePermission
from models.role import Role


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
        result = await session.execute(select(PermissionMenu).where(PermissionMenu.id == int(id)))
        return result.scalar_one_or_none()

    async def query_permission_menu_with_page(self, page_request: PageRequest, unit_type, edu_type, system_type,
                                              role_id: int = None, ):
        query = select(PermissionMenu).join(RolePermission, RolePermission.menu_id == PermissionMenu.id,
                                            isouter=True).order_by(desc(RolePermission.id)).join(Role,
                                                                                                 Role.id == RolePermission.role_id,
                                                                                                 isouter=True)
        query = query.where(PermissionMenu.is_deleted == False)

        if unit_type:
            query = query.where(Role.unit_type == unit_type)
        if edu_type:
            query = query.where(Role.edu_type == edu_type)
        if role_id:
            query = query.where(Role.id == role_id)
        if system_type:
            query = query.where(Role.system_type == system_type)
        paging = await self.query_page(query, page_request)
        return paging

    async def query_permission_menu_with_args(self, unit_type, edu_type, system_type, role_id: int = None, parent_id=0,resouce_codes='',filter = None):
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
                        PermissionMenu.resource_code,
                        PermissionMenu.action,
                        PermissionMenu.updated_uid,
                        Role.app_name
                        ).select_from(PermissionMenu).join(RolePermission, RolePermission.menu_id == PermissionMenu.id,
                                                           isouter=True).join(Role, Role.id == RolePermission.role_id,
                                                                              isouter=True).order_by(
            asc(RolePermission.sort_order)).order_by(asc(PermissionMenu.sort_order)).order_by(asc(RolePermission.id)))
        query = query.where(PermissionMenu.is_deleted == False).where(Role.is_deleted == False).where(
            RolePermission.is_deleted == False)
        if filter and len(filter) >0:
            # 不在filter里面
            query = query.where(PermissionMenu.id.not_in(filter))
            # query = query.where(PermissionMenu.id == int(role_id))
        if unit_type:
            query = query.where(Role.unit_type == unit_type)

        if edu_type:
            query = query.where(Role.edu_type == edu_type)

        if role_id:
            query = query.where(Role.id == int(role_id))
        if parent_id:
            if isinstance(parent_id, list):
                query = query.where(PermissionMenu.parent_id.in_(parent_id))
                pass
            else:
                query = query.where(PermissionMenu.parent_id == int(parent_id))
                pass
        else:
            query = query.where(PermissionMenu.parent_id == 0)
        if resouce_codes:
            if isinstance(resouce_codes, list):
                # 针对list 去重
                resouce_codes = list(set(resouce_codes))
                query = query.where(PermissionMenu.resource_code.in_(resouce_codes))
                pass
            else:
                query = query.where(PermissionMenu.resource_code ==   resouce_codes )
                pass
        if system_type:
            query = query.where(Role.system_type == system_type)
        session = await self.slave_db()
        columns = query.columns.keys()
        result = await session.execute(query)
        result_items = result.all()
        # 将元组列表转换为字典列表
        dict_result_items = [dict(zip(columns, item)) for item in result_items]
        return dict_result_items

    async def update_permission_menu(self, permission_menu, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(permission_menu, *args)
        query = update(PermissionMenu).where(PermissionMenu.id == permission_menu.id).values(**update_contents)
        return await self.update(session, query, permission_menu, update_contents, is_commit=is_commit)
