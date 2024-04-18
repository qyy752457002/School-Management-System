import hashlib

import shortuuid

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.institution_dao import InstitutionDAO
from models.institution import Institution
from views.models.institutions import Institutions  as InstitutionModel



@dataclass_inject
class InstitutionRule(object):
    institution_dao: InstitutionDAO

    async def get_institution_by_id(self, institution_id):
        institution_db = await self.institution_dao.get_institution_by_id(institution_id)
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(institution_db, InstitutionModel)
        return planning_school

    async def add_institution(self, planning_school: InstitutionModel):
        exists_planning_school = await self.institution_dao.get_institution_by_id(
            planning_school.planning_school_id)
        if exists_planning_school:
            raise Exception(f"行政事业单位{planning_school.institution_name}已存在")
        institution_db = Institution()
        institution_db.is_ethnic_school = planning_school.is_ethnic_school
        institution_db.is_att_class = planning_school.is_att_class
        institution_db.att_class_type = planning_school.att_class_type
        institution_db.is_province_feat = planning_school.is_province_feat
        institution_db.is_bilingual_clas = planning_school.is_bilingual_clas
        institution_db.minority_lang_code = planning_school.minority_lang_code
        institution_db.is_profitable = planning_school.is_profitable
        institution_db.prof_org_name = planning_school.prof_org_name
        institution_db.is_prov_demo = planning_school.is_prov_demo
        institution_db.is_latest_year = planning_school.is_latest_year
        institution_db.is_town_kinderg = planning_school.is_town_kinderg
        institution_db.is_incl_kinderg = planning_school.is_incl_kinderg
        institution_db.is_affil_school = planning_school.is_affil_school
        institution_db.affil_univ_code = planning_school.affil_univ_code
        institution_db.affil_univ_name = planning_school.affil_univ_name
        institution_db.is_last_yr_revok = planning_school.is_last_yr_revok
        institution_db.is_school_counted = planning_school.is_school_counted

        institution_db.planning_school_id = planning_school.planning_school_id

        institution_db.deleted = 0
        institution_db.created_uid = 0
        institution_db.updated_uid = 0


        institution_db = await self.institution_dao.add_institution(institution_db)
        planning_school = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""])
        return planning_school

    async def update_institution(self, planning_school,ctype=1):
        exists_planning_school = await self.institution_dao.get_institution_by_id(planning_school.id)
        if not exists_planning_school:
            raise Exception(f"行政事业单位{planning_school.id}不存在")
        if ctype==1:
            institution_db = Institution()
            institution_db.id = planning_school.id
            institution_db.institution_no = planning_school.institution_no
            institution_db.institution_name = planning_school.institution_name
            institution_db.block = planning_school.block
            institution_db.borough = planning_school.borough
            institution_db.institution_type = planning_school.institution_type
            institution_db.institution_operation_type = planning_school.institution_operation_type
            institution_db.institution_operation_type_lv2 = planning_school.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3 = planning_school.institution_operation_type_lv3
            institution_db.institution_org_type = planning_school.institution_org_type
            institution_db.institution_level = planning_school.institution_level
        else:
            institution_db = Institution()
            institution_db.id = planning_school.id
            institution_db.institution_name=planning_school.institution_name
            institution_db.institution_short_name=planning_school.institution_short_name
            institution_db.institution_code=planning_school.institution_code
            institution_db.create_institution_date=planning_school.create_institution_date
            institution_db.founder_type=planning_school.founder_type
            institution_db.founder_name=planning_school.founder_name
            institution_db.urban_rural_nature=planning_school.urban_rural_nature
            institution_db.institution_operation_type=planning_school.institution_operation_type
            institution_db.institution_org_form=planning_school.institution_org_form
            institution_db.institution_operation_type_lv2=planning_school.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3=planning_school.institution_operation_type_lv3
            institution_db.department_unit_number=planning_school.department_unit_number
            institution_db.sy_zones=planning_school.sy_zones
            institution_db.historical_evolution=planning_school.historical_evolution


        institution_db = await self.institution_dao.update_institution(institution_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""])
        return institution_db

    async def softdelete_institution(self, institution_id):
        exists_planning_school = await self.institution_dao.get_institution_by_id(institution_id)
        if not exists_planning_school:
            raise Exception(f"行政事业单位{institution_id}不存在")
        institution_db = await self.institution_dao.softdelete_institution(exists_planning_school)
        # planning_school = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""],)
        return institution_db


    async def get_institution_count(self):
        return await self.institution_dao.get_institution_count()

    async def query_institution_with_page(self, page_request: PageRequest, institution_name=None,
                                              institution_id=None,institution_no=None ):
        paging = await self.institution_dao.query_institution_with_page(institution_name, institution_id,institution_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, InstitutionModel)
        return paging_result

