from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from pydantic import BaseModel

from business_exceptions.student import StudentNotFoundError, StudentExistsError, StudentSessionNotFoundError
from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.student_session import StudentSessionstatus
from models.students import Student
from models.students_base_info import StudentBaseInfo
from rules.common.common_rule import send_orgcenter_request
from rules.students_rule import StudentsRule
from views.common.common_view import page_none_deal, convert_snowid_to_strings, convert_snowid_in_model
from views.models.students import NewBaseInfoCreate, StudentsBaseInfo
from views.models.students import NewStudentsQuery, NewStudentsQueryRe
from views.models.teachers import EducateUserModel


@dataclass_inject
class StudentsBaseInfoRule(object):
    students_base_info_dao: StudentsBaseInfoDao
    students_dao: StudentsDao
    student_session_dao: StudentSessionDao
    school_dao: SchoolDAO
    school_commu_dao: SchoolCommunicationDAO

    async def get_students_base_info_by_student_id(self, student_id)->StudentsBaseInfo:
        """
        获取单个学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_students_base_info_by_student_id(student_id)
        if not students_base_info_db:
            raise StudentNotFoundError()
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        schoolinfo = await self.school_dao.get_school_by_id(students_base_info_db.school_id)
        if schoolinfo:
            students_base_info.block = schoolinfo.block
            students_base_info.borough = schoolinfo.borough
        schoolcominfo = await self.school_commu_dao.get_school_communication_by_school_id(students_base_info_db.school_id)
        if schoolcominfo:
            students_base_info.loc_area = schoolcominfo.loc_area
            students_base_info.loc_area_pro = schoolcominfo.loc_area_pro
        convert_snowid_in_model(students_base_info, ["id",'student_id','school_id','class_id','session_id','student_base_id','grade_id'])
        if int(students_base_info.class_id)== 0    :
            students_base_info.class_id=None
        if int(students_base_info.grade_id)== 0 :
            students_base_info.grade_id=None

        return students_base_info

    async def get_students_base_info_by_id(self, students_base_id):
        """
        获取单个学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_students_base_info_by_id(students_base_id)
        if not students_base_info_db:
            raise StudentNotFoundError()
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        convert_snowid_in_model(students_base_info, ["id",'student_id','school_id','class_id','session_id','student_base_id','grade_id'])

        return students_base_info



    async def add_students_base_info(self, students_base_info: NewBaseInfoCreate):
        """
        新增学生基本信息
        """
        exits_student = await self.students_dao.get_students_by_id(students_base_info.student_id)
        if not exits_student:
            raise StudentNotFoundError()
        exits_student_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(
            students_base_info.student_id)
        if exits_student_base_info:
            raise StudentExistsError()
        students_base_info_db = view_model_to_orm_model(students_base_info, StudentBaseInfo, exclude=["student_base_id"])
        # 读取当前开启的届别  赋值
        param = {"session_status":  StudentSessionstatus.ENABLE.value}
        res  = await self.student_session_dao.get_student_session_by_param(**param)
        # session = orm_model_to_view_model(res, StudentSessionModel, exclude=[""])
        if not res or  not  res.session_id:
            raise StudentSessionNotFoundError()
            pass
        students_base_info_db.session_id = res.session_id
        students_base_info_db.session= res.session_name
        students_base_info_db.student_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        # todo 统一的方法获取学生的身份 写入 



        students_base_info_db = await self.students_base_info_dao.add_students_base_info(students_base_info_db)
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        try:

            await self.send_student_to_org_center(students_base_info,exits_student)
        except Exception as e:
            print('对接组织中心异常',e)


        return students_base_info

    async def update_students_base_info(self, students_base_info):
        """
        编辑学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(
            students_base_info.student_id)
        if not exists_students_base_info:
            raise StudentNotFoundError()
        need_update_list = []
        for key, value in students_base_info.dict().items():
            if value:
                need_update_list.append(key)
        students_base_info = await self.students_base_info_dao.update_students_base_info(students_base_info,
                                                                                         *need_update_list)
        convert_snowid_in_model(students_base_info, ["id",'student_id','school_id','class_id','session_id','student_base_id','grade_id'])

        return students_base_info

    async def update_students_class_division(self, class_id, student_ids):
        """
        编辑学生基本信息
        """

        students_base_info = await self.students_base_info_dao.update_students_class_division(class_id, student_ids)
        # 写入分班记录表
        # await self.students_dao.add_students_class_division(class_id, student_ids)
        return students_base_info

    async def delete_students_base_info(self, students_id):
        """
        删除学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(students_id)
        if not exists_students_base_info:
            raise StudentNotFoundError()
        students_base_info_db = await self.students_base_info_dao.delete_students_base_info(exists_students_base_info)
        return students_base_info_db

    async def query_students_base_info_with_page(self, query_model: NewStudentsQuery,
                                                 page_request: PageRequest,extend_params=None) -> PaginatedResponse:
        """
        分页查询
        """
        paging = await self.students_base_info_dao.query_students_with_page(query_model, page_request,extend_params)

        paging_result = PaginatedResponse.from_paging(page_none_deal(paging), NewStudentsQueryRe)
        convert_snowid_to_strings(paging_result, ["id",'student_id','school_id','class_id','session_id'])
        return paging_result

    async def get_students_base_info_count(self):
        """
        获取学生信息数量
        """
        count = await self.students_base_info_dao.get_student_base_info_count()
        return count

    # 发送学生到组织中心 todo 调试
    async def send_student_to_org_center(self, student_baseinfo:StudentsBaseInfo|BaseModel,exits_student:Student):
        # teacher_db = await self.teachers_dao.get_teachers_arg_by_id(teacher_id)
        # data_dict = to_dict(teacher_db)
        # print(data_dict)
        # convert_snowid_in_model()
        student_rule = get_injector(StudentsRule)
        psr = await student_rule.init_enum_value()
        await psr.convert_import_format_to_view_model(student_baseinfo)
        school = await self.school_dao.get_school_by_id(student_baseinfo.school_id)


        dict_data = EducateUserModel(**student_baseinfo.__dict__,
                                     currentUnit=student_baseinfo.school,
                                     # createdTime= student_baseinfo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     # updatedTime=student_baseinfo.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     name=exits_student.student_name,
                                     userCode=student_baseinfo.student_number,
                                     userId=student_baseinfo.student_id,
                                     phoneNumber= '',
                                     # departmentId="基础信息管理系统",
                                     #不同于老师显示的  基础系统名字 可能不一定准确  这里暂时用班级试试
                                     departmentId=student_baseinfo.class_id,
                                     departmentName=student_baseinfo.class_id,
                                     gender= exits_student.student_gender,
                                     idcard=exits_student.id_number,
                                     idcardType=exits_student.id_type,
                                     realName=exits_student.student_name,
                                     # 组织和主单位 确保学校已经对接进去了
                                     owner=school.school_no,
                                     mainUnitName=school.school_no,
                                     # identity=student_baseinfo.identity,
                                     identityTypeNames=student_baseinfo.identity_type,

                                     )
        params_data = dict_data.__dict__
        # params_data = JsonUtils.dict_to_json_str(dict_data)
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