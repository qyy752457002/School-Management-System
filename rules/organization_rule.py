import copy
from datetime import date, datetime

import shortuuid
from mini_framework.authentication.config import authentication_config
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from pydantic import BaseModel
from sqlalchemy import select

from business_exceptions.organization import OrganizationNotFoundError, OrganizationExistError
from daos.organization_dao import OrganizationDAO
from daos.school_dao import SchoolDAO
from models.organization import Organization as OrganizationModel
from rules.common.common_rule import send_orgcenter_request
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model, convert_dates_to_strings
from views.models.organization import Organization
from views.models.planning_school import PlanningSchoolStatus


@dataclass_inject
class OrganizationRule(object):
    organization_dao: OrganizationDAO
    school_dao: SchoolDAO

    async def get_organization_by_id(self, organization_id, extra_model=None):
        organization_db = await self.organization_dao.get_organization_by_id(organization_id)
        # 可选 , exclude=[""]
        if extra_model:
            # school = orm_model_to_view_model(school_db, extra_model)
            organization = orm_model_to_view_model(organization_db, extra_model)

        else:
            organization = orm_model_to_view_model(organization_db, Organization)
        return organization

    async def get_organization_by_organization_name(self, organization_name):
        organization_db = await self.organization_dao.get_organization_by_organization_name(
            organization_name)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization

    async def add_organization(self, organization: Organization):
        exists_organization = await self.organization_dao.get_organization_by_name(
            organization.org_name, organization)
        if exists_organization:
            raise OrganizationExistError()
        organization_db = view_model_to_orm_model(organization, OrganizationModel, exclude=["id"])
        # school_db.status =  PlanningSchoolStatus.DRAFT.value
        # 只有2步  故新增几位开设中 
        organization_db.created_uid = 0
        organization_db.updated_uid = 0
        organization_db.org_code = shortuuid.uuid()
        organization_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        organization_db = await self.organization_dao.add_organization(organization_db)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=["created_at", ])
        convert_snowid_in_model(organization, ["id", "school_id", 'parent_id', ])
        # todo 发送组织中心
        try:
            await self.send_org_to_org_center(organization)
        except Exception as e:
            print("发送组织中心失败", e)
        return organization

    async def update_organization(self, organization, ):
        # 默认 改
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise OrganizationNotFoundError()
        organization_db = view_model_to_orm_model(organization, OrganizationModel, exclude=[])
        need_update_list = []
        # 自动判断哪些字段需要更新
        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)

        organization_db = await self.organization_dao.update_organization(organization_db, *need_update_list)
        print(organization_db, 999)
        convert_snowid_in_model(organization_db, ["id", "school_id", 'parent_id', ])

        return organization_db

    async def update_organization_byargs(self, organization, ctype=1):
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise OrganizationNotFoundError()
        need_update_list = []

        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)

        organization_db = await self.organization_dao.update_organization_byargs(organization, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization_db

    async def delete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id, True)
        if not exists_organization:
            raise OrganizationNotFoundError()
        top_id = exists_organization.parent_id
        organization_db = await self.organization_dao.delete_organization(exists_organization)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=[""], )
        # 查询下层的部门
        if organization_id:
            parent_id_lv2 = await self.organization_dao.get_child_organization_ids([organization_id])
            parent_id_lv3 = await self.organization_dao.get_child_organization_ids(parent_id_lv2)
            await self.organization_dao.delete_organization_by_ids(parent_id_lv3 + parent_id_lv2)
            # organization_db = await self.organization_dao.softdelete_organization(exists_organization)
            pass
        convert_snowid_in_model(organization, ["id", "school_id", 'parent_id', ])

        return organization

    async def softdelete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"{organization_id}不存在")
        organization_db = await self.organization_dao.softdelete_organization(exists_organization)
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""],)
        return organization_db

    async def get_all_organizations(self):
        return await self.organization_dao.get_all_organizations()

    async def get_organization_count(self):
        return await self.organization_dao.get_organization_count()

    async def query_organization_with_page(self, page_request: PageRequest, parent_id, school_id):
        parent_id_lv2 = []
        if parent_id:
            if int(parent_id) > 0:
                parent_id_lv2.append(int(parent_id))
                #
                # # todo  参照 举办者类型   自动查出 23 级
                # res= await self.query_organization( parent_id)
                # for item in res:
                #     parent_id_lv2.append(item.id)
                #
                # pass
            else:
                parent_id_lv2.append(int(parent_id))

        paging = await self.organization_dao.query_organization_with_page(page_request, parent_id_lv2, school_id
                                                                          )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, Organization)
        convert_snowid_to_strings(paging_result, ["id", "school_id", 'parent_id'])
        return paging_result

    async def update_organization_status(self, organization_id, status, action=None):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"学校{organization_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status == PlanningSchoolStatus.NORMAL.value and exists_organization.status == PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_organization.status = PlanningSchoolStatus.NORMAL.value
        elif status == PlanningSchoolStatus.CLOSED.value and exists_organization.status == PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_organization.status = PlanningSchoolStatus.CLOSED.value
        else:
            # exists_organization.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_organization.status,2222222)
        organization_db = await self.organization_dao.update_organization_byargs(exists_organization, *need_update_list)

        # organization_daodb = await self.organization_dao.update_organization_daostatus(exists_organization,status)
        # school = orm_model_to_view_model(organization_daodb, SchoolModel, exclude=[""],)
        return organization_db

    async def query_organization(self, parent_id, ):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(OrganizationModel).where(OrganizationModel.parent_id == parent_id))
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, Organization)
            convert_snowid_in_model(planning_school)

            lst.append(planning_school)
        return lst

    async def increment_organization_member_cnt(self, organization_id, cnt):
        #

        exists_organization_members = await self.organization_dao.update_organization_increment_member_cnt(
            OrganizationModel(id=int(organization_id), ))
        return organization_id

    # 部门对接
    async def send_org_to_org_center(self, exists_planning_school_origin: Organization | BaseModel, res_unit=None):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer

        school = await self.school_dao.get_school_by_id(exists_planning_school.school_id)
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school.school_id)
            return
        unitid = None
        org_code = exists_planning_school.org_code
        if isinstance(res_unit, dict):
            unitid = res_unit['data2']
        if unitid is None:
            unitid = school.org_center_info
        parent_id = ""
        if int(exists_planning_school.parent_id) != 0:
            parent = await self.organization_dao.get_organization_by_id(exists_planning_school.parent_id)
            if parent is None:
                print('上级部门未找到 跳过发送组织', exists_planning_school.parent_id)
                return
            parent_id = parent.org_code
        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "displayName": exists_planning_school.org_name,
            "educateUnit": unitid if unitid is not None else school.school_name,
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": int(exists_planning_school.parent_id) == 0,
            "key": "",
            "manager": "",
            "name": org_code,
            "newCode": exists_planning_school.org_code,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,
            "parentId": parent_id,
            "parentName": "",
            "tags": [
                ""
            ],
            "title": "",
            "type": "",
        #     秘钥
            "clientId":  'c07ac36559b4a860d248',
            "clientSecret":  '5445838d08a0e7b2139acf77868e858c592e09f3',
        }
        apiname = '/api/add-group-organization'
        # 字典参数
        datadict = dict_data
        datadict = convert_dates_to_strings(datadict)
        print('调用添加部门  字典参数', datadict, )
        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        try:
            print('调用添加部门 接口响应', response, )
            return response, datadict
        except Exception as e:
            print(e)
            raise e
