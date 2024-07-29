from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_qualifications import TeacherQualifications
from models.teachers import Teacher


class TeacherQualificationsDAO(DAOBase):

    async def add_teacher_qualifications(self, teacher_qualifications: TeacherQualifications):
        session = await self.master_db()
        session.add(teacher_qualifications)
        await session.commit()
        await session.refresh(teacher_qualifications)
        return teacher_qualifications

    async def get_teacher_qualifications_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherQualifications))
        return result.scalar()

    async def delete_teacher_qualifications(self, teacher_qualifications: TeacherQualifications):
        session = await self.master_db()
        return await self.delete(session, teacher_qualifications)

    async def get_teacher_qualifications_by_teacher_qualifications_id(self, teacher_qualifications_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherQualifications).where(
            TeacherQualifications.teacher_qualifications_id == teacher_qualifications_id,
            TeacherQualifications.is_deleted == False))
        return result.scalar_one_or_none()

    async def query_teacher_qualifications_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherQualifications)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_qualifications(self, teacher_qualifications, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_qualifications, *args)
        query = update(TeacherQualifications).where(
            TeacherQualifications.teacher_qualifications_id == teacher_qualifications.teacher_qualifications_id).values(
            **update_contents)
        return await self.update(session, query, teacher_qualifications, update_contents, is_commit=is_commit)

    async def get_all_teacher_qualifications(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherQualifications).join(Teacher,
                                                   TeacherQualifications.teacher_id == Teacher.teacher_id).where(
            TeacherQualifications.teacher_id == teacher_id, TeacherQualifications.is_deleted == False)
        result = await session.execute(query)
        return result.scalars().all()
