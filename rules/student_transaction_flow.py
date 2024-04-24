# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from daos.student_transaction_flow_dao import StudentTransactionFlowDAO
from models.student_transaction_flow import StudentTransactionFlow
from views.models.student_transaction import StudentTransactionFlow as StudentTransactionFlowModel


@dataclass_inject
class StudentTransactionFlowRule(object):
    student_transaction_flow_dao: StudentTransactionFlowDAO

    async def get_student_transaction_flow_by_id(self, student_transaction_flow_id):
        student_transaction_flow_db = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_id(student_transaction_flow_id)
        # 可选 , exclude=[""]
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel)
        return student_transaction_flow

    async def get_student_transaction_flow_by_student_transaction_flow_name(self, student_transaction_flow_name):
        student_transaction_flow_db = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_studenttransaction_flow_name(
            student_transaction_flow_name)
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel, exclude=[""])
        return student_transaction_flow

    async def add_student_transaction_flow(self, student_transaction_flow: StudentTransactionFlowModel):
        # exists_student_transaction_flow = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_studenttransaction_flow_name(student_transaction_flow.student_transaction_flow_name)
        # if exists_student_transaction_flow:
        #     raise Exception(f"转学申请{student_transaction_flow.student_transaction_flow_name}已存在")

        # 定义 视图和model的映射关系
        original_dict_map_view_orm ={
            # "transfer_in_type": "out_type",
                                     "natural_edu_no": "country_no",
                                     "grade_name": "in_grade",
                                     "classes": "in_class",
                                     "transferin_time": "in_date",
                                     "transferin_reason": "reason",
                                     "school_id": "in_school_id",

                                     }

        student_transaction_flow_db = view_model_to_orm_model(student_transaction_flow, StudentTransactionFlow,exclude=["id"]  )
        # student_transaction_flow_db = StudentTransaction()
        # student_transaction_flow_db.direction = TransactionDirection.IN.value
        # student_transaction_flow_db.school_id = student_transaction_flow.school_id
        # student_transaction_flow_db.student_transaction_flow_no = student_transaction_flow.student_transaction_flow_no
        # student_transaction_flow_db.student_transaction_flow_alias = student_transaction_flow.student_transaction_flow_alias
        # student_transaction_flow_db.description = student_transaction_flow.description

        student_transaction_flow_db = await self.student_transaction_flow_dao.add_studenttransactionflow(student_transaction_flow_db)

        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}

        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel, exclude=[""],other_mapper= flipped_dict)
        return student_transaction_flow

    async def update_student_transaction_flow(self, student_transaction_flow):
        exists_student_transaction_flow = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_id(
            student_transaction_flow.id)
        if not exists_student_transaction_flow:
            raise Exception(f"转学申请{student_transaction_flow.id}不存在")

        need_update_list = []
        for key, value in student_transaction_flow.dict().items():
            if value:
                need_update_list.append(key)

        student_transaction_flow_db = await self.student_transaction_flow_dao.update_studenttransaction_flow(student_transaction_flow,*need_update_list)
        # student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionModel, exclude=[""])
        return student_transaction_flow_db

    async def delete_student_transaction_flow(self, student_transaction_flow_id):
        exists_student_transaction_flow = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_id(
            student_transaction_flow_id)
        if not exists_student_transaction_flow:
            raise Exception(f"转学申请{student_transaction_flow_id}不存在")
        student_transaction_flow_db = await self.student_transaction_flow_dao.delete_student_transaction_flow(
            exists_student_transaction_flow)
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel, exclude=[""])
        return student_transaction_flow

    async def get_all_student_transaction_flows(self):
        return await self.student_transaction_flow_dao.get_all_student_transaction_flows()

    async def get_student_transaction_flow_count(self):
        return await self.student_transaction_flow_dao.get_studenttransaction_flow_count()

    async def query_student_transaction_flow_with_page(self, page_request: PageRequest, student_transaction_flow_name=None,
                                                  school_id=None, ):
        paging = await self.student_transaction_flow_dao.query_studenttransaction_flow_with_page(student_transaction_flow_name,
                                                                                       school_id, page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, StudentTransactionFlowModel)
        return paging_result

    async def query_student_transaction_flow(self, student_transaction_flow_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(StudentTransactionFlow).where(
            StudentTransactionFlow.student_transaction_flow_name.like(f'%{student_transaction_flow_name}%')))
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, StudentTransactionFlowModel)

            lst.append(planning_school)
        return lst
