# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.planning_school_communication_dao import PlanningSchoolCommunicationDAO
from models.planning_school_communication import PlanningSchoolCommunication
from views.models.planning_school_communications import PlanningSchoolCommunications  as PlanningSchoolCommunicationModel



@dataclass_inject
class PlanningSchoolCommunicationRule(object):
    planning_school_communication_dao: PlanningSchoolCommunicationDAO

    async def get_planning_school_communication_by_id(self, planning_school_communication_id):
        planning_school_communication_db = await self.planning_school_communication_dao.get_planning_school_communication_by_id(planning_school_communication_id)
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_communication_db, PlanningSchoolCommunicationModel)
        return planning_school

    async def add_planning_school_communication(self, planning_school: PlanningSchoolCommunicationModel):
        exists_planning_school = await self.planning_school_communication_dao.get_planning_school_communication_by_id(
            planning_school.planning_school_id)
        if exists_planning_school:
            raise Exception(f"规划校通信信息{planning_school.planning_school_communication_name}已存在")
        planning_school_communication_db = PlanningSchoolCommunication()
        planning_school_communication_db.planning_school_id = planning_school.planning_school_id
        planning_school_communication_db.postal_code = planning_school.postal_code
        planning_school_communication_db.fax_number = planning_school.fax_number
        planning_school_communication_db.email = planning_school.email
        planning_school_communication_db.contact_number = planning_school.contact_number
        planning_school_communication_db.area_code = planning_school.area_code

        planning_school_communication_db.long = planning_school.long
        planning_school_communication_db.lat = planning_school.lat
        planning_school_communication_db.leg_repr_name = planning_school.leg_repr_name
        planning_school_communication_db.party_leader_name = planning_school.party_leader_name
        planning_school_communication_db.party_leader_position = planning_school.party_leader_position
        planning_school_communication_db.adm_leader_name = planning_school.adm_leader_name
        planning_school_communication_db.adm_leader_position = planning_school.adm_leader_position
        planning_school_communication_db.loc_area = planning_school.loc_area
        planning_school_communication_db.loc_area_pro = planning_school.loc_area_pro
        planning_school_communication_db.detailed_address = planning_school.detailed_address
        planning_school_communication_db.related_license_upload = planning_school.related_license_upload
        planning_school_communication_db.school_web_url = planning_school.school_web_url
        planning_school_communication_db.deleted = 0
        planning_school_communication_db.status = '正常'
        planning_school_communication_db.created_uid = 0
        planning_school_communication_db.updated_uid = 0


        planning_school_communication_db.status = '正常'
        planning_school_communication_db.created_uid = 0
        planning_school_communication_db.updated_uid = 0

        planning_school_communication_db = await self.planning_school_communication_dao.add_planning_school_communication(planning_school_communication_db)
        planning_school = orm_model_to_view_model(planning_school_communication_db, PlanningSchoolCommunicationModel, exclude=[""])
        return planning_school

    async def update_planning_school_communication(self, planning_school,ctype=1):
        exists_planning_school = await self.planning_school_communication_dao.get_planning_school_communication_by_id(planning_school.id)
        if not exists_planning_school:
            raise Exception(f"规划校通信信息{planning_school.id}不存在")
        if ctype==1:
            planning_school_communication_db = PlanningSchoolCommunication()
            planning_school_communication_db.id = planning_school.id
            planning_school_communication_db.planning_school_communication_no = planning_school.planning_school_communication_no
            planning_school_communication_db.planning_school_communication_name = planning_school.planning_school_communication_name
            planning_school_communication_db.block = planning_school.block
            planning_school_communication_db.borough = planning_school.borough
            planning_school_communication_db.planning_school_communication_type = planning_school.planning_school_communication_type
            planning_school_communication_db.planning_school_communication_operation_type = planning_school.planning_school_communication_operation_type
            planning_school_communication_db.planning_school_communication_operation_type_lv2 = planning_school.planning_school_communication_operation_type_lv2
            planning_school_communication_db.planning_school_communication_operation_type_lv3 = planning_school.planning_school_communication_operation_type_lv3
            planning_school_communication_db.planning_school_communication_org_type = planning_school.planning_school_communication_org_type
            planning_school_communication_db.planning_school_communication_level = planning_school.planning_school_communication_level
        else:
            planning_school_communication_db = PlanningSchoolCommunication()
            planning_school_communication_db.id = planning_school.id
            planning_school_communication_db.planning_school_communication_name=planning_school.planning_school_communication_name
            planning_school_communication_db.planning_school_communication_short_name=planning_school.planning_school_communication_short_name
            planning_school_communication_db.planning_school_communication_code=planning_school.planning_school_communication_code
            planning_school_communication_db.create_planning_school_communication_date=planning_school.create_planning_school_communication_date
            planning_school_communication_db.founder_type=planning_school.founder_type
            planning_school_communication_db.founder_name=planning_school.founder_name
            planning_school_communication_db.urban_rural_nature=planning_school.urban_rural_nature
            planning_school_communication_db.planning_school_communication_operation_type=planning_school.planning_school_communication_operation_type
            planning_school_communication_db.planning_school_communication_org_form=planning_school.planning_school_communication_org_form
            planning_school_communication_db.planning_school_communication_operation_type_lv2=planning_school.planning_school_communication_operation_type_lv2
            planning_school_communication_db.planning_school_communication_operation_type_lv3=planning_school.planning_school_communication_operation_type_lv3
            planning_school_communication_db.department_unit_number=planning_school.department_unit_number
            planning_school_communication_db.sy_zones=planning_school.sy_zones
            planning_school_communication_db.historical_evolution=planning_school.historical_evolution


        planning_school_communication_db = await self.planning_school_communication_dao.update_planning_school_communication(planning_school_communication_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_communication_db, PlanningSchoolCommunicationModel, exclude=[""])
        return planning_school_communication_db

    async def softdelete_planning_school_communication(self, planning_school_communication_id):
        exists_planning_school = await self.planning_school_communication_dao.get_planning_school_communication_by_id(planning_school_communication_id)
        if not exists_planning_school:
            raise Exception(f"规划校通信信息{planning_school_communication_id}不存在")
        planning_school_communication_db = await self.planning_school_communication_dao.softdelete_planning_school_communication(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_communication_db, PlanningSchoolCommunicationModel, exclude=[""],)
        return planning_school_communication_db


    async def get_planning_school_communication_count(self):
        return await self.planning_school_communication_dao.get_planning_school_communication_count()

    async def query_planning_school_communication_with_page(self, page_request: PageRequest, planning_school_communication_name=None,
                                              planning_school_communication_id=None,planning_school_communication_no=None ):
        paging = await self.planning_school_communication_dao.query_planning_school_communication_with_page(planning_school_communication_name, planning_school_communication_id,planning_school_communication_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolCommunicationModel)
        return paging_result

