from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.operation_record import OperationRecord


class OperationRecordDAO(DAOBase):

    async def add_operation_record(self, operation_record: OperationRecord):
        session = await self.master_db()
        session.add(operation_record)
        await session.commit()
        await session.refresh(operation_record)
        return operation_record

    async def get_operation_record_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(OperationRecord))
        return result.scalar()

    async def delete_operation_record(self, operation_record: OperationRecord):
        session = await self.master_db()
        await session.delete(operation_record)
        await session.commit()

    async def get_operation_record_by_id(self, id):
        session = await self.slave_db()
        result = await session.execute(select(OperationRecord).where(OperationRecord.id == id))
        return result.scalar_one_or_none()

    async def query_operation_record_with_page(self, page_request: PageRequest, **kwargs):
        query = select(OperationRecord)
        query = query.order_by(OperationRecord.id.asc())

        for key, value in kwargs.items():
            if key == 'student_gender':

                # query = query.where(getattr(Student, key) == value)
                pass
            # elif key == 'school_id':
            # 	cond1 = StudentTransaction.in_school_id == value
            # 	cond2 = StudentTransaction.out_school_id == value
            # 	mcond = or_(cond1, cond2)
            #
            # 	query = query.filter( and_(
            # 		StudentTransaction.is_deleted == False,  # a=1
            # 		or_(
            # 			mcond
            # 		)
            # 	))
            # query = query.where(getattr(Student, key).like(f'%{value}%'))
            else:
                query = query.where(getattr(OperationRecord, key) == value)
        paging = await self.query_page(query, page_request)
        return paging



    async def update_operation_record(self, operation_record, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(operation_record, *args)
        query = update(OperationRecord).where(OperationRecord.id == operation_record.id).values(**update_contents)
        return await self.update(session, query, operation_record, update_contents, is_commit=is_commit)
