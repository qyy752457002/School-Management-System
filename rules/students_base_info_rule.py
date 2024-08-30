import copy
import traceback
from datetime import date, datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from pydantic import BaseModel

from business_exceptions.student import StudentNotFoundError, StudentExistsError, StudentSessionNotFoundError
from daos.class_dao import ClassesDAO
from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.public_enum import IdentityType
from models.student_session import StudentSessionstatus
from models.students import Student
from models.students_base_info import StudentBaseInfo
from rules.common.common_rule import send_orgcenter_request, get_identity_by_job
from rules.students_rule import StudentsRule
from views.common.common_view import page_none_deal, convert_snowid_to_strings, convert_snowid_in_model
from views.models.organization import Organization
from views.models.students import NewBaseInfoCreate, StudentsBaseInfo
from views.models.students import NewStudentsQuery, NewStudentsQueryRe
from views.models.teachers import EducateUserModel
from views.models.school import SchoolKeyInfo as SchoolModel, School


@dataclass_inject
class StudentsBaseInfoRule(object):
    students_base_info_dao: StudentsBaseInfoDao
    students_dao: StudentsDao
    student_session_dao: StudentSessionDao
    school_dao: SchoolDAO
    school_commu_dao: SchoolCommunicationDAO
    classes_dao: ClassesDAO


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

            # res,param_dict = await self.send_student_to_org_center(students_base_info,exits_student)
            # await self.send_user_org_relation_to_org_center(param_dict, None, None, res)
            pass

        except Exception as e:
            print('对接组织中心异常',e)
            traceback.print_exc()


        return students_base_info

    async def update_students_base_info(self, students_base_info,origin_exist_data =None):
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
        origin_exist_data= exists_students_base_info
        print('原基本学生信息',origin_exist_data)
        if origin_exist_data is not None:
            try:
                if origin_exist_data.class_id is not None:
                    if isinstance(origin_exist_data.class_id,str):
                        origin_exist_data.class_id = int(origin_exist_data.class_id)

                    else:
                        pass
                    if origin_exist_data.class_id>0:
                        print('不处理',origin_exist_data.class_id)
                        pass
                    else:
                        print('处理')
                        studict = students_base_info.__dict__
                        studict['school_id'] = origin_exist_data.school_id
                        stuobj = StudentsBaseInfo(**studict)
                        stutableobj = await self.students_dao.get_students_by_id(stuobj.student_id)

                        # students_base_info.school_id = origin_exist_data.school_id
                        res,param_dict = await self.send_student_to_org_center(stuobj,stutableobj)
                        await self.send_user_org_relation_to_org_center(param_dict, None, None, res)

                        # origin_exi
                        # st_data.class_id = None
                else:
                    pass


                pass

            except Exception as e:
                print('对接组织中心异常',e)
                traceback.print_exc()

            pass

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
        # student_baseinfo.class_id= '7228496316651933696'
        classes  = await self.classes_dao.get_classes_by_id(student_baseinfo.class_id)
        student_baseinfo.identity_type = IdentityType.STUDENT.value
        # if school is None:
        #     print('学校未找到 跳过发送组织', school)
        #     return
        school_operation_type = []
        if school:
            school2 = orm_model_to_view_model(school, School)
            if school2.school_edu_level:
                school_operation_type.append(school2.school_edu_level)
            if school2.school_category:
                school_operation_type.append(school2.school_category)
            if school2.school_operation_type:
                school_operation_type.append(school2.school_operation_type)
        identity_type, identity = await get_identity_by_job(school_operation_type, 'student')
        student_baseinfo.identity= identity

        dict_data = EducateUserModel(**student_baseinfo.__dict__,
                                     currentUnit= school.org_center_info,
                                     # createdTime= student_baseinfo.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     # updatedTime=student_baseinfo.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     name=exits_student.student_name,
                                     userCode= str(student_baseinfo.student_id) ,
                                     userId=student_baseinfo.student_id,
                                     phoneNumber= '',
                                     # departmentId="基础信息管理系统",
                                     #不同于老师显示的  基础系统名字 可能不一定准确  这里暂时用班级试试
                                     departmentId=classes.class_name,
                                     departmentName=classes.class_name,
                                     gender= exits_student.student_gender,
                                     idcard=exits_student.id_number,
                                     idcardType=exits_student.id_type,
                                     realName=exits_student.student_name,
                                     # 组织和主单位 确保学校已经对接进去了
                                     owner=school.school_no,
                                     mainUnitName=school.school_no,
                                     # identity= '',
                                     # identityType = IdentityType.STUDENT.value,

                                     # identityTypeNames=student_baseinfo.identity_type,

                                     )
        params_data = dict_data.__dict__
        # 秘钥
        # params_data['clientId'] = 'c07ac36559b4a860d248'
        # params_data['clientSecret'] = '5445838d08a0e7b2139acf77868e858c592e09f3'
        # params_data = JsonUtils.dict_to_json_str(dict_data)
        api_name = '/api/add-educate-user'
        # 字典参数
        datadict = params_data
        print(datadict, '参数')
        response = await send_orgcenter_request(api_name, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print(response)
            return response,params_data
        except Exception as e:
            print(e)
            raise e
            return response
        return None

    async def send_user_org_relation_to_org_center(self, param_dict , res_unit,
                                                   data_org, res_admin):

        unitid = None
        userid = None
        if isinstance(res_unit, dict):
            unitid = res_unit['data2']
        if isinstance(res_admin, dict):
            userid = res_admin['data2']
        #
        dict_data = {
            "createdTime": "1989-05-20 17:50:56",
            "departmentId": param_dict['departmentId'],
            "identity":param_dict['identity'],
            "identityType": IdentityType.STUDENT.value,
            # 单位和用户ID
            # "unitId": "74",
            "userId": userid,
            "unitId":  param_dict['currentUnit'],
        }

        apiname = '/api/add-educate-user-department-identitys'
        # 字典参数 todo  调整  参数完善   另 服务范围的接口
        datadict = [dict_data]
        # datadict = convert_dates_to_strings(datadict)
        print('调用添加部门用户关系  字典参数', datadict, )

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print('调用添加部门用户关系 接口响应', response, )
        try:

            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None