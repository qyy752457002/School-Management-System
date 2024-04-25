# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.SubSystem_dao import SubSystemDAO
from models.sub_system import SubSystem
from views.models.sub_system import SubSystem as SubSystemModel
# from views.models.sub_system import SubSystemSearchRes

@dataclass_inject
class SubSystemRule(object):
    sub_system_dao: SubSystemDAO

    async def get_sub_system_by_id(self, sub_system_id):
        sub_system_db = await self.sub_system_dao.get_subsystem_by_id(sub_system_id)
        # 可选 , exclude=[""]
        sub_system = orm_model_to_view_model(sub_system_db, SubSystemModel)
        return sub_system

    async def add_sub_system(self, sub_system: SubSystemModel):
        exists_sub_system = await self.sub_system_dao.get_subsystem_by_name(
            sub_system.system_name)
        if exists_sub_system:
            raise Exception(f"系统{sub_system.system_name}已存在")
        sub_system_db = view_model_to_orm_model(sub_system, SubSystem, exclude=["id"])

        sub_system_db = await self.sub_system_dao.add_subsystem(sub_system_db)
        sub_system = orm_model_to_view_model(sub_system_db, SubSystemModel, exclude=["created_at", 'updated_at'])
        return sub_system

    async def update_sub_system(self, sub_system, ctype=1):
        exists_sub_system = await self.sub_system_dao.get_subsystem_by_id(sub_system.id)
        if not exists_sub_system:
            raise Exception(f"系统{sub_system.id}不存在")
        need_update_list = []
        for key, value in sub_system.dict().items():
            if value:
                need_update_list.append(key)

        sub_system_db = await self.sub_system_dao.update_subsystem(sub_system, *need_update_list)

        # sub_system_db = await self.sub_system_dao.update_sub_system(sub_system_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # sub_system = orm_model_to_view_model(sub_system_db, SubSystemModel, exclude=[""])
        return sub_system_db

    async def softdelete_sub_system(self, sub_system_id):
        exists_sub_system = await self.sub_system_dao.get_subsystem_by_id(sub_system_id)
        if not exists_sub_system:
            raise Exception(f"系统{sub_system_id}不存在")
        sub_system_db = await self.sub_system_dao.delete_subsystem(exists_sub_system)
        # sub_system = orm_model_to_view_model(sub_system_db, SubSystemModel, exclude=[""],)
        return sub_system_db

    async def get_sub_system_count(self):
        return await self.sub_system_dao.get_subsystem_count()

    async def query_sub_system_with_page(self, page_request: PageRequest,  ):
        paging = await self.sub_system_dao.query_subsystem_with_page(page_request,  )
        # 字段映射的示例写法   , {"hash_password": "password"} SubSystemSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, SubSystemModel)
        return paging_result
