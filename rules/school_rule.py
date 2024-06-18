# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
import hashlib

import shortuuid
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select, or_

from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.enum_value_dao import EnumValueDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.school_dao import SchoolDAO
from models.planning_school import PlanningSchool
from models.school import School
from rules.enum_value_rule import EnumValueRule
from views.models.extend_params import ExtendParams
# from rules.planning_school_rule import PlanningSchoolRule
from views.models.planning_school import PlanningSchoolStatus
from views.models.school import School as SchoolModel, SchoolKeyAddInfo

from views.models.school import SchoolBaseInfo
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus


@dataclass_inject
class SchoolRule(object):
    school_dao: SchoolDAO
    p_school_dao: PlanningSchoolDAO
    enum_value_dao: EnumValueDAO

    async def get_school_by_id(self, school_id,extra_model=None):
        school_db = await self.school_dao.get_school_by_id(school_id)
        # 可选 , exclude=[""]
        if not school_db:
            return None
        if extra_model:
            school = orm_model_to_view_model(school_db, extra_model)

            # planning_school_extra = orm_model_to_view_model(planning_school_db, extra_model,
            #                                                 exclude=[""])
            # return planning_school,planning_school_extra

        else:

            # return planning_school
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
        if school.planning_school_id>0 :
            # rule互相应用有问题  用dao
            p_exists_school_model = await self.p_school_dao.get_planning_school_by_id(  school.planning_school_id)
            if not p_exists_school_model:
                raise PlanningSchoolNotFoundError()
            print(p_exists_school_model,999)

            p_exists_school = orm_model_to_view_model(p_exists_school_model, PlanningSchoolModel)
            print(p_exists_school)


        # await school_rule.add_school_from_planning_school(exists_planning_school)
        #     p_exists_school = await p_school_rule.get_planning_school_by_id(
        #         school.planning_school_id)
            if p_exists_school:

                # 办学者
                school_db.school_type = p_exists_school.planning_school_type
                school_db.school_edu_level = p_exists_school.planning_school_edu_level
                school_db.school_category = p_exists_school.planning_school_category
                school_db.school_operation_type = p_exists_school.planning_school_operation_type

                school_db.school_nature = p_exists_school.planning_school_nature
                school_db.school_org_type = p_exists_school.planning_school_org_type
                school_db.school_org_form = p_exists_school.planning_school_org_form
                school_db.founder_type = p_exists_school.founder_type
                school_db.founder_type_lv2 = p_exists_school.founder_type_lv2
                school_db.founder_type_lv3 = p_exists_school.founder_type_lv3
                school_db.founder_name = p_exists_school.founder_name
                school_db.founder_code = p_exists_school.founder_code
                # school_db.urban_rural_nature = p_exists_school.planning_school_urban_rural_nature

        school_db = await self.school_dao.add_school(school_db)
        school = orm_model_to_view_model(school_db, SchoolKeyAddInfo, exclude=["created_at",'updated_at'])
        return school


    async def add_school_from_planning_school(self, planning_school: PlanningSchool):
        # todo 这里的值转换 用 数据库db类型直接赋值  模型转容易报错   另 其他2个表的写入
        return None
        school = orm_model_to_view_model(planning_school, SchoolKeyAddInfo, exclude=["id"])
        school.school_name = planning_school.planning_school_name
        school.planning_school_id = planning_school.id

        school.school_no = planning_school.planning_school_no
        school.borough = planning_school.borough
        school.block = planning_school.block
        school.school_type = planning_school.planning_school_type
        school.school_edu_level = planning_school.planning_school_edu_level
        school.school_category = planning_school.planning_school_category
        school.school_operation_type = planning_school.planning_school_operation_type
        school.school_org_type = planning_school.planning_school_org_type
        school.school_level = planning_school.planning_school_level
        school.school_code = planning_school.planning_school_code

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
        print(school_db)

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
            school_db.school_edu_level = school.school_edu_level
            school_db.school_category = school.school_category
            school_db.school_operation_type = school.school_operation_type
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
            school_db.school_edu_level=school.school_edu_level
            school_db.school_org_form=school.school_org_form
            school_db.school_category=school.school_category
            school_db.school_operation_type=school.school_operation_type
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
        if exists_school.status== PlanningSchoolStatus.DRAFT.value:
            exists_school.status= PlanningSchoolStatus.OPENING.value
            school.status= PlanningSchoolStatus.OPENING.value
        else:
            pass

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

    async def query_school_with_page(self, page_request: PageRequest,   school_name,school_no,school_code,
                                     block,school_level,borough,status,founder_type,
                                     founder_type_lv2,
                                     founder_type_lv3,planning_school_id,province,city ):
        #  根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res= await enum_value_rule.get_next_level_enum_values('founder_type'  ,founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)


            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if len(founder_type_lv2)>0:
            founder_type_lv3_res= await enum_value_rule.get_next_level_enum_values('founder_type_lv2'  ,founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.school_dao.query_school_with_page(page_request,  school_name,school_no,school_code,
                                                                block,school_level,borough,status,founder_type,
                                                                founder_type_lv2,
                                                                founder_type_lv3,planning_school_id,province,city
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SchoolModel)
        return paging_result


    async def update_school_status(self, school_id, status,action=None):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"学校{school_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_school.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_school.status,2222222)
        school_db = await self.school_dao.update_school_byargs(exists_school,*need_update_list)


        # school_db = await self.school_dao.update_school_status(exists_school,status)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db



    async def query_schools(self,planning_school_name,extend_params:ExtendParams|None):

        session = await db_connection_manager.get_async_session("default", True)
        query = select(School).where(School.school_name.like(f'%{planning_school_name}%') )
        # print(extend_params,3333333333)
        if extend_params:
            if extend_params.school_id:
                query = query.where(School.id == int(extend_params.school_id)  )
            if extend_params.planning_school_id:
                query = query.where(School.planning_school_id == int(extend_params.planning_school_id)  )

            if extend_params.county_name:
                # 区的转换   or todo
                # enuminfo = await self.enum_value_dao.get_enum_value_by_value(extend_params.county_id, 'country' )
                query = query.filter( or_( School.block == extend_params.county_name , School.borough == extend_params.county_name))


                # if enuminfo:
                pass
            if extend_params.system_type:
                pass

        result = await session.execute(query)
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