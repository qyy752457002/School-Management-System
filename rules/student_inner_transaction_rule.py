# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from datetime import datetime

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

# from business_exceptions.student_inner_transaction import StudentInnerTransactionAlreadyExistError
from daos.student_inner_transaction_dao import StudentInnerTransactionDAO
from models.student_inner_transaction import StudentInnerTransaction
from rules.student_transaction import StudentTransactionRule
from views.models.student_inner_transaction import StudentInnerTransactionRes as StudentInnerTransactionModel, \
    StudentInnerTransactionRes


@dataclass_inject
class StudentInnerTransactionRule(object):
    student_inner_transaction_dao: StudentInnerTransactionDAO

    async def get_student_inner_transaction_by_id(self, student_inner_transaction_id):
        student_inner_transaction_db = await self.student_inner_transaction_dao.get_student_inner_transaction_by_id(student_inner_transaction_id)
        # 可选 , exclude=[""]
        student_inner_transaction = orm_model_to_view_model(student_inner_transaction_db, StudentInnerTransactionModel)
        return student_inner_transaction

    async def get_student_inner_transaction_by_student_inner_transaction_name(self, student_inner_transaction_name):
        student_inner_transaction_db = await self.student_inner_transaction_dao.get_student_inner_transaction_by_student_inner_transaction_name(student_inner_transaction_name)
        student_inner_transaction = orm_model_to_view_model(student_inner_transaction_db, StudentInnerTransactionModel, exclude=[""])
        return student_inner_transaction

    async def add_student_inner_transaction(self, student_inner_transaction: StudentInnerTransactionModel):
        # exists_student_inner_transaction = await self.student_inner_transaction_dao.get_student_inner_transaction_by_student_inner_transaction_name(student_inner_transaction.student_inner_transaction_name)
        # if exists_student_inner_transaction:
        #     raise StudentInnerTransactionAlreadyExistError()
        # student_inner_transaction_db = StudentInnerTransaction()
        # student_inner_transaction_db.student_inner_transaction_name = student_inner_transaction.student_inner_transaction_name
        # student_inner_transaction_db.school_id = student_inner_transaction.school_id
        # student_inner_transaction_db.student_inner_transaction_no = student_inner_transaction.student_inner_transaction_no
        # student_inner_transaction_db.student_inner_transaction_alias = student_inner_transaction.student_inner_transaction_alias
        # student_inner_transaction_db.description = student_inner_transaction.description
        student_inner_transaction_db = view_model_to_orm_model(student_inner_transaction, StudentInnerTransaction,    exclude=["id"])
        student_inner_transaction_db.created_at =   datetime.now()
                                 # .strftime("%Y-%m-%d %H:%M:%S"))
        stutran= get_injector(StudentTransactionRule)

        student_edu_info_out = await stutran.get_student_edu_info_by_id(student_inner_transaction.student_id, )
        student_inner_transaction_db.school_id = int(student_edu_info_out.school_id)
        student_inner_transaction_db.class_id =  str(student_edu_info_out.class_id)

        student_inner_transaction_db = await self.student_inner_transaction_dao.add_student_inner_transaction(student_inner_transaction_db)
        student_inner_transaction = orm_model_to_view_model(student_inner_transaction_db, StudentInnerTransactionModel, exclude=["created_at",'updated_at','transaction_time'])
        return student_inner_transaction

    async def update_student_inner_transaction(self, student_inner_transaction):
        exists_student_inner_transaction = await self.student_inner_transaction_dao.get_student_inner_transaction_by_id(student_inner_transaction.id)
        if not exists_student_inner_transaction:
            raise Exception(f"年级{student_inner_transaction.id}不存在")

        need_update_list = []
        for key, value in student_inner_transaction.dict().items():
            if value:
                need_update_list.append(key)


        student_inner_transaction_db = await self.student_inner_transaction_dao.update_student_inner_transaction_byargs(exists_student_inner_transaction,*need_update_list)
        student_inner_transaction = orm_model_to_view_model(student_inner_transaction_db, StudentInnerTransactionModel, exclude=[""])
        return student_inner_transaction

    async def delete_student_inner_transaction(self, student_inner_transaction_id):
        exists_student_inner_transaction = await self.student_inner_transaction_dao.get_student_inner_transaction_by_id(student_inner_transaction_id)
        if not exists_student_inner_transaction:
            raise Exception(f"年级{student_inner_transaction_id}不存在")
        student_inner_transaction_db = await self.student_inner_transaction_dao.delete_student_inner_transaction(exists_student_inner_transaction)
        student_inner_transaction = orm_model_to_view_model(student_inner_transaction_db, StudentInnerTransactionModel, exclude=[""])
        return student_inner_transaction

    async def softdelete_student_inner_transaction(self, student_inner_transaction_id):
        exists_student_inner_transaction = await self.student_inner_transaction_dao.get_student_inner_transaction_by_id(student_inner_transaction_id)
        if not exists_student_inner_transaction:
            raise Exception(f"年级信息{student_inner_transaction_id}不存在")
        student_inner_transaction_db = await self.student_inner_transaction_dao.softdelete_student_inner_transaction(exists_student_inner_transaction)
        return student_inner_transaction_db

    async def get_all_student_inner_transactions(self):
        return await self.student_inner_transaction_dao.get_all_student_inner_transactions()

    async def get_student_inner_transaction_count(self):
        return await self.student_inner_transaction_dao.get_student_inner_transaction_count()

    async def query_student_inner_transaction_with_page(self,  page_request: PageRequest,student_inner_transaction_search ):
        paging = await self.student_inner_transaction_dao.query_student_inner_transaction_with_page(student_inner_transaction_search ,page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, StudentInnerTransactionRes, {"student_name": "student_name", "school_name": "school_name"})
        return paging_result



    async def query_student_inner_transaction(self,student_inner_transaction_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(StudentInnerTransaction).where(StudentInnerTransaction.student_inner_transaction_name.like(f'%{student_inner_transaction_name}%') ))
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, StudentInnerTransactionModel)

            lst.append(planning_school)
        return lst

