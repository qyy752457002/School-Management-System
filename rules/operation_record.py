from typing import List

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.operation_record import OperationRecordNotFoundError
# from business_exceptions.operation_record import OperationRecordNotFoundError
from daos.OperationRecord_dao import OperationRecordDAO
from models.operation_record import OperationRecord
from views.models.operation_record import OperationRecord as OperationRecordModel
from mini_framework.databases.conn_managers.db_manager import db_connection_manager

@dataclass_inject
class OperationRecordRule(object):
    operation_record_dao: OperationRecordDAO

    async def get_operation_record_by_id(self, operation_record_id):
        operation_record_db = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not operation_record_db:
            raise OperationRecordNotFoundError()
        # 可选 , exclude=[""]
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel)
        return operation_record

    async def get_operation_record_by_operation_record_name(self, operation_record_name):
        operation_record_db = await self.operation_record_dao.get_operation_record_by_operation_record_name(
            operation_record_name)
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""])
        return operation_record

    async def add_operation_record(self, operation_record: OperationRecordModel):
        # exists_operation_record = await self.operation_record_dao.get_operation_record_by_operation_record_name(
        #     operation_record.operation_record_name)
        # if exists_operation_record:
        #     raise Exception(f"枚举值{operation_record.operation_record_name}已存在")
        operation_record_db = view_model_to_orm_model(operation_record, OperationRecord,    exclude=["id"])
        # operation_record_db.status =  OperationRecordStatus.DRAFT.value
        operation_record_db.created_uid = 0
        operation_record_db.updated_uid = 0

        operation_record_db = await self.operation_record_dao.add_operation_record(operation_record_db)
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=["created_at",'updated_at'])
        return operation_record

    async def delete_operation_record(self, operation_record_id):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()
        operation_record_db = await self.operation_record_dao.delete_operation_record(exists_operation_record)
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""],)
        return operation_record

    async def softdelete_operation_record(self, operation_record_id):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()
        operation_record_db = await self.operation_record_dao.softdelete_operation_record(exists_operation_record)
        # operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""],)
        return operation_record_db

    async def get_all_operation_records(self):
        return await self.operation_record_dao.get_all_operation_records()

    async def get_operation_record_count(self):
        return await self.operation_record_dao.get_operation_record_count()

    async def query_operation_record_with_page(self, page_request: PageRequest,  operation_target_type,action_target_id,operater_account,
                                               operater_id,operation_module,operation_type ):
        paging = await self.operation_record_dao.query_operation_record_with_page(  page_request, operation_record_name,parent_code  )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, OperationRecordModel)
        return paging_result


    async def update_operation_record_status(self, operation_record_id, status):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()


        need_update_list = []
        need_update_list.append('status')

        print(exists_operation_record.status,2222222)
        operation_record_db = await self.operation_record_dao.update_operation_record_byargs(exists_operation_record,*need_update_list)
        # operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""],)
        return operation_record_db

    async def update_operation_record_byargs(self, operation_record,ctype=1):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record.id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()
        need_update_list = []
        for key, value in operation_record.dict().items():
            if value:
                need_update_list.append(key)


        operation_record_db = await self.operation_record_dao.update_operation_record_byargs(operation_record, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # operation_record = orm_model_to_view_model(operation_record_db, SchoolModel, exclude=[""])
        return operation_record_db


    async def query_operation_records(self,operation_record_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(OperationRecord).where(OperationRecord.operation_record_name.like(f'%{operation_record_name}%') ))
        res= result.scalars().all()
        lst = []
        for row in res:
            operation_record = orm_model_to_view_model(row, OperationRecordModel)
            lst.append(operation_record)
        return lst

    async def get_next_level_operation_records(self,operation_record_name,operation_records:List[str]):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(
            select(OperationRecord).where(OperationRecord.operation_record.in_( operation_records ) ) .where(OperationRecord.enum_name== operation_record_name )
        )

        res= result.scalars().all()
        listids=  []
        for row in res:
            # operation_record = orm_model_to_view_model(row, OperationRecordModel,exclude=["sort_number"])
            # lst.append(operation_record)
            listids.append(row.id)
        result2 = await session.execute(
            select(OperationRecord).where(OperationRecord.parent_id.in_( listids ) )
        )

        res2= result2.scalars().all()
        lst =  []
        for row in res2:
            # operation_record = orm_model_to_view_model(row, OperationRecordModel,exclude=["sort_number",'description'])
            lst.append(row)

        return lst



    async def get_operation_record_all(self, filterdict):
        return await self.operation_record_dao.get_operation_record_all(filterdict)
