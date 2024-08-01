# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import datetime
from urllib.parse import urlencode

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from sqlalchemy import select

from business_exceptions.classes import ClassesNotFoundError
from business_exceptions.grade import GradeNotFoundError
from business_exceptions.school import SchoolNotFoundError, SchoolValidateError
from business_exceptions.student_session import StudentSessionNotFoundError
from business_exceptions.student_temporary_study import TargetSchoolError, StudentTemporaryStudyExistsError
from daos.class_dao import ClassesDAO
from daos.grade_dao import GradeDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from daos.student_temporary_study_dao import StudentTemporaryStudyDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.student_temporary_study import StudentTemporaryStudy
from models.students import StudentApprovalAtatus
from views.common.common_view import workflow_service_config, convert_snowid_to_strings, convert_snowid_in_model
from views.models.student_transaction import StudentTransactionStatus
from views.models.students import StudentsBaseInfo
from views.models.system import STUDENT_TRANSFER_WORKFLOW_CODE
from views.models.student_temporary_study import StudentTemporaryStudy as StudentTemporaryStudyModel


@dataclass_inject
class StudentTemporalStudyRule(object):
    student_temporary_study_dao: StudentTemporaryStudyDAO
    students_baseinfo_dao: StudentsBaseInfoDao
    students_dao: StudentsDao

    class_dao: ClassesDAO
    grade_dao: GradeDAO
    school_dao: SchoolDAO
    session_dao: StudentSessionDao

    async def get_student_temporary_study_by_process_instance_id(self, student_temporary_study_id):
        student_temporary_study_db = await self.student_temporary_study_dao.get_studenttransaction_by_process_instance_id(student_temporary_study_id)
        # 可选 , exclude=[""]
        # print(vars(student_temporary_study_db))
        student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel,other_mapper={"student_no": "edu_number",})

        return student_temporary_study

    async def get_student_temporary_study_by_id(self, student_temporary_study_id):
        student_temporary_study_db = await self.student_temporary_study_dao.get_studenttransaction_by_id(student_temporary_study_id)
        # 可选 , exclude=[""]
        # print(vars(student_temporary_study_db))
        student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel,other_mapper={"student_no": "edu_number",})

        return student_temporary_study

    async def get_student_edu_info_by_id(self, students_id):
        # students_db = await self.students_dao.get_students_by_id(students_id)
        # students = orm_model_to_view_model(students_db, StudentsKeyinfoDetail, exclude=[""])
        # 查其他的信息
        baseinfo2 = await self.students_baseinfo_dao.get_students_base_info_ext_by_student_id(students_id)
        # print(baseinfo2)
        # baseinfo= baseinfo2[0]
        graduation_student = baseinfo2[0]
        for key, value in graduation_student.items():
            if value is None:
                baseinfo2[0][key] = ''
            # delattr(graduation_student, key)
        print('信息',baseinfo2, type(baseinfo2[0]))
        if isinstance(baseinfo2[0], dict):
            baseinfo  =  StudentEduInfo(**baseinfo2[0])
        else:

            baseinfo = orm_model_to_view_model(baseinfo2[0], StudentEduInfo, exclude=[""],
                                           other_mapper={"major_name": "major_name", })
        # baseinfo= baseinfo2[0]

        return baseinfo

    async def get_student_temporary_study_by_student_temporary_study_name(self, student_temporary_study_name):
        student_temporary_study_db = await self.student_temporary_study_dao.get_studenttransaction_by_studenttransaction_name(
            student_temporary_study_name)
        student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel, exclude=[""])
        return student_temporary_study

    async def add_student_temporary_study(self, student_temporary_study:StudentTemporaryStudy):
        #  去重
        exists_student_temporary_study = await self.student_temporary_study_dao.get_student_temporary_study_by_args(student_id = student_temporary_study.student_id,is_deleted = False )
        if exists_student_temporary_study:
            raise StudentTemporaryStudyExistsError()
        # 检查校验数据""
        school  = await self.school_dao.get_school_by_id(student_temporary_study.school_id)
        if school is None:
            raise SchoolNotFoundError()
        session = await self.session_dao.get_student_session_by_id(student_temporary_study.session_id)
        if session is None:
            raise StudentSessionNotFoundError()
        grade = await self.grade_dao.get_grade_by_id(student_temporary_study.grade_id)
        if grade is None:
            raise GradeNotFoundError()
        classes = await self.class_dao.get_classes_by_id(student_temporary_study.class_id)
        if classes is None:
            raise ClassesNotFoundError()

        # 状态和 数据赋值
        student_temporary_study.status = StudentTransactionStatus.NEEDAUDIT.value
        baseinfo=await self.students_baseinfo_dao.get_students_base_info_by_student_id(student_temporary_study.student_id)
        if baseinfo is not None:
            student_temporary_study.origin_class_id = baseinfo.class_id
            student_temporary_study.origin_grade_id = baseinfo.grade_id
            student_temporary_study.origin_school_id = baseinfo.school_id
            student_temporary_study.origin_session_id = baseinfo.session_id
            student_temporary_study.student_no = baseinfo.student_number
            student_temporary_study.edu_number = baseinfo.edu_number


        students = await self.students_dao.get_students_by_id(student_temporary_study.student_id)
        if students is not None:
            student_temporary_study.student_gender = students.student_gender
            student_temporary_study.student_name = students.student_name
            student_temporary_study.id_number = students.id_number
        if school.id   ==baseinfo.school_id:
            raise TargetSchoolError()

        student_temporary_study_db = view_model_to_orm_model(student_temporary_study, StudentTemporaryStudy, exclude=["id"])
        student_temporary_study_db.created_uid = 0
        student_temporary_study_db.updated_uid = 0
        student_temporary_study_db.id = SnowflakeIdGenerator(1, 1).generate_id()


        student_temporary_study_db = await self.student_temporary_study_dao.add_student_temporary_study(student_temporary_study_db)
        student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTemporaryStudyModel,
                                                  exclude=["created_at", 'updated_at', ])
        # str
        convert_snowid_in_model(student_temporary_study,extra_colums=["student_id",'school_id','class_id','grade_id','session_id','origin_grade_id','origin_class_id','process_instance_id',])

        return student_temporary_study

    async def update_student_temporary_study(self, student_temporary_study):
        exists_student_temporary_study = await self.student_temporary_study_dao.get_studenttransaction_by_id(
            student_temporary_study.id)
        if not exists_student_temporary_study:
            raise Exception(f"转学申请{student_temporary_study.id}不存在")

        need_update_list = []
        for key, value in student_temporary_study.dict().items():
            if value:
                need_update_list.append(key)

        student_temporary_study_db = await self.student_temporary_study_dao.update_studenttransaction(student_temporary_study,
                                                                                              *need_update_list)
        # student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel, exclude=[""])
        return student_temporary_study_db

    async def delete_student_temporary_study(self, student_temporary_study_id):
        exists_student_temporary_study = await self.student_temporary_study_dao.get_studenttransaction_by_id(
            student_temporary_study_id)
        if not exists_student_temporary_study:
            raise Exception(f"转学申请{student_temporary_study_id}不存在")
        student_temporary_study_db = await self.student_temporary_study_dao.delete_student_temporary_study(
            exists_student_temporary_study)
        student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel, exclude=[""])
        return student_temporary_study

    async def get_all_student_temporary_studys(self):
        return await self.student_temporary_study_dao.get_all_student_temporary_studys()

    async def get_student_temporary_study_count(self):
        return await self.student_temporary_study_dao.get_studenttransaction_count()


    async def query_student_temporary_study_with_page(self, page_request: PageRequest,  status,student_name,student_gender,school_id,apply_user,edu_number):
        # 获取分页数据
        kdict = dict()
        if school_id is not None:
            if school_id.isnumeric():
                school_id = int(school_id)
            else:
                raise SchoolValidateError()
        if status:
            kdict["status"] = status.value
        if student_name:
            kdict["student_name"] = student_name
        if student_gender:
            kdict["student_gender"] = student_gender
        if school_id:
            kdict["school_id"] =  int(float(school_id))
        if apply_user:
            kdict["apply_user"] = apply_user
        if edu_number:
            kdict["edu_number"] = edu_number

        paging = await self.student_temporary_study_dao.query_student_temporary_study_with_page(page_request, **kdict)
        # print(2222222222222, vars(paging.items[0]))
        paging_result = PaginatedResponse.from_paging(paging, StudentTemporaryStudyModel, )
        # print(3333333333333333,paging_result)
        convert_snowid_to_strings(paging_result, ["id",'student_id','school_id','class_id','session_id','relation_id','process_instance_id','in_school_id','grade_id','transferin_audit_id','origin_grade_id','origin_class_id','process_instance_id'])
        #  convert_snowid_in_model(student_temporary_study,extra_colums=["student_id",'school_id','class_id','grade_id','session_id','origin_grade_id','origin_class_id','process_instance_id',])
        #
        #
        return paging_result

    async def query_student_temporary_study(self, student_temporary_study_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(StudentTransaction).where(
            StudentTransaction.student_temporary_study_name.like(f'%{student_temporary_study_name}%')))
        res = result.scalars().all()

        lst = []
        for row in res:
            student_temporary_study = orm_model_to_view_model(row, StudentTransactionModel)
            convert_snowid_in_model(student_temporary_study)

            lst.append(student_temporary_study)
        return lst


    async def deal_student_temporary_study_biz(self, student_edu_info):
        # todo  转入  需要设置到当前学校  转出 则该状态
        res = await self.update_student_temporary_study(student_edu_info)
        # print(res )
        if student_edu_info.status == StudentTransactionStatus.PASS.value:
            # 入信息
            tinfo = await self.student_temporary_study_dao.get_studenttransaction_by_id( student_edu_info.id)

            if isinstance(tinfo, object) and hasattr(tinfo, 'relation_id') and tinfo.relation_id:
                # 出信息
                relationinfo = await self.get_student_temporary_study_by_id(tinfo.relation_id, )
                pass
            if tinfo.direction == TransactionDirection.IN.value:
                # 入信息 todo 这个提取到 入的学校的方法里 预提交方法里
                students_base_info = StudentsBaseInfo(student_id=tinfo.student_id,school_id=tinfo.school_id,grade_id=tinfo.grade_id,class_id=tinfo.class_id)
                #学生的状态为 已经 入学 新的班级和学校ID

                need_update_list = ['school_id','grade_id','class_id']

                print(need_update_list,students_base_info)
                await self.students_baseinfo_dao.update_students_base_info(students_base_info,*need_update_list)
                #学生 审核态 改为已审核
                stu = await self.students_dao.get_students_by_id ( tinfo.student_id)
                stu.approval_status = StudentApprovalAtatus.ASSIGNMENT.value
                need_update_list = ['approval_status']

                await self.students_dao.update_students(stu,*need_update_list)

        # student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel, exclude=[""])
        return student_edu_info

    async def deal_student_temporary_study(self, student_edu_info):
        #   转入  需要设置到当前学校  转出 则该状态
        tinfo=await self.get_student_temporary_study_by_process_instance_id(student_edu_info.process_instance_id)
        # 入信息  这个提取到 入的学校的方法里 预提交方法里
        students_base_info = StudentsBaseInfo(student_id=tinfo.student_id,school_id=tinfo.school_id,grade_id=tinfo.grade_id,class_id=tinfo.class_id)
        #学生的状态为 已经 入学 新的班级和学校ID

        need_update_list = ['school_id','grade_id','class_id']

        print(need_update_list,students_base_info)
        await self.students_baseinfo_dao.update_students_base_info(students_base_info,*need_update_list)
        #学生 审核态 改为已审核
        stu = await self.students_dao.get_students_by_id ( tinfo.student_id)
        stu.approval_status = StudentApprovalAtatus.ASSIGNMENT.value
        need_update_list = ['approval_status']

        await self.students_dao.update_students(stu,*need_update_list)

        # student_temporary_study = orm_model_to_view_model(student_temporary_study_db, StudentTransactionModel, exclude=[""])
        return student_edu_info

    async def exist_undealed_student_temporary_study(self, student_id):
        tinfo=await self.student_temporary_study_dao.get_studenttransaction_by_student_id(student_id)
        if tinfo and  tinfo.status == StudentTransactionStatus.NEEDAUDIT.value:
            return True
        return False
