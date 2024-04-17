from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.planning_school_dao import PlanningSchoolDAO
from models.planning_school import PlanningSchool
from views.models.planning_school import PlanningSchool as PlanningSchoolModel

from views.models.planning_school import PlanningSchoolBaseInfo


@dataclass_inject
class PlanningSchoolRule(object):
    planning_school_dao: PlanningSchoolDAO

    async def get_planning_school_by_id(self, planning_school_id):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel)
        return planning_school

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school_name)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def add_planning_school(self, planning_school: PlanningSchoolModel):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school.planning_school_name)
        if exists_planning_school:
            raise Exception(f"规划校{planning_school.planning_school_name}已存在")
        planning_school_db = PlanningSchool()
        planning_school_db.planning_school_name = planning_school.planning_school_name
        planning_school_db.planning_school_no = planning_school.planning_school_no
        planning_school_db.planning_school_code = planning_school.planning_school_code

        planning_school_db.planning_school_operation_license_number = planning_school.planning_school_operation_license_number
        planning_school_db.block = planning_school.block
        planning_school_db.borough = planning_school.borough
        planning_school_db.planning_school_type = planning_school.planning_school_type
        planning_school_db.planning_school_operation_type = planning_school.planning_school_operation_type
        planning_school_db.planning_school_operation_type_lv2 = planning_school.planning_school_operation_type_lv2
        planning_school_db.planning_school_operation_type_lv3 = planning_school.planning_school_operation_type_lv3
        planning_school_db.planning_school_org_type = planning_school.planning_school_org_type
        planning_school_db.planning_school_level = planning_school.planning_school_level
        planning_school_db.status = '正常'
        planning_school_db.kg_level = planning_school.kg_level
        planning_school_db.planning_school_short_name = planning_school.planning_school_short_name
        planning_school_db.planning_school_en_name = planning_school.planning_school_en_name
        planning_school_db.create_planning_school_date = planning_school.create_planning_school_date
        planning_school_db.social_credit_code = planning_school.social_credit_code
        planning_school_db.founder_type = planning_school.founder_type
        planning_school_db.founder_name = planning_school.founder_name
        planning_school_db.founder_code = planning_school.founder_code
        planning_school_db.urban_rural_nature = planning_school.urban_rural_nature
        planning_school_db.planning_school_org_form = planning_school.planning_school_org_form
        planning_school_db.planning_school_closure_date = planning_school.planning_school_closure_date
        planning_school_db.department_unit_number = planning_school.department_unit_number
        planning_school_db.sy_zones = planning_school.sy_zones
        planning_school_db.historical_evolution = planning_school.historical_evolution
        planning_school_db.sy_zones_pro = planning_school.sy_zones_pro
        planning_school_db.primary_planning_school_system = planning_school.primary_planning_school_system
        planning_school_db.primary_planning_school_entry_age = planning_school.primary_planning_school_entry_age
        planning_school_db.junior_middle_planning_school_system = planning_school.junior_middle_planning_school_system
        planning_school_db.junior_middle_planning_school_entry_age = planning_school.junior_middle_planning_school_entry_age
        planning_school_db.senior_middle_planning_school_system = planning_school.senior_middle_planning_school_system
        planning_school_db.created_uid = 0
        planning_school_db.updated_uid = 0
        # planning_school_db.created_at = planning_school.created_at
        # planning_school_db.updated_at = planning_school.updated_at

        planning_school_db = await self.planning_school_dao.add_planning_school(planning_school_db)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def update_planning_school(self, planning_school):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise Exception(f"规划校{planning_school.id}不存在")
        planning_school_db = await self.planning_school_dao.update_planning_school(planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def delete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise Exception(f"规划校{planning_school_id}不存在")
        planning_school_db = await self.planning_school_dao.delete_planning_school(exists_planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def get_all_planning_schools(self):
        return await self.planning_school_dao.get_all_planning_schools()

    async def get_planning_school_count(self):
        return await self.planning_school_dao.get_planning_school_count()

    async def query_planning_school_with_page(self, page_request: PageRequest, planning_school_name=None,
                                              planning_school_id=None,planning_school_no=None ):
        paging = await self.planning_school_dao.query_planning_school_with_page(planning_school_name, planning_school_id,planning_school_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolModel)
        return paging_result
