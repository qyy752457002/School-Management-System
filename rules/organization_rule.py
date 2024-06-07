# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.school import SchoolNotFoundError
# from daos.organization_dao import CampusDAO
from daos.organization_dao import OrganizationDAO
# from models.organization import Campus
from rules.enum_value_rule import EnumValueRule
from views.models.organization import Organization
# from views.models.organization import Campus as Organization

# from views.models.organization import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from views.models.school import School as SchoolModel
from models.organization import Organization as OrganizationModel
@dataclass_inject
class OrganizationRule(object):
    organization_dao: OrganizationDAO

    async def get_organization_by_id(self, organization_id,extra_model=None):
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
            organization.org_name)
        if exists_organization:
            raise Exception(f"{organization.organization_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        organization_db = view_model_to_orm_model(organization, OrganizationModel,    exclude=["id"])
        # school_db.status =  PlanningSchoolStatus.DRAFT.value
        # 校区只有2步  故新增几位开设中 
        organization_db.created_uid = 0
        organization_db.updated_uid = 0

        organization_db = await self.organization_dao.add_organization(organization_db)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=["created_at",'updated_at'])
        return organization

    async def update_organization(self, organization,ctype=1):
        # 默认 改 关键信息
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise Exception(f"校区{organization.id}不存在")
        if ctype==1:
            organization_db = Campus()
            organization_db.id = organization.id
            organization_db.organization_no = organization.organization_no
            organization_db.organization_name = organization.organization_name
            organization_db.block = organization.block
            organization_db.borough = organization.borough
            organization_db.organization_type = organization.organization_type
            organization_db.organization_operation_type = organization.organization_operation_type
            organization_db.organization_operation_type_lv2 = organization.organization_operation_type_lv2
            organization_db.organization_operation_type_lv3 = organization.organization_operation_type_lv3
            organization_db.organization_org_type = organization.organization_org_type
            organization_db.organization_level = organization.organization_level
        else:
            organization_db = Campus()
            organization_db.id = organization.id
            organization_db.organization_name=organization.organization_name
            organization_db.organization_short_name=organization.organization_short_name
            organization_db.organization_code=organization.organization_code
            organization_db.create_organization_date=organization.create_organization_date
            organization_db.founder_type=organization.founder_type
            organization_db.founder_name=organization.founder_name
            organization_db.urban_rural_nature=organization.urban_rural_nature
            organization_db.organization_operation_type=organization.organization_operation_type
            organization_db.organization_org_form=organization.organization_org_form
            organization_db.organization_operation_type_lv2=organization.organization_operation_type_lv2
            organization_db.organization_operation_type_lv3=organization.organization_operation_type_lv3
            organization_db.department_unit_number=organization.department_unit_number
            organization_db.sy_zones=organization.sy_zones
            organization_db.historical_evolution=organization.historical_evolution


        organization_db = await self.organization_dao.update_organization(organization_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization_db

    async def update_organization_byargs(self, organization,ctype=1):
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise Exception(f"校区{organization.id}不存在")
        # if exists_organization.status== PlanningSchoolStatus.DRAFT.value:
        #     exists_organization.status= PlanningSchoolStatus.OPENING.value
        #     organization.status= PlanningSchoolStatus.OPENING.value
        # else:
        #     pass
        need_update_list = []

        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)

        organization_db = await self.organization_dao.update_organization_byargs(organization, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization_db

    async def delete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"校区{organization_id}不存在")
        organization_db = await self.organization_dao.delete_organization(exists_organization)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=[""],)
        return organization

    async def softdelete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"校区{organization_id}不存在")
        organization_db = await self.organization_dao.softdelete_organization(exists_organization)
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""],)
        return organization_db

    async def get_all_organizations(self):
        return await self.organization_dao.get_all_organizations()

    async def get_organization_count(self):
        return await self.organization_dao.get_organization_count()

    async def query_organization_with_page(self, page_request: PageRequest,   org_type , school_id ):


        paging = await self.organization_dao.query_organization_with_page(page_request,  org_type , school_id
                                                              )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, Organization)
        return paging_result



    async def update_organization_status(self, organization_id, status,action=None):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"学校{organization_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_organization.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_organization.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_organization.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_organization.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_organization.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_organization.status,2222222)
        organization_db = await self.organization_dao.update_organization_byargs(exists_organization,*need_update_list)


        # organization_daodb = await self.organization_dao.update_organization_daostatus(exists_organization,status)
        # school = orm_model_to_view_model(organization_daodb, SchoolModel, exclude=[""],)
        return organization_db



    async def query_organization(self,planning_organization_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(Campus).where(Campus.organization_name.like(f'%{planning_organization_name}%') ))
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, Organization)

            lst.append(planning_school)
        return lst

