from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.transfer_details import TransferDetails
from views.models.teacher_transaction import TeacherTransactionQuery
from models.teachers_info import TeacherInfo
from models.teachers import Teacher


class TransferDetailsDAO(DAOBase):

    async def add_transfer_details(self, transfer_details: TransferDetails):
        session = await self.master_db()
        session.add(transfer_details)
        await session.commit()
        await session.refresh(transfer_details)
        return transfer_details

    async def get_transfer_details_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TransferDetails))
        return result.scalar()

    async def delete_transfer_details(self, transfer_details: TransferDetails):
        session = await self.master_db()
        await session.delete(transfer_details)
        await session.commit()

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TransferDetails).where(TransferDetails.transfer_details_id == transfer_details_id))
        return result.scalar_one_or_none()

    async def query_transfer_details_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TransferDetails)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_transfer_details(self, transfer_details, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(transfer_details, *args)
        query = update(TransferDetails).where(
            TransferDetails.transfer_details_id == transfer_details.transfer_details_id).values(**update_contents)
        return await self.update(session, query, transfer_details, update_contents, is_commit=is_commit)

    async def query_teacher(self, query_model: TeacherTransactionQuery):
        session = await self.slave_db()
        query = select(Teacher.teacher_id, Teacher.teacher_name, Teacher.teacher_id_number, Teacher.teacher_id_type,
                       Teacher.teacher_gender, TeacherInfo.teacher_number, TeacherInfo.birth_place).join(TeacherInfo,
                                                                                                         Teacher.teacher_id == TeacherInfo.teacher_id)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_id_type:
            query = query.where(Teacher.teacher_id_type == query_model.teacher_id_type)
        result = await session.execute(query)
        return result.scalars().all()
