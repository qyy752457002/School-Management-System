from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teachers import Teacher
from views.models.teacher_transaction import TeacherTransactionQuery


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
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id == teachers_id, Teacher.is_deleted == 0))
        return result.scalar_one_or_none()

    # 删除单个教师信息

    # 删除单个教师信息
    async def delete_teachers(self, teachers: Teacher):
        session = await self.master_db()
        print(teachers.teacher_id, teachers.is_deleted)
        return await self.delete(session, teachers)

    # 获取所有教师信息
    async def get_all_teachers(self):
        session = await self.slave_db()
        result = await session.execute(select(Teacher))
        return result.scalars().all()

    # 获取教师数量
    async def get_teachers_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Teacher))
        return result.scalar()

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_name == teacher_transaction.teacher_name,
                                      Teacher.teacher_id_type == teacher_transaction.teacher_id_type,
                                      Teacher.teacher_id_number == teacher_transaction.teacher_id_number,
                                      )
        result = await session.execute(query)
        return result.scalar_one_or_none()
