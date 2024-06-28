from datetime import datetime
from typing import List

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.operation_record import OperationRecordNotFoundError
# from business_exceptions.operation_record import OperationRecordNotFoundError
from daos.operation_record_dao import OperationRecordDAO
from models.operation_record import OperationRecord
from views.common.common_view import get_client_ip
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

    async def add_operation_record(self, operation_record: OperationRecordModel,request=None):
        # 通用的参数可以 自动获取设置
        operation_record.operation_time = datetime.now()
        if request:
            operation_record.ip = get_client_ip(request)
        if not operation_record.operator_id:
            operation_record.operator_id = 1
            operation_record.operator_name = 'admin'
        if not operation_record.process_instance_id:
            operation_record.process_instance_id = 0
        if not operation_record.status:
            operation_record.status = ''

        operation_record_db = view_model_to_orm_model(operation_record, OperationRecord, exclude=["id"])
        # operation_record_db.status =  OperationRecordStatus.DRAFT.value
        operation_record_db.created_uid = 0
        operation_record_db.updated_uid = 0

        operation_record_db = await self.operation_record_dao.add_operation_record(operation_record_db)
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel,
                                                   exclude=["created_at", 'updated_at'])
        return operation_record

    async def delete_operation_record(self, operation_record_id):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()
        operation_record_db = await self.operation_record_dao.delete_operation_record(exists_operation_record)
        operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""], )
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

    async def query_operation_record_with_page(self, page_request: PageRequest, target, action_target_id,
                                               operator_name,
                                               operator_id, change_module, action_type,process_instance_id):
        # 获取分页数据
        kdict = dict()
        if target:
            kdict["target"] = target.value
        if action_target_id:
            kdict["action_target_id"] = action_target_id
        if process_instance_id:
            kdict["process_instance_id"] = process_instance_id
        if operator_name:
            kdict["operator_name"] = operator_name
        if operator_id:
            kdict["created_uid"] = operator_id
        if change_module:
            kdict["change_module"] = change_module.value
        if action_type:
            kdict["action_type"] = action_type.value

        paging = await self.operation_record_dao.query_operation_record_with_page(page_request, **kdict)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, OperationRecordModel)
        return paging_result


    async def update_operation_record_status(self, operation_record_id, status):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record_id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()

        need_update_list = []
        need_update_list.append('status')

        print(exists_operation_record.status, 2222222)
        operation_record_db = await self.operation_record_dao.update_operation_record_byargs(exists_operation_record,
                                                                                             *need_update_list)
        # operation_record = orm_model_to_view_model(operation_record_db, OperationRecordModel, exclude=[""],)
        return operation_record_db

    async def update_operation_record_byargs(self, operation_record, ctype=1):
        exists_operation_record = await self.operation_record_dao.get_operation_record_by_id(operation_record.id)
        if not exists_operation_record:
            raise OperationRecordNotFoundError()
        need_update_list = []
        for key, value in operation_record.dict().items():
            if value:
                need_update_list.append(key)

        operation_record_db = await self.operation_record_dao.update_operation_record_byargs(operation_record,
                                                                                             *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # operation_record = orm_model_to_view_model(operation_record_db, SchoolModel, exclude=[""])
        return operation_record_db

    async def query_operation_records(self, operation_record_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(
            select(OperationRecord).where(OperationRecord.operation_record_name.like(f'%{operation_record_name}%')))
        res = result.scalars().all()
        lst = []
        for row in res:
            operation_record = orm_model_to_view_model(row, OperationRecordModel)
            lst.append(operation_record)
        return lst

    async def get_next_level_operation_records(self, operation_record_name, operation_records: List[str]):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(
            select(OperationRecord).where(OperationRecord.operation_record.in_(operation_records)).where(
                OperationRecord.enum_name == operation_record_name)
        )

        res = result.scalars().all()
        listids = []
        for row in res:
            # operation_record = orm_model_to_view_model(row, OperationRecordModel,exclude=["sort_number"])
            # lst.append(operation_record)
            listids.append(row.id)
        result2 = await session.execute(
            select(OperationRecord).where(OperationRecord.parent_id.in_(listids))
        )

        res2 = result2.scalars().all()
        lst = []
        for row in res2:
            # operation_record = orm_model_to_view_model(row, OperationRecordModel,exclude=["sort_number",'description'])
            lst.append(row)

        return lst

    async def get_operation_record_all(self, filterdict):
        return await self.operation_record_dao.get_operation_record_all(filterdict)
