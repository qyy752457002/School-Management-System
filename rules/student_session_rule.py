import copy
from datetime import date, datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from models.student_session import StudentSession
from rules.common.common_rule import send_orgcenter_request
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model, convert_dates_to_strings
from views.models.students import StudentSession as StudentSessionModel


@dataclass_inject
class StudentSessionRule(object):
    student_session_dao: StudentSessionDao
    school_dao: SchoolDAO

    async def get_student_session_by_id(self, session_id):
        """
        获取单个类别
        """
        session_db = await self.student_session_dao.get_student_session_by_id(session_id)
        session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        convert_snowid_in_model(session, ["id", 'student_id', 'school_id', 'class_id', 'session_id'])

        return session




    async def add_student_session(self, session: StudentSession):
        """
        新增类别
        """
        session_db = view_model_to_orm_model(session, StudentSession, exclude=["session_id"])
        session_db.session_id = SnowflakeIdGenerator(1, 1).generate_id()
        session_db = await self.student_session_dao.add_student_session(session_db)
        session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        convert_snowid_in_model(session, ["id", 'student_id', 'school_id', 'class_id', 'session_id'])
        # 发送组织中心
        # await self.send_org_to_org_center(session_db)
        return session

    async def update_student_session(self, session):
        """
        编辑类别
        """
        exists_session = await self.student_session_dao.get_student_session_by_id(session.session_id)
        if not exists_session:
            raise Exception(f"编号为{session.session_id}类别不存在")
        need_update_list = []
        for key, value in session.dict().items():
            if value:
                need_update_list.append(key)
        session = await self.student_session_dao.update_student_session(session, *need_update_list)
        convert_snowid_in_model(session, ["id", 'student_id', 'school_id', 'class_id', 'session_id'])
        return session

    async def delete_student_session(self, session_id):
        """
        删除类别
        """
        exists_session = await self.student_session_dao.get_student_session_by_id(session_id)
        if not exists_session:
            raise Exception(f"编号为{session_id}类别不存在")
        session_db = await self.student_session_dao.delete_student_session(exists_session)
        return session_db

    async def get_all_student_sessions(self):
        """
        获取所有类别
        """
        session_db = await self.student_session_dao.get_all_student_sessions()
        # session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        return session_db

    async def get_student_session_count(self):
        """
        获取类别数量
        """
        count = await self.student_session_dao.get_student_session_count()
        return count

    async def query_session_with_page(self, page_request: PageRequest, status, session_name, session_alias):

        paging = await self.student_session_dao.query_session_with_page(page_request, status, session_name,
                                                                        session_alias)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, StudentSessionModel)
        convert_snowid_to_strings(paging_result, ["id", 'student_id', 'school_id', 'class_id', 'session_id'])
        return paging_result

    async def send_org_to_org_center(self, exists_planning_school_origin: StudentSession):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        school = await self.school_dao.get_school_by_id(exists_planning_school.school_id)
        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "createdTime": '',
            "displayName": exists_planning_school.session_name,
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
            "name": exists_planning_school.session_name,
            "newCode": exists_planning_school.session_alias,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,
            "parentId": '',
            "parentName": "",
            "tags": [
                ""
            ],
            "title": exists_planning_school.session_name,
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
