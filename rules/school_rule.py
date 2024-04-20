# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
import hashlib

import shortuuid
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from daos.school_dao import SchoolDAO
from models.school import School
from views.models.planning_school import PlanningSchoolStatus
from views.models.school import School as SchoolModel, SchoolKeyAddInfo

from views.models.school import SchoolBaseInfo


@dataclass_inject
class SchoolRule(object):
    school_dao: SchoolDAO

    async def get_school_by_id(self, school_id):
        school_db = await self.school_dao.get_school_by_id(school_id)
        # 可选 , exclude=[""]
        school = orm_model_to_view_model(school_db, SchoolModel)
        return school

    async def get_school_by_school_name(self, school_name):
        school_db = await self.school_dao.get_school_by_school_name(
            school_name)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school

    async def add_school(self, school: SchoolModel):
        exists_school = await self.school_dao.get_school_by_school_name(
            school.school_name)
        if exists_school:
            raise Exception(f"学校{school.school_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        school_db = view_model_to_orm_model(school, School,    exclude=["id"])

        school_db.status =  PlanningSchoolStatus.DRAFT.value
        school_db.created_uid = 0
        school_db.updated_uid = 0

        school_db = await self.school_dao.add_school(school_db)
        school = orm_model_to_view_model(school_db, SchoolKeyAddInfo, exclude=["created_at",'updated_at'])
        return school

    async def update_school(self, school,ctype=1):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校{school.id}不存在")
        if ctype==1:
            school_db = School()
            school_db.id = school.id
            school_db.school_no = school.school_no
            school_db.school_name = school.school_name
            school_db.block = school.block
            school_db.borough = school.borough
            school_db.school_type = school.school_type
            school_db.school_operation_type = school.school_operation_type
            school_db.school_operation_type_lv2 = school.school_operation_type_lv2
            school_db.school_operation_type_lv3 = school.school_operation_type_lv3
            school_db.school_org_type = school.school_org_type
            school_db.school_level = school.school_level
        else:
            school_db = School()
            school_db.id = school.id
            school_db.school_name=school.school_name
            school_db.school_short_name=school.school_short_name
            school_db.school_code=school.school_code
            school_db.create_school_date=school.create_school_date
            school_db.founder_type=school.founder_type
            school_db.founder_name=school.founder_name
            school_db.urban_rural_nature=school.urban_rural_nature
            school_db.school_operation_type=school.school_operation_type
            school_db.school_org_form=school.school_org_form
            school_db.school_operation_type_lv2=school.school_operation_type_lv2
            school_db.school_operation_type_lv3=school.school_operation_type_lv3
            school_db.department_unit_number=school.department_unit_number
            school_db.sy_zones=school.sy_zones
            school_db.historical_evolution=school.historical_evolution


        school_db = await self.school_dao.update_school(school_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school_db

    async def update_school_byargs(self, school,ctype=1):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校{school.id}不存在")
        need_update_list = []
        for key, value in school.dict().items():
            if value:
                need_update_list.append(key)

        school_db = await self.school_dao.update_school_byargs(school, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school_db

    async def delete_school(self, school_id):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"学校{school_id}不存在")
        school_db = await self.school_dao.delete_school(exists_school)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school

    async def softdelete_school(self, school_id):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"学校{school_id}不存在")
        school_db = await self.school_dao.softdelete_school(exists_school)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db

    async def get_all_schools(self):
        return await self.school_dao.get_all_schools()

    async def get_school_count(self):
        return await self.school_dao.get_school_count()

    async def query_school_with_page(self, page_request: PageRequest, school_name=None,
                                              school_id=None,school_no=None ):
        paging = await self.school_dao.query_school_with_page(school_name, school_id,school_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SchoolModel)
        return paging_result


    async def update_school_status(self, school_id, status):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"学校{school_id}不存在")
        school_db = await self.school_dao.update_school_status(exists_school,status)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db



    async def query_schools(self,planning_school_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(School).where(School.school_name.like(f'{planning_school_name}%') ))
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, SchoolModel)

            # account = PlanningSchool(school_id=row.school_id,
            #                  grade_no=row.grade_no,
            #                  grade_name=row.grade_name,
            #                  grade_alias=row.grade_alias,
            #                  description=row.description)
            lst.append(planning_school)
        return lst