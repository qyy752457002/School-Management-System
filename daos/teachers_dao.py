from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
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

    # 编辑教师关键信息

    async def update_teachers(self, teachers):
        session = await self.master_db()
        update_stmt = update(Teacher).where(Teacher.id == teachers.id).values(
            teacher_name=teachers.teacher_name,
            teacher_gender=teachers.teacher,
            teacher_id_type=teachers.teacher_id_type,
            teacher_id_number=teachers.teacher_id_number,
            teacher_date_of_birth=teachers.teacher_date_of_birth,
            teacher_employer=teachers.teacher_employer,
            teacher_avatar=teachers.teacher_avatar,
        )
        await session.execute(update_stmt)
        await session.commit()
        return teachers

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(select(Teacher).where(Teacher.id == teachers_id))
        return result.scalar_one_or_none()

    #联合Teacher和TeacherInfo表查询教师信息


