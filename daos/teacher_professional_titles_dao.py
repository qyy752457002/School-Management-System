from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_professional_titles import TeacherProfessionalTitles
from models.teachers import Teacher


class TeacherProfessionalTitlesDAO(DAOBase):

    async def add_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitles):
        session = await self.master_db()
        session.add(teacher_professional_titles)
        await session.commit()
        await session.refresh(teacher_professional_titles)
        return teacher_professional_titles

    async def get_teacher_professional_titles_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherProfessionalTitles))
        return result.scalar()

    async def delete_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitles):
        session = await self.master_db()
        await session.delete(teacher_professional_titles)
        await session.commit()

    async def get_teacher_professional_titles_by_teacher_professional_titles_id(self, teacher_professional_titles_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherProfessionalTitles).where(
            TeacherProfessionalTitles.teacher_professional_titles_id == teacher_professional_titles_id))
        return result.scalar_one_or_none()

    async def query_teacher_professional_titles_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherProfessionalTitles)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_professional_titles(self, teacher_professional_titles, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_professional_titles, *args)
        query = update(TeacherProfessionalTitles).where(
            TeacherProfessionalTitles.teacher_professional_titles_id == teacher_professional_titles.teacher_professional_titles_id).values(
            **update_contents)
        return await self.update(session, query, teacher_professional_titles, update_contents, is_commit=is_commit)

    async def get_all_teacher_professional_titles(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherProfessionalTitles).join(Teacher,
                                                       TeacherProfessionalTitles.teacher_id == Teacher.teacher_id).where(
            TeacherProfessionalTitles.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
