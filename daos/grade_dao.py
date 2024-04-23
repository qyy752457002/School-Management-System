from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.grade import Grade


class GradeDAO(DAOBase):

    async def get_grade_by_id(self, grade_id):
        session = await self.slave_db()
        result = await session.execute(select(Grade).where(Grade.id == grade_id))
        return result.scalar_one_or_none()

    async def get_grade_by_grade_name(self, grade_name):
        session = await self.slave_db()
        result = await session.execute(select(Grade).where(Grade.grade_name == grade_name))
        return result.first()

    async def add_grade(self, grade):
        session = await self.master_db()
        session.add(grade)
        await session.commit()
        await session.refresh(grade)
        return grade

    async def update_grade(self, grade):
        session = await self.master_db()
        session.add(grade)
        await session.commit()
        return grade

    async def softdelete_grade(self, grade):
        session = await self.master_db()
        deleted_status= True
        update_stmt = update(Grade).where(Grade.id == grade.id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return grade

    async def delete_grade(self, grade):
        session = await self.master_db()
        await session.delete(grade)
        await session.commit()
        return grade

    async def get_all_grades(self):
        session = await self.slave_db()
        result = await session.execute(select(Grade))
        return result.scalars().all()

    async def get_grade_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Grade))
        return result.scalar()

    async def query_grade_with_page(self, grade_name,school_id, page_request: PageRequest) -> Paging:
        query = select(Grade)
        if grade_name:
            query = query.where(Grade.grade_name.like(f'%{grade_name}%') )
        if school_id:
            query = query.where(Grade.school_id == school_id)
        paging = await self.query_page(query, page_request)
        return paging
