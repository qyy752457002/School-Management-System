# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import pprint
import traceback
from urllib.parse import urlencode

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.storage.view_model import FileStorageModel
from mini_framework.utils.http import HTTPRequest
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from daos.permission_menu_dao import PermissionMenuDAO
from daos.roles_dao import RolesDAO
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from rules.common.common_rule import process_userinfo, filter_action_by_file_name, read_file_to_permission_dict
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from views.common.common_view import workflow_service_config, convert_snowid_in_model, system_config
from views.models.permission_menu import PermissionMenu as PermissionMenuModel
from views.models.sub_system import SubSystem as SubSystemModel
from views.models.system import PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
from daos.sub_system_dao import SubSystemDAO
from models.sub_system import SubSystem


@dataclass_inject
class SystemRule(object):
    permission_menu_dao: PermissionMenuDAO
    roles_dao: RolesDAO
    teacher_work_flow_rule: TeacherWorkFlowRule
    file_storage_dao: FileStorageDAO
    system_dao: SubSystemDAO

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

    async def query_system_with_page(self, page_request: PageRequest, role_id, unit_type, edu_type, system_type, ):
        paging = await self.permission_menu_dao.query_permission_menu_with_page(page_request, unit_type, edu_type,
                                                                                system_type, role_id)
        # 字段映射的示例写法   , {"hash_password": "password"} SubSystemSearchRes
        # print(paging)
        paging_result = PaginatedResponse.from_paging(paging, PermissionMenuModel, other_mapper={
            "menu_name": "power_name",
            "menu_path": "power_url",
            "menu_code": "power_code",
            "menu_type": "power_type",
        })
        title = ''
        if paging_result and hasattr(paging_result, 'items'):
            ids = []
            for item in paging_result.items:
                ids.append(item.id)
                if title == '':
                    role = await self.roles_dao.get_roles_by_id(item.id)
                    title = role.app_name
        return paging_result, title

    async def query_system_with_kwargs(self, role_id, unit_type, edu_type, system_type, parent_id='',resource_codes='',extend_params=None ):
        paging = await self.permission_menu_dao.query_permission_menu_with_args(unit_type, edu_type, system_type,
                                                                                role_id, parent_id)
        # 校验已配置的权限
        filter = [ ]

        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao=get_injector(TenantDAO)
            school_dao=get_injector(SchoolDAO)
            tenant =  await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)
            print(333,tenant)

            if  tenant is   not None and  len(tenant.code) == 6 :
                filter = [39 ]

            pass
        file_name=None
        processed_dict={}
        is_permission_verify = system_config.system_config.get("permission_verify")
        if   is_permission_verify:
            # 获取权限一次
            account = request_context_manager.current().current_login_account
            account_name = account.name
            print('开始菜单的权限过滤方法 --')

            file_name = await process_userinfo(account_name)
            with open(file_name, 'r') as file:
            # 读取文件的全部内容
                file_content = file.read()
            processed_dict = read_file_to_permission_dict(file_content)
            pass

        res = dict()
        ids = []
        title = ''
        for item in paging:
            ids.append(item['id'])
            if title == '':
                title = item['app_name']
            # 判断如果action里有汉字的顿号 则提换为英文的逗号
            if item['action'] and '、' in item['action']:
                item['action'] = item['action'].replace('、', ',')
            await filter_action_by_file_name(item,processed_dict)

            system = orm_model_to_view_model(item, PermissionMenuModel, other_mapper={
                "menu_name": "power_name",
                "menu_path": "power_url",
                "menu_code": "power_code",
                "menu_type": "power_type",
            })
            res[item['id']] = system
            # res.append(system)
            print(system)
        #     读取二级菜单
        paging2 = await self.permission_menu_dao.query_permission_menu_with_args(unit_type, edu_type, system_type,
                                                                                 role_id, ids,filter=filter)
        print(paging2, res.keys())
        ids_3 = []

        for item in paging2:
            ids_3.append(item['id'])

            if int(item['parent_id']) in res.keys():
                # 判断如果action里有汉字的顿号 则提换为英文的逗号
                if item['action'] and '、' in item['action']:
                    item['action'] = item['action'].replace('、', ',')
                await filter_action_by_file_name(item,processed_dict)

                system = orm_model_to_view_model(item, PermissionMenuModel, other_mapper={
                    "menu_name": "power_name",
                    "menu_path": "power_url",
                    "menu_code": "power_code",
                    "menu_type": "power_type",
                })
                convert_snowid_in_model(system,["id",'permission_id'])

                res[int(item['parent_id'])].children.append(system)

        # print(list(paging))
        # 三级次啊单
        paging3 = await self.permission_menu_dao.query_permission_menu_with_args(unit_type, edu_type, system_type,
                                                                                 role_id, ids_3,resource_codes)
        for _, pm in res.items():
            for item in pm.children:
                print(item.id, item.children)
                for value in paging3:
                    if int(value['parent_id']) == int(item.id):
                        if value['action'] and '、' in value['action']:
                            value['action'] = value['action'].replace('、', ',')
                        await filter_action_by_file_name(value,processed_dict)

                        system = orm_model_to_view_model(value, PermissionMenuModel, other_mapper={
                            "menu_name": "power_name",
                            "menu_path": "power_url",
                            "menu_code": "power_code",
                            "menu_type": "power_type",
                        })
                        convert_snowid_in_model(system,["id",'permission_id'])

                        item.children.append(system)

        # print(dict(paging))
        return res, title

    # 通用型 工作流获取方法
    async def query_workflow_with_page(self, query_model, page_request: PageRequest, user_id=None, process_code=None,
                                       result_model=None,extend_params=None):
        params = {"applicant_name": user_id, "process_code": process_code, }
        # params= {**params,**query_model.dict()}
        print('params--', params)
        paging = None
        try:
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          result_model, params)
            # 针对如果是 关闭的 审核列表  遍历处理里面的 每个图片信息 取获取转换一个URL附上
            sortlist = []
            if paging and hasattr(paging, 'items'):
                for item in paging.items:
                    sortlist.append(item['start_time'])
                    if process_code == PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE or process_code == SCHOOL_CLOSE_WORKFLOW_CODE or process_code == INSTITUTION_CLOSE_WORKFLOW_CODE:
                        if isinstance(item, dict)  :

                            item['related_license_upload_url']=None
                            if 'related_license_upload' in item.keys() and item['related_license_upload'] and  len(item['related_license_upload'])>0:
                                print('item', item['related_license_upload'])
                                # 针对有可能是多张图片的处理
                                if isinstance(item['related_license_upload'], list):
                                    item['related_license_upload_url']= [ ]
                                    for i in range(len(item['related_license_upload'])):
                                        tempurl = await self.get_download_url_by_id(item['related_license_upload'][i])
                                        item['related_license_upload_url'].append( tempurl )
                                    # item['related_license_upload'] = item['related_license_upload'][0]
                                else:

                                    item['related_license_upload_url'] = await self.get_download_url_by_id(
                                    item['related_license_upload'])
                        elif isinstance(item, object) :
                            item.related_license_upload_url = None
                            if   item.related_license_upload:
                                item.related_license_upload_url = await self.get_download_url_by_id(
                                item.related_license_upload)

                    elif process_code == SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE :
                        print('学校关闭的流程 处理3个ID为str', )
                        if isinstance(item, dict)  :
                            if 'id' in item:
                                item['id']= str(item['id'])
                            if 'planning_school_id' in item:
                                item['planning_school_id']= str(item['planning_school_id'])
                            if 'school_id' in item:
                                item['school_id']= str(item['school_id'])
                            print('处理字典',item)
                    else :
                        print('非关闭的流程', )

            print('排序 ',sortlist)
            return paging
        except Exception as e:
            print('异常', e, )
            traceback.print_exc()
            # return None
            return e

        # return paging

    async def get_work_flow_instance_by_process_instance_id(self, process_instance_id: int):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance-by-process-instance-id'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.get_json(url, headerdict)
        # result = JsonUtils.json_str_to_dict(result)
        return result

    async def get_work_flow_current_node_by_process_instance_id(self, process_instance_id):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/current-node-by-process-instance-id'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.get_json(url, headerdict)
        return result

    # 根据ID获取下载地址的方法
    async def get_download_url_by_id(self, id):

        url = ''
        if id and id.isnumeric():
            fileinfo = await self.file_storage_dao.get_file_by_id(int(id))
            if fileinfo:
                # 获取行的数据
                fileinfo = fileinfo._asdict()['FileStorage']
                print(fileinfo)  # 使用 _asdict() 方法转换为字典
                if hasattr(fileinfo, 'file_name'):

                    file_storage = FileStorageModel(file_name=fileinfo.file_name, virtual_bucket_name=fileinfo.virtual_bucket_name,
                                                    file_size=fileinfo.file_size, )
                    try:
                        url = storage_manager.query_get_object_url_with_token(file_storage)
                        print('获取的结果', url)
                    except Exception as e:
                        print('error', e)
                        if hasattr(e, 'user_message'):
                            id = e.user_message

                        return url

                        pass
                    pprint.pprint(id)

            else:
                print('文件not found ')
                pass

        return url
