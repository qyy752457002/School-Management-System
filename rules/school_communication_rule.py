# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.entities import BaseDBModel
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.school_communication import SchoolCommunicationNotFoundError
from daos.school_communication_dao import SchoolCommunicationDAO
from models.school_communication import SchoolCommunication
from views.models.planning_school import PlanningSchool
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.school_communications import SchoolCommunications  as SchoolCommunicationModel



@dataclass_inject
class SchoolCommunicationRule(object):
    school_communication_dao: SchoolCommunicationDAO
    # 定义映射关系 orm到视图的映射关系
    other_mapper={"school_web_url": "website_url",

                  }

    async def get_school_communication_by_id(self, school_communication_id,extra_model=None):
        school_communication_db = await self.school_communication_dao.get_school_communication_by_id(school_communication_id)
        # 可选 , exclude=[""]
        if extra_model:
            school = orm_model_to_view_model(school_communication_db, extra_model,other_mapper=self.other_mapper)
        else:
            school = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel)
        return school
    async def get_school_communication_by_school_id(self, school_communication_id,extra_model=None):
        school_communication_db = await self.school_communication_dao.get_school_communication_by_school_id(school_communication_id)
        if not school_communication_db:
            return None
        # 可选 , exclude=[""]
        if extra_model:
            school = orm_model_to_view_model(school_communication_db, extra_model,other_mapper=self.other_mapper)
        else:
            school = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel)
        return school

    async def add_school_communication(self, school: SchoolCommunicationModel,convertmodel=True):
        exists_school = await self.school_communication_dao.get_school_communication_by_school_id(
            school.school_id)
        if exists_school:
            raise Exception(f"学校通信信息{school.school_id}已存在")


        if convertmodel:
            school_communication_db = view_model_to_orm_model(school, SchoolCommunication,    exclude=["id"])

        else:
            school_communication_db = SchoolCommunication()
            school_communication_db.id = None
            school_communication_db.school_id= school.school_id

        school_communication_db.deleted = 0
        school_communication_db.status = '正常'
        school_communication_db.created_uid = 0
        school_communication_db.updated_uid = 0
        school_communication_db.id = SnowflakeIdGenerator(1, 1).generate_id()


        school_communication_db = await self.school_communication_dao.add_school_communication(school_communication_db)
        school = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel, exclude=["created_at",'updated_at'])
        return school

    async def update_school_communication(self, school,ctype=1):
        exists_school = await self.school_communication_dao.get_school_communication_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校通信信息{school.id}不存在")
        if ctype==1:
            school_communication_db = SchoolCommunication()
            school_communication_db.id = school.id
            school_communication_db.school_communication_no = school.school_communication_no
            school_communication_db.school_communication_name = school.school_communication_name
            school_communication_db.block = school.block
            school_communication_db.borough = school.borough
            school_communication_db.school_communication_type = school.school_communication_type
            school_communication_db.school_communication_operation_type = school.school_communication_operation_type
            school_communication_db.school_communication_operation_type_lv2 = school.school_communication_operation_type_lv2
            school_communication_db.school_communication_operation_type_lv3 = school.school_communication_operation_type_lv3
            school_communication_db.school_communication_org_type = school.school_communication_org_type
            school_communication_db.school_communication_level = school.school_communication_level
        else:
            school_communication_db = SchoolCommunication()
            school_communication_db.id = school.id
            school_communication_db.school_communication_name=school.school_communication_name
            school_communication_db.school_communication_short_name=school.school_communication_short_name
            school_communication_db.school_communication_code=school.school_communication_code
            school_communication_db.create_school_communication_date=school.create_school_communication_date
            school_communication_db.founder_type=school.founder_type
            school_communication_db.founder_name=school.founder_name
            school_communication_db.urban_rural_nature=school.urban_rural_nature
            school_communication_db.school_communication_operation_type=school.school_communication_operation_type
            school_communication_db.school_communication_org_form=school.school_communication_org_form
            school_communication_db.school_communication_operation_type_lv2=school.school_communication_operation_type_lv2
            school_communication_db.school_communication_operation_type_lv3=school.school_communication_operation_type_lv3
            school_communication_db.department_unit_number=school.department_unit_number
            school_communication_db.sy_zones=school.sy_zones
            school_communication_db.historical_evolution=school.historical_evolution


        school_communication_db = await self.school_communication_dao.update_school_communication(school_communication_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel, exclude=[""])
        return school_communication_db

    async def softdelete_school_communication(self, school_communication_id):
        exists_school = await self.school_communication_dao.get_school_communication_by_id(school_communication_id)
        if not exists_school:
            raise Exception(f"学校通信信息{school_communication_id}不存在")
        school_communication_db = await self.school_communication_dao.softdelete_school_communication(exists_school)
        # school = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel, exclude=[""],)
        return school_communication_db


    async def get_school_communication_count(self):
        return await self.school_communication_dao.get_school_communication_count()

    async def query_school_communication_with_page(self, page_request: PageRequest, school_communication_name=None,
                                              school_communication_id=None,school_communication_no=None ):
        paging = await self.school_communication_dao.query_school_communication_with_page(school_communication_name, school_communication_id,school_communication_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SchoolCommunicationModel)
        return paging_result




    async def update_school_communication_byargs(self, school_communication,):
        school_communication.school_id= int(school_communication.school_id)
        if school_communication.school_id>0:
            exists_school_communication = await self.school_communication_dao.get_school_communication_by_school_id(school_communication.school_id)

        else:

            exists_school_communication = await self.school_communication_dao.get_school_communication_by_id(school_communication.id)
        if not exists_school_communication:
            raise SchoolCommunicationNotFoundError()
        need_update_list = []
        for key, value in school_communication.dict().items():
            if value and key!='id':
                need_update_list.append(key)

        school_communication_db = await self.school_communication_dao.update_school_communication_byargs(school_communication, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        return school_communication_db
    async def add_school_communication_from_planning_school(self, planning_school: PlanningSchoolCommunications,school_res):
        # todo 这里的值转换 用 数据库db类型直接赋值  模型转容易报错   另 其他2个表的写入  检查是否原有的  防止重复新增
        # return None

        # schooldatabaseinfo = SchoolBaseInfoOptional(**planning_school.__dict__)
        dicta = planning_school.__dict__
        dicta['school_id'] = school_res.id

        school = SchoolCommunicationModel(** dicta)
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

        return await self.add_school_communication(school)



