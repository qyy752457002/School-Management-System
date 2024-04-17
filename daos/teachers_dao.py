from sqlalchemy import select, func

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teachers import Teacher


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
        session.add(teachers)
        await session.commit()
        return teachers

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(select(Teacher).where(Teacher.id == teachers_id))
        return result.scalar_one_or_none()


