# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.planning_school_eduinfo_dao import PlanningSchoolEduinfoDAO
from models.planning_school_eduinfo import PlanningSchoolEduinfo
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo  as PlanningSchoolEduinfoModel



@dataclass_inject
class PlanningSchoolEduinfoRule(object):
    planning_school_eduinfo_dao: PlanningSchoolEduinfoDAO

    async def get_planning_school_eduinfo_by_id(self, planning_school_eduinfo_id):
        planning_school_eduinfo_db = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_id(planning_school_eduinfo_id)
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_eduinfo_db, PlanningSchoolEduinfoModel)
        return planning_school

    async def get_planning_school_eduinfo_by_planning_school_id(self, planning_school_eduinfo_id):
        planning_school_eduinfo_db = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_planning_school_id(planning_school_eduinfo_id)
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_eduinfo_db, PlanningSchoolEduinfoModel)
        return planning_school


    async def add_planning_school_eduinfo(self, planning_school: PlanningSchoolEduinfoModel,convertmodel=True):
        exists_planning_school = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_id(
            planning_school.planning_school_id)
        if exists_planning_school:
            raise Exception(f"规划校教育信息{planning_school.planning_school_id}已存在")
        if convertmodel:
            planning_school_eduinfo_db = view_model_to_orm_model(planning_school, PlanningSchoolEduinfo,    exclude=["id"])

        else:
            planning_school_eduinfo_db = PlanningSchoolEduinfo(**planning_school.__dict__)
            planning_school_eduinfo_db.id = None
            planning_school_eduinfo_db.planning_school_id= planning_school.planning_school_id


        planning_school_eduinfo_db.deleted = 0
        planning_school_eduinfo_db.created_uid = 0
        planning_school_eduinfo_db.updated_uid = 0

        planning_school_eduinfo_db = await self.planning_school_eduinfo_dao.add_planning_school_eduinfo(planning_school_eduinfo_db)
        planning_school = orm_model_to_view_model(planning_school_eduinfo_db, PlanningSchoolEduinfoModel, exclude=["created_at",'updated_at'])
        return planning_school

    async def update_planning_school_eduinfo(self, planning_school,ctype=1):
        exists_planning_school = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_id(planning_school.id)
        if not exists_planning_school:
            raise Exception(f"规划校教育信息{planning_school.id}不存在")
        if ctype==1:
            planning_school_eduinfo_db = PlanningSchoolEduinfo()
            planning_school_eduinfo_db.id = planning_school.id
            planning_school_eduinfo_db.planning_school_eduinfo_no = planning_school.planning_school_eduinfo_no
            planning_school_eduinfo_db.planning_school_eduinfo_name = planning_school.planning_school_eduinfo_name
            planning_school_eduinfo_db.block = planning_school.block
            planning_school_eduinfo_db.borough = planning_school.borough
            planning_school_eduinfo_db.planning_school_eduinfo_type = planning_school.planning_school_eduinfo_type
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type = planning_school.planning_school_eduinfo_operation_type
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type_lv2 = planning_school.planning_school_eduinfo_operation_type_lv2
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type_lv3 = planning_school.planning_school_eduinfo_operation_type_lv3
            planning_school_eduinfo_db.planning_school_eduinfo_org_type = planning_school.planning_school_eduinfo_org_type
            planning_school_eduinfo_db.planning_school_eduinfo_level = planning_school.planning_school_eduinfo_level
        else:
            planning_school_eduinfo_db = PlanningSchoolEduinfo()
            planning_school_eduinfo_db.id = planning_school.id
            planning_school_eduinfo_db.planning_school_eduinfo_name=planning_school.planning_school_eduinfo_name
            planning_school_eduinfo_db.planning_school_eduinfo_short_name=planning_school.planning_school_eduinfo_short_name
            planning_school_eduinfo_db.planning_school_eduinfo_code=planning_school.planning_school_eduinfo_code
            planning_school_eduinfo_db.create_planning_school_eduinfo_date=planning_school.create_planning_school_eduinfo_date
            planning_school_eduinfo_db.founder_type=planning_school.founder_type
            planning_school_eduinfo_db.founder_name=planning_school.founder_name
            planning_school_eduinfo_db.urban_rural_nature=planning_school.urban_rural_nature
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type=planning_school.planning_school_eduinfo_operation_type
            planning_school_eduinfo_db.planning_school_eduinfo_org_form=planning_school.planning_school_eduinfo_org_form
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type_lv2=planning_school.planning_school_eduinfo_operation_type_lv2
            planning_school_eduinfo_db.planning_school_eduinfo_operation_type_lv3=planning_school.planning_school_eduinfo_operation_type_lv3
            planning_school_eduinfo_db.department_unit_number=planning_school.department_unit_number
            planning_school_eduinfo_db.sy_zones=planning_school.sy_zones
            planning_school_eduinfo_db.historical_evolution=planning_school.historical_evolution


        planning_school_eduinfo_db = await self.planning_school_eduinfo_dao.update_planning_school_eduinfo(planning_school_eduinfo_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_eduinfo_db, PlanningSchoolEduinfoModel, exclude=[""])
        return planning_school_eduinfo_db

    async def softdelete_planning_school_eduinfo(self, planning_school_eduinfo_id):
        exists_planning_school = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_id(planning_school_eduinfo_id)
        if not exists_planning_school:
            raise Exception(f"规划校教育信息{planning_school_eduinfo_id}不存在")
        planning_school_eduinfo_db = await self.planning_school_eduinfo_dao.softdelete_planning_school_eduinfo(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_eduinfo_db, PlanningSchoolEduinfoModel, exclude=[""],)
        return planning_school_eduinfo_db


    async def get_planning_school_eduinfo_count(self):
        return await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_count()

    async def query_planning_school_eduinfo_with_page(self, page_request: PageRequest, planning_school_eduinfo_name=None,
                                              planning_school_eduinfo_id=None,planning_school_eduinfo_no=None ):
        paging = await self.planning_school_eduinfo_dao.query_planning_school_eduinfo_with_page(planning_school_eduinfo_name, planning_school_eduinfo_id,planning_school_eduinfo_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolEduinfoModel)
        return paging_result

