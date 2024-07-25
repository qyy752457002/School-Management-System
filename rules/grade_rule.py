import copy
from datetime import datetime, date
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select
from business_exceptions.grade import GradeAlreadyExistError, GradeNotFoundError
from daos.enum_value_dao import EnumValueDAO
from daos.grade_dao import GradeDAO
from daos.school_dao import SchoolDAO
from models.grade import Grade
from rules.common.common_rule import send_orgcenter_request
from rules.enum_value_rule import EnumValueRule
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model, convert_dates_to_strings
from views.models.grades import Grades as GradeModel
from views.models.system import GRADE_ENUM_KEY, DISTRICT_ENUM_KEY


@dataclass_inject
class GradeRule(object):
    grade_dao: GradeDAO
    school_dao: SchoolDAO
    async def get_grade_by_id(self, grade_id):
        grade_db = await self.grade_dao.get_grade_by_id(grade_id)
        # 可选 , exclude=[""]
        grade = orm_model_to_view_model(grade_db, GradeModel)
        convert_snowid_in_model(grade, ["id", "school_id",])
        return grade

    async def get_grade_by_grade_name(self, grade_name):
        grade_db = await self.grade_dao.get_grade_by_grade_name(grade_name)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def add_grade(self, grade: GradeModel,obj=None):
        exists_grade = await self.grade_dao.get_grade_by_grade_name(grade.grade_name,grade)
        if exists_grade:
            raise GradeAlreadyExistError()
        # 校验 枚举值
        enum_value_rule = get_injector(EnumValueRule)
        # await enum_value_rule.check_enum_values(GRADE_ENUM_KEY,grade.grade_type)

        grade_db = view_model_to_orm_model(grade, Grade,    exclude=["id"])
        grade_db.created_at =   datetime.now()
                                 # .strftime("%Y-%m-%d %H:%M:%S"))
        grade_db.id = SnowflakeIdGenerator(1, 1).generate_id()
        grade_db_res = await self.grade_dao.add_grade(grade_db)
        grade_res = orm_model_to_view_model(grade_db_res, GradeModel, exclude=[""])

        #  市级添加  自动传递到 区级 自动到 校
        auto_gen= False
        if auto_gen and  grade.city:
            # 区的转换   or todo
            districts =await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY,grade.city)
            print('区域',districts, '')
            for district in districts:
                grade_db = view_model_to_orm_model(grade, Grade,    exclude=["id"])
                grade_db.created_at =   datetime.now()
                grade_db.district = district.enum_value
                grade_db.id = SnowflakeIdGenerator(1, 1).generate_id()


                await self.grade_dao.add_grade(grade_db)
        convert_snowid_in_model(grade_res, ["id", "school_id",])
        # 发送组织中心
        await self.send_org_to_org_center(grade_db )
        return grade_res

    async def update_grade(self, grade):
        if isinstance(grade.id,tuple) or not grade.id>0:
            raise GradeNotFoundError()
        exists_grade = await self.grade_dao.get_grade_by_id(grade.id)
        if not exists_grade:
            raise GradeNotFoundError()


        need_update_list = []
        for key, value in grade.dict().items():
            if value:
                need_update_list.append(key)

        print(need_update_list,222,grade)
        grade_db = await self.grade_dao.update_grade_byargs(grade,*need_update_list)
        # gradev = orm_model_to_view_model(grade_db, GradeModel,  )
        convert_snowid_in_model(grade, ["id", "school_id",])
        return grade

    async def delete_grade(self, grade_id):
        exists_grade = await self.grade_dao.get_grade_by_id(grade_id)
        if not exists_grade:
            raise GradeNotFoundError()


        grade_db = await self.grade_dao.delete_grade(exists_grade)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        convert_snowid_in_model(grade, ["id", "school_id",])
        return grade

    async def softdelete_grade(self, grade_id):
        exists_grade = await self.grade_dao.get_grade_by_id(grade_id)
        if not exists_grade:
            raise GradeNotFoundError()


        grade_db = await self.grade_dao.softdelete_grade(exists_grade)
        return grade_db

    async def get_all_grades(self):
        return await self.grade_dao.get_all_grades()

    async def get_grade_count(self):
        return await self.grade_dao.get_grade_count()

    async def query_grade_with_page(self,  page_request: PageRequest,grade_name=None,school_id=None,city='', district=''):
        paging = await self.grade_dao.query_grade_with_page(grade_name,school_id, page_request,city, district)
        # 字段映射的示例写法
        paging_result = PaginatedResponse.from_paging(paging, GradeModel)
        convert_snowid_to_strings(paging_result, ["id", "school_id",])

        return paging_result



    async def query_grade(self,grade_name,extendparams=None):

        session = await db_connection_manager.get_async_session("default", True)
        query =select(Grade).where(Grade.grade_name.like(f'%{grade_name}%') ).where(Grade.is_deleted == False)
        if extendparams:
            if extendparams.school_id:
                query = query.where(Grade.school_id == int(extendparams.school_id))
            if extendparams.city:
                query = query.where(Grade.city == extendparams.city)
            if extendparams.county_id :
                query = query.where(Grade.district == extendparams.county_id)

        result = await session.execute(query)
        res= result.scalars().all()

        lst = []
        for row in res:
            item = orm_model_to_view_model(row, GradeModel)
            convert_snowid_in_model(item, ["id", "school_id",])
            lst.append(item)
        return lst
    async def send_org_to_org_center(self, exists_planning_school_origin: Grade):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        school = await self.school_dao.get_school_by_id(exists_planning_school.school_id)
        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "createdTime": '',
            "displayName": exists_planning_school.grade_name,
            "educateUnit": school.school_name,
            "educateUnitObj": {
                "administrativeDivisionCity": "",
                "administrativeDivisionCounty": "",
                "administrativeDivisionProvince": "",
                "createdTime": school.created_at,
                "departmentObjs": [],
                "locationAddress": "",
                "locationCity": "",
                "locationCounty": "",
                "locationProvince": "",
                "owner": "",
                "unitCode": school.school_no,
                "unitId": "",
                "unitName": school.school_name,
                "unitType": "",
                "updatedTime": school.updated_at
            },
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": True,
            "key": "sit",
            "manager": "",
            "name": exists_planning_school.grade_name,
            "newCode": exists_planning_school.grade_no,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,
            "parentId": '',
            "parentName": "",
            "tags": [
                ""
            ],
            "title": exists_planning_school.grade_name,
            "type": "",
            "updatedTime": ''
        }

        apiname = '/api/add-group'
        # 字典参数
        datadict = dict_data
        if isinstance(datadict['createdTime'], (date, datetime)):
            datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")

        datadict = convert_dates_to_strings(datadict)
        print(datadict, '字典参数')

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print(response)

            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

