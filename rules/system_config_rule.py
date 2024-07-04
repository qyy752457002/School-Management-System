from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from daos.system_config_dao import SystemConfigDAO
from models.system_config import SystemConfig

from views.models.system import SystemConfig as SystemConfigModel

@dataclass_inject
class SystemConfigRule(object):
    system_config_dao: SystemConfigDAO

    async def get_system_config_by_id(self, system_config_id):
        system_config_db = await self.system_config_dao.get_system_config_by_id(system_config_id)
        # 可选 , exclude=[""]
        system_config = orm_model_to_view_model(system_config_db, SystemConfigModel)
        return system_config

    async def add_system_config(self, system_config: SystemConfigModel):
        exists_system_config = await self.system_config_dao.get_system_config_by_name(
            system_config.config_name,system_config)
        if exists_system_config:
            raise Exception(f"系统{system_config.config_name}已存在")
        system_config_db = view_model_to_orm_model(system_config, SystemConfig, exclude=["id"])
        system_config_db.id = 0
        system_config_db.id  = SnowflakeIdGenerator(1, 1).generate_id()

        system_config_db = await self.system_config_dao.add_system_config(system_config_db)
        system_config = orm_model_to_view_model(system_config_db, SystemConfigModel, exclude=["created_at", 'updated_at'])
        return system_config

    async def update_system_config(self, system_config, ):
        exists_system_config = await self.system_config_dao.get_system_config_by_id(system_config.id)
        if not exists_system_config:
            raise Exception(f"系统{system_config.id}不存在")
        need_update_list = []
        for key, value in system_config.dict().items():
            if value:
                need_update_list.append(key)

        system_config_db = await self.system_config_dao.update_system_config(system_config, *need_update_list)

        # system_config_db = await self.system_config_dao.update_system_config(system_config_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # system_config = orm_model_to_view_model(system_config_db, SystemConfigModel, exclude=[""])
        return system_config_db

    async def softdelete_system_config(self, system_config_id):
        exists_system_config = await self.system_config_dao.get_system_config_by_id(system_config_id)
        if not exists_system_config:
            raise Exception(f"系统{system_config_id}不存在")
        system_config_db = await self.system_config_dao.delete_system_config(exists_system_config)
        # system_config = orm_model_to_view_model(system_config_db, SystemConfigModel, exclude=[""],)
        return system_config_db

    async def get_system_config_count(self):
        return await self.system_config_dao.get_system_config_count()

    async def query_system_config_with_page(self,config_name, school_id,page_request: PageRequest,   ):
        paging = await self.system_config_dao.query_system_config_with_page(page_request, config_name,school_id )
        # 字段映射的示例写法   , {"hash_password": "password"} SystemConfigSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, SystemConfigModel,other_mapper={

        })
        title= ''
        return paging_result

    async def query_system_config_with_kwargs(self, role_id,unit_type, edu_type, system_config_type,parent_id ='' ):
        paging = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_config_type, role_id,parent_id)
        # 字段映射的示例写法   , {"hash_password": "password"} SystemConfigSearchRes
        # print(paging)
        # paging_result = PaginatedResponse.from_paging(paging,
        res = dict()
        ids  = [ ]
        title = ''
        for item in paging:
            ids.append(item['id'])
            if title == '':
                title= item['app_name']



            system_config = orm_model_to_view_model(item, PermissionMenuModel,other_mapper={
                "menu_name": "power_name",
                "menu_path": "power_url",
                "menu_code": "power_code",
                "menu_type": "power_type",
            })
            res[ item['id']] = system_config
            # res.append(system_config)
            print(system_config)
        #     读取二级菜单
        paging2 = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_config_type, role_id,ids)
        print(paging2,res.keys())
        ids_3  = [ ]

        for item in paging2:
            ids_3.append(item['id'])

            if int(item['parent_id']) in res.keys():

                system_config = orm_model_to_view_model(item, PermissionMenuModel,other_mapper={
                    "menu_name": "power_name",
                    "menu_path": "power_url",
                    "menu_code": "power_code",
                    "menu_type": "power_type",
                })
                res[int(item['parent_id'])].children.append(system_config)

        # print(list(paging))
        paging2 = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_config_type, role_id,ids_3)
        for _,pm in res.items():
            for item in pm.children:
                print(item.id ,item.children )
                for value in paging2:
                    if int(value['parent_id'])== item.id :

                        system_config = orm_model_to_view_model(value, PermissionMenuModel,other_mapper={
                            "menu_name": "power_name",
                            "menu_path": "power_url",
                            "menu_code": "power_code",
                            "menu_type": "power_type",
                        })
                        item.children.append(system_config)

        # print(dict(paging))
        return res,title
