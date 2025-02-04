import copy

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from sqlalchemy import select

from business_exceptions.school import SchoolNotFoundError
from daos.campus_dao import CampusDAO
from daos.school_dao import SchoolDAO
from models.campus import Campus
from rules.enum_value_rule import EnumValueRule
from views.common.common_view import convert_snowid_in_model, convert_snowid_to_strings
from views.models.campus import Campus as CampusModel

from views.models.planning_school import PlanningSchoolStatus
from views.models.school import School as SchoolModel


@dataclass_inject
class CampusRule(object):
    campus_dao: CampusDAO
    p_school_dao: SchoolDAO

    async def get_campus_by_id(self, campus_id, extra_model=None):
        campus_db = await self.campus_dao.get_campus_by_id(campus_id)
        # 可选 , exclude=[""]
        if extra_model:
            # school = orm_model_to_view_model(school_db, extra_model)
            campus = orm_model_to_view_model(campus_db, extra_model)

        else:
            campus = orm_model_to_view_model(campus_db, CampusModel)
        return campus

    async def get_campus_by_campus_name(self, campus_name):
        campus_db = await self.campus_dao.get_campus_by_campus_name(
            campus_name)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        return campus

    async def add_campus(self, campus: CampusModel):
        exists_campus = await self.campus_dao.get_campus_by_campus_name(
            campus.campus_name)
        if exists_campus:
            raise Exception(f"校区{campus.campus_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        campus_db = view_model_to_orm_model(campus, Campus, exclude=["id"])
        # school_db.status =  PlanningSchoolStatus.DRAFT.value
        # 校区只有2步  故新增几位开设中 
        campus_db.status = PlanningSchoolStatus.NORMAL.value
        campus_db.created_uid = 0
        campus_db.updated_uid = 0
        campus_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        if campus.school_id > 0:
            # rule互相应用有问题  用dao
            p_exists_school_model = await self.p_school_dao.get_school_by_id(campus.school_id)
            if not p_exists_school_model:
                raise SchoolNotFoundError()
            # print(p_exists_school_model,999)

            p_exists_school = orm_model_to_view_model(p_exists_school_model, SchoolModel)
            # print(p_exists_school)

            if p_exists_school:
                # 办学者
                campus_db.campus_operation_type = p_exists_school.school_operation_type
                campus_db.campus_org_type = p_exists_school.school_org_type
                campus_db.campus_org_form = p_exists_school.school_org_form
                campus_db.founder_type = p_exists_school.founder_type
                campus_db.founder_type_lv2 = p_exists_school.founder_type_lv2
                campus_db.founder_type_lv3 = p_exists_school.founder_type_lv3
                campus_db.founder_name = p_exists_school.founder_name
                campus_db.founder_code = p_exists_school.founder_code

        campus_db = await self.campus_dao.add_campus(campus_db)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=["created_at", 'updated_at'])
        convert_snowid_in_model(campus, ['planning_school_id', 'school_id'])

        return campus

    async def update_campus(self, campus, ctype=1):
        # 默认 改 关键信息
        exists_campus = await self.campus_dao.get_campus_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区{campus.id}不存在")
        if ctype == 1:
            campus_db = Campus()
            campus_db.id = campus.id
            campus_db.campus_no = campus.campus_no
            campus_db.campus_name = campus.campus_name
            campus_db.block = campus.block
            campus_db.borough = campus.borough
            campus_db.campus_type = campus.campus_type
            campus_db.campus_operation_type = campus.campus_operation_type
            campus_db.campus_operation_type_lv2 = campus.campus_operation_type_lv2
            campus_db.campus_operation_type_lv3 = campus.campus_operation_type_lv3
            campus_db.campus_org_type = campus.campus_org_type
            campus_db.campus_level = campus.campus_level
        else:
            campus_db = Campus()
            campus_db.id = campus.id
            campus_db.campus_name = campus.campus_name
            campus_db.campus_short_name = campus.campus_short_name
            campus_db.campus_code = campus.campus_code
            campus_db.create_campus_date = campus.create_campus_date
            campus_db.founder_type = campus.founder_type
            campus_db.founder_name = campus.founder_name
            campus_db.urban_rural_nature = campus.urban_rural_nature
            campus_db.campus_operation_type = campus.campus_operation_type
            campus_db.campus_org_form = campus.campus_org_form
            campus_db.campus_operation_type_lv2 = campus.campus_operation_type_lv2
            campus_db.campus_operation_type_lv3 = campus.campus_operation_type_lv3
            campus_db.department_unit_number = campus.department_unit_number
            campus_db.sy_zones = campus.sy_zones
            campus_db.historical_evolution = campus.historical_evolution

        campus_db = await self.campus_dao.update_campus(campus_db, ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        return campus_db

    async def update_campus_byargs(self, campus, ctype=1):
        exists_campus = await self.campus_dao.get_campus_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区{campus.id}不存在")
        # if exists_campus.status== PlanningSchoolStatus.DRAFT.value:
        #     exists_campus.status= PlanningSchoolStatus.OPENING.value
        #     campus.status= PlanningSchoolStatus.OPENING.value
        # else:
        #     pass
        need_update_list = []

        for key, value in campus.dict().items():
            if value:
                need_update_list.append(key)

        campus_db = await self.campus_dao.update_campus_byargs(campus, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        campus2 = copy.deepcopy(campus_db)
        convert_snowid_in_model(campus2, ['planning_school_id', 'school_id', 'id'])
        return campus2

    async def delete_campus(self, campus_id):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"校区{campus_id}不存在")
        campus_db = await self.campus_dao.delete_campus(exists_campus)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""], )
        return campus

    async def softdelete_campus(self, campus_id):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"校区{campus_id}不存在")
        campus_db = await self.campus_dao.softdelete_campus(exists_campus)
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""],)
        return campus_db

    async def get_all_campuss(self):
        return await self.campus_dao.get_all_campuss()

    async def get_campus_count(self):
        return await self.campus_dao.get_campus_count()

    async def query_campus_with_page(self, page_request: PageRequest, campus_name, campus_no, campus_code,
                                     block, campus_level, borough, status, founder_type,
                                     founder_type_lv2,
                                     founder_type_lv3, planning_campus_id):
        #  根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res = await enum_value_rule.get_next_level_enum_values('founder_type', founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)

            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if len(founder_type_lv2) > 0:
            founder_type_lv3_res = await enum_value_rule.get_next_level_enum_values('founder_type_lv2',
                                                                                    founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.campus_dao.query_campus_with_page(page_request, campus_name, campus_no, campus_code,
                                                              block, campus_level, borough, status, founder_type,
                                                              founder_type_lv2,
                                                              founder_type_lv3, planning_campus_id
                                                              )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CampusModel)
        convert_snowid_to_strings(paging_result, extra_colums=["id", "campus_id", 'school_id'])
        return paging_result

    async def update_campus_status(self, campus_id, status, action_reason=None,related_license_upload=None):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"学校{campus_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status == PlanningSchoolStatus.NORMAL.value and exists_campus.status == PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_campus.status = PlanningSchoolStatus.NORMAL.value
        elif status == PlanningSchoolStatus.CLOSED.value and exists_campus.status == PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_campus.status = PlanningSchoolStatus.CLOSED.value
        else:
            # exists_campus.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')
        need_update_list.append('action_reason')
        need_update_list.append('related_license_upload')
        exists_campus.action_reason = action_reason
        exists_campus.related_license_upload = related_license_upload

        # print(exists_campus.status,2222222)
        campus_db = await self.campus_dao.update_campus_byargs(exists_campus, *need_update_list)

        # campus_daodb = await self.campus_dao.update_campus_daostatus(exists_campus,status)
        # school = orm_model_to_view_model(campus_daodb, SchoolModel, exclude=[""],)
        return campus_db

    async def query_campus(self, planning_campus_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(Campus).where(Campus.campus_name.like(f'%{planning_campus_name}%')))
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, CampusModel)

            lst.append(planning_school)
        return lst
