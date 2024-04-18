# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.school_eduinfo_dao import SchoolEduinfoDAO
from models.school_eduinfo import SchoolEduinfo
from views.models.school_eduinfo import SchoolEduInfo  as SchoolEduinfoModel



@dataclass_inject
class SchoolEduinfoRule(object):
    school_eduinfo_dao: SchoolEduinfoDAO

    async def get_school_eduinfo_by_id(self, school_eduinfo_id):
        school_eduinfo_db = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school_eduinfo_id)
        # 可选 , exclude=[""]
        school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel)
        return school

    async def add_school_eduinfo(self, school: SchoolEduinfoModel):
        exists_school = await self.school_eduinfo_dao.get_school_eduinfo_by_id(
            school.school_id)
        if exists_school:
            raise Exception(f"学校教育信息{school.school_eduinfo_name}已存在")
        school_eduinfo_db = SchoolEduinfo()
        school_eduinfo_db.is_ethnic_school = school.is_ethnic_school
        school_eduinfo_db.is_att_class = school.is_att_class
        school_eduinfo_db.att_class_type = school.att_class_type
        school_eduinfo_db.is_province_feat = school.is_province_feat
        school_eduinfo_db.is_bilingual_clas = school.is_bilingual_clas
        school_eduinfo_db.minority_lang_code = school.minority_lang_code
        school_eduinfo_db.is_profitable = school.is_profitable
        school_eduinfo_db.prof_org_name = school.prof_org_name
        school_eduinfo_db.is_prov_demo = school.is_prov_demo
        school_eduinfo_db.is_latest_year = school.is_latest_year
        school_eduinfo_db.is_town_kinderg = school.is_town_kinderg
        school_eduinfo_db.is_incl_kinderg = school.is_incl_kinderg
        school_eduinfo_db.is_affil_school = school.is_affil_school
        school_eduinfo_db.affil_univ_code = school.affil_univ_code
        school_eduinfo_db.affil_univ_name = school.affil_univ_name
        school_eduinfo_db.is_last_yr_revok = school.is_last_yr_revok
        school_eduinfo_db.is_school_counted = school.is_school_counted

        school_eduinfo_db.school_id = school.school_id

        school_eduinfo_db.deleted = 0
        school_eduinfo_db.created_uid = 0
        school_eduinfo_db.updated_uid = 0


        school_eduinfo_db = await self.school_eduinfo_dao.add_school_eduinfo(school_eduinfo_db)
        school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel, exclude=[""])
        return school

    async def update_school_eduinfo(self, school,ctype=1):
        exists_school = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校教育信息{school.id}不存在")
        if ctype==1:
            school_eduinfo_db = SchoolEduinfo()
            school_eduinfo_db.id = school.id
            school_eduinfo_db.school_eduinfo_no = school.school_eduinfo_no
            school_eduinfo_db.school_eduinfo_name = school.school_eduinfo_name
            school_eduinfo_db.block = school.block
            school_eduinfo_db.borough = school.borough
            school_eduinfo_db.school_eduinfo_type = school.school_eduinfo_type
            school_eduinfo_db.school_eduinfo_operation_type = school.school_eduinfo_operation_type
            school_eduinfo_db.school_eduinfo_operation_type_lv2 = school.school_eduinfo_operation_type_lv2
            school_eduinfo_db.school_eduinfo_operation_type_lv3 = school.school_eduinfo_operation_type_lv3
            school_eduinfo_db.school_eduinfo_org_type = school.school_eduinfo_org_type
            school_eduinfo_db.school_eduinfo_level = school.school_eduinfo_level
        else:
            school_eduinfo_db = SchoolEduinfo()
            school_eduinfo_db.id = school.id
            school_eduinfo_db.school_eduinfo_name=school.school_eduinfo_name
            school_eduinfo_db.school_eduinfo_short_name=school.school_eduinfo_short_name
            school_eduinfo_db.school_eduinfo_code=school.school_eduinfo_code
            school_eduinfo_db.create_school_eduinfo_date=school.create_school_eduinfo_date
            school_eduinfo_db.founder_type=school.founder_type
            school_eduinfo_db.founder_name=school.founder_name
            school_eduinfo_db.urban_rural_nature=school.urban_rural_nature
            school_eduinfo_db.school_eduinfo_operation_type=school.school_eduinfo_operation_type
            school_eduinfo_db.school_eduinfo_org_form=school.school_eduinfo_org_form
            school_eduinfo_db.school_eduinfo_operation_type_lv2=school.school_eduinfo_operation_type_lv2
            school_eduinfo_db.school_eduinfo_operation_type_lv3=school.school_eduinfo_operation_type_lv3
            school_eduinfo_db.department_unit_number=school.department_unit_number
            school_eduinfo_db.sy_zones=school.sy_zones
            school_eduinfo_db.historical_evolution=school.historical_evolution


        school_eduinfo_db = await self.school_eduinfo_dao.update_school_eduinfo(school_eduinfo_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel, exclude=[""])
        return school_eduinfo_db

    async def softdelete_school_eduinfo(self, school_eduinfo_id):
        exists_school = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school_eduinfo_id)
        if not exists_school:
            raise Exception(f"学校教育信息{school_eduinfo_id}不存在")
        school_eduinfo_db = await self.school_eduinfo_dao.softdelete_school_eduinfo(exists_school)
        # school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel, exclude=[""],)
        return school_eduinfo_db


    async def get_school_eduinfo_count(self):
        return await self.school_eduinfo_dao.get_school_eduinfo_count()

    async def query_school_eduinfo_with_page(self, page_request: PageRequest, school_eduinfo_name=None,
                                              school_eduinfo_id=None,school_eduinfo_no=None ):
        paging = await self.school_eduinfo_dao.query_school_eduinfo_with_page(school_eduinfo_name, school_eduinfo_id,school_eduinfo_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SchoolEduinfoModel)
        return paging_result

