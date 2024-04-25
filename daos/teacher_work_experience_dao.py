from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_work_experience import TeacherWorkExperience

from models.teachers import Teacher


class TeacherWorkExperienceDAO(DAOBase):

    async def add_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperience):
        session = await self.master_db()
        session.add(teacher_work_experience)
        await session.commit()
        await session.refresh(teacher_work_experience)
        return teacher_work_experience

    async def get_teacher_work_experience_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherWorkExperience))
        return result.scalar()

    async def delete_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperience):
        session = await self.master_db()
        await session.delete(teacher_work_experience)
        await session.commit()

    async def get_teacher_work_experience_by_teacher_work_experience_id(self, teacher_work_experience_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherWorkExperience).where(
            TeacherWorkExperience.teacher_work_experience_id == teacher_work_experience_id))
        return result.scalar_one_or_none()

    async def get_teacher_work_experience_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherWorkExperience).where(
            TeacherWorkExperience.teacher_id == teacher_id))
        return result.scalar_one_or_none()

    async def query_teacher_work_experience_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherWorkExperience)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_work_experience(self, teacher_work_experience, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_work_experience, *args)
        query = update(TeacherWorkExperience).where(
            TeacherWorkExperience.teacher_work_experience_id == teacher_work_experience.teacher_work_experience_id).values(
            **update_contents)
        return await self.update(session, query, teacher_work_experience, update_contents, is_commit=is_commit)

    async def get_all_teacher_work_experience(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherWorkExperience).join(Teacher,
                                                   TeacherWorkExperience.teacher_id == Teacher.teacher_id).where(
            TeacherWorkExperience.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
