from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_borrow import TeacherBorrow
from models.teachers import Teacher


class TeacherBorrowDAO(DAOBase):

    async def add_teacher_borrow(self, teacher_borrow: TeacherBorrow):
        session = await self.master_db()
        session.add(teacher_borrow)
        await session.commit()
        await session.refresh(teacher_borrow)
        return teacher_borrow

    async def get_teacher_borrow_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherBorrow))
        return result.scalar()

    async def delete_teacher_borrow(self, teacher_borrow: TeacherBorrow):
        session = await self.master_db()
        await session.delete(teacher_borrow)
        await session.commit()

    async def get_teacher_borrow_by_teacher_borrow_id(self, teacher_borrow_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherBorrow).where(TeacherBorrow.teacher_borrow_id == teacher_borrow_id))
        return result.scalar_one_or_none()

    async def query_teacher_borrow_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherBorrow)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_borrow(self, teacher_borrow, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_borrow, *args)
        query = update(TeacherBorrow).where(TeacherBorrow.teacher_borrow_id == teacher_borrow.teacher_borrow_id).values(
            **update_contents)
        return await self.update(session, query, teacher_borrow, update_contents, is_commit=is_commit)

    async def get_all_teacher_borrow(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherBorrow).join(Teacher, Teacher.teacher_id == TeacherBorrow.teacher_id).where(
            TeacherBorrow.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
