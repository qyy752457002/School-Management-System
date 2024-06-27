# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from daos.permission_menu_dao import PermissionMenuDAO
from daos.roles_dao import RolesDAO
from models.permission_menu import PermissionMenu
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule

from views.models.sub_system import SubSystem as SubSystemModel
from views.models.permission_menu import PermissionMenu as PermissionMenuModel

@dataclass_inject
class SystemRule(object):
    permission_menu_dao: PermissionMenuDAO
    roles_dao: RolesDAO
    teacher_work_flow_rule: TeacherWorkFlowRule

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

    async def query_system_with_page(self, page_request: PageRequest,role_id,unit_type, edu_type, system_type,  ):
        paging = await self.permission_menu_dao.query_permission_menu_with_page(page_request, unit_type, edu_type, system_type, role_id)
        # 字段映射的示例写法   , {"hash_password": "password"} SubSystemSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, PermissionMenuModel,other_mapper={
            "menu_name": "power_name",
            "menu_path": "power_url",
            "menu_code": "power_code",
            "menu_type": "power_type",
        })
        title= ''
        if paging_result and hasattr(  paging_result,'items'):
            ids = [ ]
            for item in paging_result.items:
                ids.append(item.id)
                if title == '':
                    role = await self.roles_dao.get_roles_by_id(item.id)
                    title = role.app_name


                # item.children= await self.query_system_with_kwargs(role_id,unit_type, edu_type, system_type,item.id)
                # print(ids,item)


        return paging_result,title

    async def query_system_with_kwargs(self, role_id,unit_type, edu_type, system_type,parent_id ='' ):
        paging = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_type, role_id,parent_id)
        # 字段映射的示例写法   , {"hash_password": "password"} SubSystemSearchRes
        # print(paging)
        # paging_result = PaginatedResponse.from_paging(paging,
        res = dict()
        ids  = [ ]
        title = ''
        for item in paging:
            ids.append(item['id'])
            if title == '':
                title= item['app_name']



            system = orm_model_to_view_model(item, PermissionMenuModel,other_mapper={
                "menu_name": "power_name",
                "menu_path": "power_url",
                "menu_code": "power_code",
                "menu_type": "power_type",
            })
            res[ item['id']] = system
            # res.append(system)
            print(system)
        #     读取二级菜单
        paging2 = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_type, role_id,ids)
        print(paging2,res.keys())
        ids_3  = [ ]

        for item in paging2:
            ids_3.append(item['id'])

            if int(item['parent_id']) in res.keys():

                system = orm_model_to_view_model(item, PermissionMenuModel,other_mapper={
                    "menu_name": "power_name",
                    "menu_path": "power_url",
                    "menu_code": "power_code",
                    "menu_type": "power_type",
                })
                res[int(item['parent_id'])].children.append(system)

        # print(list(paging))
        paging2 = await self.permission_menu_dao.query_permission_menu_with_args( unit_type, edu_type, system_type, role_id,ids_3)
        for _,pm in res.items():
            for item in pm.children:
                print(item.id ,item.children )
                for value in paging2:
                    if int(value['parent_id'])== item.id :

                        system = orm_model_to_view_model(value, PermissionMenuModel,other_mapper={
                            "menu_name": "power_name",
                            "menu_path": "power_url",
                            "menu_code": "power_code",
                            "menu_type": "power_type",
                        })
                        item.children.append(system)

        # print(dict(paging))
        return res,title

    # 通用型 工作流获取方法
    async def query_workflow_with_page(self, query_model, page_request: PageRequest, user_id=None,process_code=None,result_model=None):
        params = {"applicant_name": user_id, "process_code": process_code, }
        paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                      result_model, params)
        return paging
