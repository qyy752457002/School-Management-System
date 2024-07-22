# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.school_eduinfo import SchoolEduinfoNotFoundError
from daos.school_eduinfo_dao import SchoolEduinfoDAO
from models.school_eduinfo import SchoolEduinfo
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.school_eduinfo import SchoolEduInfo as SchoolEduinfoModel


@dataclass_inject
class SchoolEduinfoRule(object):
    school_eduinfo_dao: SchoolEduinfoDAO

    async def get_school_eduinfo_by_id(self, school_eduinfo_id):
        school_eduinfo_db = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school_eduinfo_id)
        # 可选 , exclude=[""]
        school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel)
        return school

    async def get_school_eduinfo_by_school_id(self, school_eduinfo_id):
        school_eduinfo_db = await self.school_eduinfo_dao.get_school_eduinfo_by_school_id(school_eduinfo_id)
        if not school_eduinfo_db:
            return None
        # 可选 , exclude=[""]
        school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel)
        return school

    async def add_school_eduinfo(self, school: SchoolEduinfoModel, convertmodel=True):
        exists_school = await self.school_eduinfo_dao.get_school_eduinfo_by_school_id(
            school.school_id)
        if exists_school:
            raise Exception(f"学校教育信息{school.school_id}已存在")
        if convertmodel:
            school_eduinfo_db = view_model_to_orm_model(school, SchoolEduinfo, exclude=["id"])

        else:
            school_eduinfo_db = SchoolEduinfo()
            school_eduinfo_db.id = None
            school_eduinfo_db.school_id = school.school_id

        school_eduinfo_db.deleted = 0
        school_eduinfo_db.status = '正常'
        school_eduinfo_db.created_uid = 0
        school_eduinfo_db.updated_uid = 0
        school_eduinfo_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        school_eduinfo_db = await self.school_eduinfo_dao.add_school_eduinfo(school_eduinfo_db)
        school = orm_model_to_view_model(school_eduinfo_db, SchoolEduinfoModel, exclude=["created_at", 'updated_at'])
        return school

    async def update_school_eduinfo(self, school, ctype=1):
        exists_school = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校教育信息{school.id}不存在")
        if ctype == 1:
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
            school_eduinfo_db.school_eduinfo_name = school.school_eduinfo_name
            school_eduinfo_db.school_eduinfo_short_name = school.school_eduinfo_short_name
            school_eduinfo_db.school_eduinfo_code = school.school_eduinfo_code
            school_eduinfo_db.create_school_eduinfo_date = school.create_school_eduinfo_date
            school_eduinfo_db.founder_type = school.founder_type
            school_eduinfo_db.founder_name = school.founder_name
            school_eduinfo_db.urban_rural_nature = school.urban_rural_nature
            school_eduinfo_db.school_eduinfo_operation_type = school.school_eduinfo_operation_type
            school_eduinfo_db.school_eduinfo_org_form = school.school_eduinfo_org_form
            school_eduinfo_db.school_eduinfo_operation_type_lv2 = school.school_eduinfo_operation_type_lv2
            school_eduinfo_db.school_eduinfo_operation_type_lv3 = school.school_eduinfo_operation_type_lv3
            school_eduinfo_db.department_unit_number = school.department_unit_number
            school_eduinfo_db.sy_zones = school.sy_zones
            school_eduinfo_db.historical_evolution = school.historical_evolution

        school_eduinfo_db = await self.school_eduinfo_dao.update_school_eduinfo(school_eduinfo_db, ctype)
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
                                             school_eduinfo_id=None, school_eduinfo_no=None):
        paging = await self.school_eduinfo_dao.query_school_eduinfo_with_page(school_eduinfo_name, school_eduinfo_id,
                                                                              school_eduinfo_no,
                                                                              page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SchoolEduinfoModel)
        return paging_result

    async def update_school_eduinfo_byargs(self, school_eduinfo, ctype=1):
        if school_eduinfo.school_id > 0:
            # planning_school = await self.planning_school_rule.get_planning_school_by_id(planning_school_eduinfo.planning_school_id)
            exists_school_eduinfo = await self.school_eduinfo_dao.get_school_eduinfo_by_school_id(
                school_eduinfo.school_id)


        else:

            exists_school_eduinfo = await self.school_eduinfo_dao.get_school_eduinfo_by_id(school_eduinfo.id)
        if not exists_school_eduinfo:
            raise SchoolEduinfoNotFoundError()
        need_update_list = []
        for key, value in school_eduinfo.dict().items():
            if value and key != 'id':
                need_update_list.append(key)

        school_eduinfo_db = await self.school_eduinfo_dao.update_school_eduinfo_byargs(school_eduinfo,
                                                                                       *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        return school_eduinfo_db

    async def add_school_eduinfo_from_planning_school(self, planning_school: PlanningSchoolEduInfo, school_res):
        # todo 这里的值转换 用 数据库db类型直接赋值  模型转容易报错   另 其他2个表的写入  检查是否原有的  防止重复新增
        # return None

        # schooldatabaseinfo = SchoolBaseInfoOptional(**planning_school.__dict__)
        dicta = planning_school.__dict__
        dicta['school_id'] = school_res.id

        school = SchoolEduinfoModel(**dicta)
        # school = orm_model_to_view_model(planning_school, SchoolKeyAddInfo, exclude=["id"])
        # school.school_name = planning_school.planning_school_name
        # school.planning_school_id = planning_school.id
        # school.school_no = planning_school.planning_school_no
        # school.school_edu_level = planning_school.planning_school_edu_level
        # school.school_category = planning_school.planning_school_category
        # school.school_operation_type = planning_school.planning_school_operation_type
        # school.school_org_type = planning_school.planning_school_org_type
        # school.school_level = planning_school.planning_school_level
        # school.school_code = planning_school.planning_school_code

        return await self.add_school_eduinfo(school)
