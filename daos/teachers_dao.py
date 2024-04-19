from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase,get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teachers import Teacher
from models.teachers_info import TeacherInfo


class TeachersDao(DAOBase):
    # 新增教师关键信息
    async def add_teachers(self, teachers):
        session = await self.master_db()
        session.add(teachers)
        await session.commit()
        await session.refresh(teachers)
        return teachers


    async def update_teachers(self, teachers: Teacher, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers, *args)
        query = update(Teacher).where(Teacher.teacher_id == teachers.teacher_id).values(**update_contents)
        return await self.update(session, query, teachers, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(select(Teacher).where(Teacher.teacher_id == teachers_id))
        return result.scalar_one_or_none()

    # async def get_teachers_by_username(self, username):
    #     session = await self.slave_db()
    #     result = await session.execute(select(Teacher).where(Teacher.username) == username)
    #     return result.scalar_one_or_none()

    #删除单个教师信息
    async def delete_teachers(self, teachers: Teacher):
        session = await self.master_db()
        return await self.delete(session, teachers)

    #获取所有教师信息
    async def get_all_teachers(self):
        session = await self.slave_db()
        result = await session.execute(select(Teacher))
        return result.scalars().all()

    #获取教师数量
    async def get_teachers_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Teacher))
        return result.scalar()

    # async def query_teacher_with_page(self,username, page_request: PageRequest):
    #     query = select(Teacher)
    #     if username:
    #         query = query.where(Teacher.username == username)
    #     paging = await self.query_page(query, page_request)
    #     return paging





