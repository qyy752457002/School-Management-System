# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import datetime
from datetime import date

from fastapi import Query
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from daos.class_dao import ClassesDAO
from daos.grade_dao import GradeDAO
from daos.school_dao import SchoolDAO
from daos.student_transaction_dao import StudentTransactionDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.student_transaction import StudentTransaction, TransactionDirection
from models.students import StudentApprovalAtatus
from views.models.student_transaction import StudentEduInfo as StudentTransactionModel, StudentEduInfo, \
    StudentEduInfoOut, StudentTransactionStatus
from views.models.students import StudentsBaseInfo


@dataclass_inject
class StudentTransactionRule(object):
    student_transaction_dao: StudentTransactionDAO
    students_baseinfo_dao: StudentsBaseInfoDao
    students_dao: StudentsDao

    class_dao: ClassesDAO
    grade_dao: GradeDAO
    school_dao: SchoolDAO

    async def get_student_transaction_by_id(self, student_transaction_id)->StudentTransactionModel:
        student_transaction_db = await self.student_transaction_dao.get_studenttransaction_by_id(student_transaction_id)
        # 可选 , exclude=[""]
        print(vars(student_transaction_db))
        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel,other_mapper={"student_no": "edu_number",})

        return student_transaction

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

        baseinfo = orm_model_to_view_model(baseinfo2[0], StudentEduInfo, exclude=[""],
                                           other_mapper={"major_name": "major_name", })

        return baseinfo

    async def get_student_transaction_by_student_transaction_name(self, student_transaction_name):
        student_transaction_db = await self.student_transaction_dao.get_studenttransaction_by_studenttransaction_name(
            student_transaction_name)
        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""])
        return student_transaction

    async def add_student_transaction(self, student_transaction,
                                      direction=TransactionDirection.IN.value, relation_id=0):
        relation_id = int(relation_id)
        #   根据ID  兆 name

        if student_transaction.grade_id:
            classinfo = await self.grade_dao.get_grade_by_id(student_transaction.grade_id)
            if classinfo:
                student_transaction.grade_name = classinfo.grade_name
        if student_transaction.school_id:
            classinfo = await self.school_dao.get_school_by_id(student_transaction.school_id)
            if classinfo:
                student_transaction.school_name = classinfo.school_name

        # 定义 视图和model的映射关系

        original_dict_map_view_orm = {

        }
        if direction == TransactionDirection.OUT.value:
            original_dict_map_view_orm = {

            }
        exclude = []

        if int(relation_id) > 0:
            # exclude=[]
            exclude = ["id"]

        else:
            # student_transaction_db = StudentTransaction()
            exclude = ["id"]

        for key, value in student_transaction.__dict__.items():
            if isinstance(value, tuple):
                exclude.append(key)

        student_transaction_db = view_model_to_orm_model(student_transaction, StudentTransaction,
                                                          exclude=exclude,other_mapper={"classes": "classes",})
        # student_transaction_db = StudentTransaction()
        # todo 读取 当前操作的老师 token 
        student_transaction_db.apply_user  ='xxx'
        student_transaction_db.direction = direction
        student_transaction_db.relation_id = int(relation_id)
        if isinstance(student_transaction.grade_id,int):
            student_transaction_db.grade_id = str(student_transaction.grade_id)
        if isinstance(student_transaction.class_id,int):
            student_transaction_db.class_id = str(student_transaction.class_id)
        if isinstance(student_transaction.major_id,int):
            student_transaction_db.major_id = str(student_transaction.major_id)
        special_date =   datetime.datetime.now()

        student_transaction_db.apply_time = special_date.strftime("%Y-%m-%d %H:%M:%S")
        if student_transaction.class_id:
            classinfo = await self.class_dao.get_classes_by_id(student_transaction.class_id)
            if classinfo:
                student_transaction_db.classes = classinfo.class_name


        student_transaction_db = await self.student_transaction_dao.add_studenttransaction(student_transaction_db)
        # todo

        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}
        student_transaction_db.edu_number=''
        # print(student_transaction_db)
        # print(vars(student_transaction_db))

        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""],
                                                      other_mapper=flipped_dict)
        # print(student_transaction)
        # print(vars(student_transaction))

        return student_transaction

    async def update_student_transaction(self, student_transaction):
        exists_student_transaction = await self.student_transaction_dao.get_studenttransaction_by_id(
            student_transaction.id)
        if not exists_student_transaction:
            raise Exception(f"转学申请{student_transaction.id}不存在")

        need_update_list = []
        for key, value in student_transaction.dict().items():
            if value:
                need_update_list.append(key)

        student_transaction_db = await self.student_transaction_dao.update_studenttransaction(student_transaction,
                                                                                              *need_update_list)
        # student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""])
        return student_transaction_db

    async def delete_student_transaction(self, student_transaction_id):
        exists_student_transaction = await self.student_transaction_dao.get_studenttransaction_by_id(
            student_transaction_id)
        if not exists_student_transaction:
            raise Exception(f"转学申请{student_transaction_id}不存在")
        student_transaction_db = await self.student_transaction_dao.delete_student_transaction(
            exists_student_transaction)
        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""])
        return student_transaction

    async def get_all_student_transactions(self):
        return await self.student_transaction_dao.get_all_student_transactions()

    async def get_student_transaction_count(self):
        return await self.student_transaction_dao.get_studenttransaction_count()

    async def query_student_transaction_with_page(self, page_request: PageRequest, audit_status,
                                                  student_name,
                                                  student_gender,
                                                  school_id,
                                                  apply_user,
                                                  edu_no):
        # 获取分页数据
        kdict = dict()
        if audit_status:
            kdict["status"] = audit_status.value
        if student_name:
            kdict["student_name"] = student_name
        if student_gender:
            kdict["student_gender"] = student_gender
        if school_id:
            kdict["school_id"] = school_id
        if apply_user:
            kdict["apply_user"] = apply_user
        if edu_no:
            kdict["country_no"] = edu_no

        paging = await self.student_transaction_dao.query_studenttransaction_with_page(page_request, **kdict)
        # print(2222222222222, vars(paging.items[0]))
        paging_result = PaginatedResponse.from_paging(paging, StudentEduInfoOut,other_mapper={"student_name":"student_name"})
        # print(3333333333333333,paging_result)
        return paging_result

    async def query_student_transaction(self, student_transaction_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(StudentTransaction).where(
            StudentTransaction.student_transaction_name.like(f'%{student_transaction_name}%')))
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, StudentTransactionModel)

            lst.append(planning_school)
        return lst


    async def deal_student_transaction(self, student_edu_info):
        # todo  转入  需要设置到当前学校  转出 则该状态
        res = await self.update_student_transaction(student_edu_info)
        # print(res )
        if student_edu_info.status == StudentTransactionStatus.PASS.value:
            # 入信息
            tinfo = await self.student_transaction_dao.get_studenttransaction_by_id( student_edu_info.id)

            if isinstance(tinfo, object) and hasattr(tinfo, 'relation_id') and tinfo.relation_id:
                # 出信息
                relationinfo = await self.get_student_transaction_by_id(tinfo.relation_id, )
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

        # student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""])
        return student_edu_info