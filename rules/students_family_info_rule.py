from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from pydantic import BaseModel

from business_exceptions.student import StudentFamilyInfoNotFoundError, StudentNotFoundError, \
    StudentFamilyInfoExistsError
from daos.school_dao import SchoolDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from daos.students_family_info_dao import StudentsFamilyInfoDao
from models.students import Student
from models.students_family_info import StudentFamilyInfo
from rules.common.common_rule import send_orgcenter_request
from views.common.common_view import convert_snowid_in_model
from views.models.students import StudentsFamilyInfo as StudentsFamilyInfoModel, StudentsFamilyInfo
from views.models.students import StudentsFamilyInfoCreate
from views.models.teachers import EducateUserModel


@dataclass_inject
class StudentsFamilyInfoRule(object):
    students_family_info_dao: StudentsFamilyInfoDao
    students_dao: StudentsDao
    students_base_info_dao: StudentsBaseInfoDao
    school_dao: SchoolDAO
    async def get_students_family_info_by_id(self, student_family_info_id):
        """
        获取单个学生家庭信息
        """
        students_family_info_db = await self.students_family_info_dao.get_students_family_info_by_id(
            student_family_info_id)
        if not students_family_info_db:
            raise StudentFamilyInfoNotFoundError()
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def add_students_family_info(self, students_family_info: StudentsFamilyInfoCreate):
        """
        新增学生家庭信息
        """
        # 处理前段传的健康状态是list转为str
        if isinstance(students_family_info.health_status, list):
            students_family_info.health_status = ",".join(students_family_info.health_status)
        exits_student = await self.students_dao.get_students_by_id(students_family_info.student_id)
        if not exits_student:
            raise StudentNotFoundError()
        #  去重  根据 姓名  性别  关系
        kdict = {"name": students_family_info.name, "gender": students_family_info.gender,"student_id": students_family_info.student_id,
                 "relationship": students_family_info.relationship}
        exist = await self.students_family_info_dao.get_student_family_info_by_param(**kdict)

        # print(exist)

        if exist:
            # print(exist)
            raise StudentFamilyInfoExistsError()

        students_family_info_db = view_model_to_orm_model(students_family_info, StudentFamilyInfo, exclude=[""])
        students_family_info_db.student_family_info_id = SnowflakeIdGenerator(1, 1).generate_id()
        students_family_info_db = await self.students_family_info_dao.add_students_family_info(students_family_info_db)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        convert_snowid_in_model(students_family_info,
                                ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'student_family_info_id'])
        # 家长身份 使用统一方法 todo 调试
        await self.send_student_familyinfo_to_org_center(students_family_info, exits_student)


        return students_family_info

    async def update_students_family_info(self, students_family_info):
        """
        编辑学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(
            students_family_info.student_family_info_id)
        if not exists_students_family_info:
            raise StudentFamilyInfoNotFoundError()
        need_update_list = []
        for key, value in students_family_info.dict().items():
            if value:
                need_update_list.append(key)
        students_family_info = await self.students_family_info_dao.update_students_family_info(students_family_info,
                                                                                               *need_update_list)
        convert_snowid_in_model(students_family_info,
                                ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'student_family_info_id'])

        return students_family_info

    async def delete_students_family_info(self, students_family_info_id):
        """
        删除学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(
            students_family_info_id)
        if not exists_students_family_info:
            raise StudentFamilyInfoNotFoundError()
        students_family_info_db = await self.students_family_info_dao.delete_students_family_info(
            exists_students_family_info)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        convert_snowid_in_model(students_family_info,
                                ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'student_family_info_id'])

        return students_family_info

    async def get_all_students_family_info(self, student_id):

        exits_student = await self.students_dao.get_students_by_id(student_id)
        if not exits_student:
            raise StudentFamilyInfoNotFoundError()
        student_family_info_db = await self.students_family_info_dao.get_all_students_family_info(student_id)
        student_family_info = []
        for item in student_family_info_db:
            student_family_info_model = orm_model_to_view_model(item, StudentsFamilyInfoModel)
            convert_snowid_in_model(student_family_info_model)
            student_family_info.append(student_family_info_model)

        return student_family_info
    async def send_student_familyinfo_to_org_center(self, exists_planning_school_origin:StudentsFamilyInfo|BaseModel,exits_student:Student):
        student_baseinfo=baseinfo = await self.students_base_info_dao.get_students_base_info_by_student_id(exits_student.student_id)
        # data_dict = to_dict(teacher_db)
        # print(data_dict)
        school = await self.school_dao.get_school_by_id(student_baseinfo.school_id)
        dict_data = EducateUserModel(**exists_planning_school_origin.__dict__,currentUnit=baseinfo.school,
                                     # createdTime= exists_planning_school_origin.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     # updatedTime=exists_planning_school_origin.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     name=exists_planning_school_origin.name,
                                     userCode=exists_planning_school_origin.identification_number,
                                     userId=exists_planning_school_origin.student_family_info_id,
                                     phoneNumber= exists_planning_school_origin.phone_number,
                                     # name=exits_student.student_name,
                                     # userCode=student_baseinfo.student_number,
                                     # userId=student_baseinfo.student_id,
                                     # phoneNumber= '',
                                     departmentId=student_baseinfo.class_id,
                                     departmentName=student_baseinfo.class_id,
                                     gender= exists_planning_school_origin.gender,
                                     idcard=exists_planning_school_origin.identification_number,
                                     idcardType=exists_planning_school_origin.identification_type,
                                     realName=exists_planning_school_origin.name,
                                     # 组织和主单位
                                     owner=school.school_no,
                                     mainUnitName=school.school_no,
                                     identity=exists_planning_school_origin.identity,
                                     identityTypeNames=exists_planning_school_origin.identity_type,
                                     )
        dict_data = dict_data.dict()
        params_data = JsonUtils.dict_to_json_str(dict_data)
        api_name = '/api/add-educate-user'
        # 字典参数
        datadict = params_data
        print(datadict, '参数')
        response = await send_orgcenter_request(api_name, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print(response)
            return response
        except Exception as e:
            print(e)
            raise e
            return response
        return None