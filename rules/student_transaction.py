# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from fastapi import Query
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from daos.student_transaction_dao import StudentTransactionDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from models.student_transaction import StudentTransaction, TransactionDirection
from views.models.student_transaction import StudentEduInfo as StudentTransactionModel, StudentEduInfo


@dataclass_inject
class StudentTransactionRule(object):
    student_transaction_dao: StudentTransactionDAO
    students_baseinfo_dao: StudentsBaseInfoDao

    async def get_student_transaction_by_id(self, student_transaction_id):
        student_transaction_db = await self.student_transaction_dao.get_studenttransaction_by_id(student_transaction_id)
        # 可选 , exclude=[""]
        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel)
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
        # exists_student_transaction = await self.student_transaction_dao.get_studenttransaction_by_studenttransaction_name(student_transaction.student_transaction_name)
        # if exists_student_transaction:
        #     raise Exception(f"转学申请{student_transaction.student_transaction_name}已存在")

        # 定义 视图和model的映射关系

        original_dict_map_view_orm = {
            # "natural_edu_no": "country_no",
            # "grade_name": "in_grade",
            # "classes": "in_class",
            # "transferin_time": "transfer_time",
            # "transferin_reason": "transfer_reason",
            # "school_id": "in_school_id",
        }
        if direction == TransactionDirection.OUT.value:
            original_dict_map_view_orm = {
                # "natural_edu_no": "country_no",
                # "grade_name": "out_grade",
                # "classes": "out_class",
                # "transferin_time": "transfer_time",
                # "transferin_reason": "transfer_reason",
                # "school_id": "out_school_id",
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

        # print(exclude)
        # print(student_transaction)

        student_transaction_db = view_model_to_orm_model(student_transaction, StudentTransaction,
                                                         original_dict_map_view_orm, exclude=exclude)
        # student_transaction_db = StudentTransaction()
        student_transaction_db.direction = direction
        student_transaction_db.relation_id = int(relation_id)
        # student_transaction_db.student_transaction_no = student_transaction.student_transaction_no
        # student_transaction_db.student_transaction_alias = student_transaction.student_transaction_alias
        # student_transaction_db.description = student_transaction.description

        # print(student_transaction_db)

        student_transaction_db = await self.student_transaction_dao.add_studenttransaction(student_transaction_db)

        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}

        student_transaction = orm_model_to_view_model(student_transaction_db, StudentTransactionModel, exclude=[""],
                                                      other_mapper=flipped_dict)
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
        # print(2222222222222,paging)

        # 字段映射的示例写法   , {"hash_password": "password"} other_mapper={"in_school_id": "school_id","in_grade": "grade_name",
        #                                                                                                     "in_class": "classes",
        #                                                                                                     }
        paging_result = PaginatedResponse.from_paging(paging, StudentTransactionModel)
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
