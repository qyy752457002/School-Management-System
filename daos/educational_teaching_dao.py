from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.educational_teaching import EducationalTeaching
from models.teachers import Teacher


class EducationalTeachingDAO(DAOBase):

    async def add_educational_teaching(self, educational_teaching: EducationalTeaching):
        session = await self.master_db()
        session.add(educational_teaching)
        await session.commit()
        await session.refresh(educational_teaching)
        return educational_teaching

    async def get_educational_teaching_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(EducationalTeaching))
        return result.scalar()

    async def delete_educational_teaching(self, educational_teaching: EducationalTeaching):
        session = await self.master_db()
        return await self.delete(session, educational_teaching)

    async def get_educational_teaching_by_educational_teaching_id(self, educational_teaching_id):
        session = await self.slave_db()
        result = await session.execute(
            select(EducationalTeaching).where(EducationalTeaching.educational_teaching_id == educational_teaching_id))
        return result.scalar_one_or_none()

    async def query_educational_teaching_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(EducationalTeaching)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_educational_teaching(self, educational_teaching, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(educational_teaching, *args)
        query = update(EducationalTeaching).where(
            EducationalTeaching.educational_teaching_id == educational_teaching.educational_teaching_id).values(
            **update_contents)
        return await self.update(session, query, educational_teaching, update_contents, is_commit=is_commit)

    async def get_all_educational_teaching(self, teacher_id):
        session = await self.slave_db()
        query = select(EducationalTeaching).join(Teacher, EducationalTeaching.teacher_id == Teacher.teacher_id).where(
            EducationalTeaching.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
