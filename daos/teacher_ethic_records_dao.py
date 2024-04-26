from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_ethic_records import TeacherEthicRecords
from models.teachers import Teacher


class TeacherEthicRecordsDAO(DAOBase):

    async def add_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecords):
        session = await self.master_db()
        session.add(teacher_ethic_records)
        await session.commit()
        await session.refresh(teacher_ethic_records)
        return teacher_ethic_records

    async def get_teacher_ethic_records_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherEthicRecords))
        return result.scalar()

    async def delete_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecords):
        session = await self.master_db()
        return await self.delete(session, teacher_ethic_records)

    async def get_teacher_ethic_records_by_teacher_ethic_records_id(self, teacher_ethic_records_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherEthicRecords).where(TeacherEthicRecords.teacher_ethic_records_id == teacher_ethic_records_id))
        return result.scalar_one_or_none()

    async def query_teacher_ethic_records_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherEthicRecords)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_ethic_records(self, teacher_ethic_records, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_ethic_records, *args)
        query = update(TeacherEthicRecords).where(
            TeacherEthicRecords.teacher_ethic_records_id == teacher_ethic_records.teacher_ethic_records_id).values(
            **update_contents)
        return await self.update(session, query, teacher_ethic_records, update_contents, is_commit=is_commit)

    async def get_all_teacher_ethic_records(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherEthicRecords).join(Teacher,
                                                 TeacherEthicRecords.teacher_id == Teacher.teacher_id).where(
            TeacherEthicRecords.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
