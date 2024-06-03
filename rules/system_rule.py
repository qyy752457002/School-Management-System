# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.system_dao import SubSystemDAO
from models.system import SubSystem
from views.models.system import SubSystem as SubSystemModel

from daos.permission_menu_dao import PermissionMenuDAO
from models.permission_menu import PermissionMenu


# from views.models.system import SubSystemSearchRes

@dataclass_inject
class SystemRule(object):
    permission_menu_dao: PermissionMenuDAO

    async def get_system_by_id(self, system_id):
        system_db = await self.system_dao.get_subsystem_by_id(system_id)
        # 可选 , exclude=[""]
        system = orm_model_to_view_model(system_db, SubSystemModel)
        return system

    async def add_system(self, system: SubSystemModel):
        exists_system = await self.system_dao.get_subsystem_by_name(
            system.system_name)
        if exists_system:
            raise Exception(f"系统{system.system_name}已存在")
        system_db = view_model_to_orm_model(system, SubSystem, exclude=["id"])

        system_db = await self.system_dao.add_subsystem(system_db)
        system = orm_model_to_view_model(system_db, SubSystemModel, exclude=["created_at", 'updated_at'])
        return system

    async def update_system(self, system, ctype=1):
        exists_system = await self.system_dao.get_subsystem_by_id(system.id)
        if not exists_system:
            raise Exception(f"系统{system.id}不存在")
        need_update_list = []
        for key, value in system.dict().items():
            if value:
                need_update_list.append(key)

        system_db = await self.system_dao.update_subsystem(system, *need_update_list)

        # system_db = await self.system_dao.update_system(system_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # system = orm_model_to_view_model(system_db, SubSystemModel, exclude=[""])
        return system_db

    async def softdelete_system(self, system_id):
        exists_system = await self.system_dao.get_subsystem_by_id(system_id)
        if not exists_system:
            raise Exception(f"系统{system_id}不存在")
        system_db = await self.system_dao.delete_subsystem(exists_system)
        # system = orm_model_to_view_model(system_db, SubSystemModel, exclude=[""],)
        return system_db

    async def get_system_count(self):
        return await self.system_dao.get_subsystem_count()

    async def query_system_with_page(self, page_request: PageRequest,unit_type, edu_type, system_type, role_id: int = None, ):
        paging = await self.permission_menu_dao.query_permission_menu_with_page(page_request, unit_type, edu_type, system_type, role_id)
        # 字段映射的示例写法   , {"hash_password": "password"} SubSystemSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, PermissionMenu)
        return paging_result
