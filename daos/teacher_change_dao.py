from sqlalchemy import select, func
from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.web.std_models.page import PageRequest

from drop.teacher_change_log import TeacherChangeLog
from models.teachers import Teacher
from drop.teacher_change_detail import TeacherChangeDetail


class TeacherChangeLogDAO(DAOBase):

    async def add_teacher_change(self, teacher_change: TeacherChangeLog):
        session = await self.master_db()
        session.add(teacher_change)
        await session.commit()
        await session.refresh(teacher_change)
        return teacher_change

    async def add_teacher_change_detail(self, teacher_change_detail: TeacherChangeDetail):
        session = await self.master_db()
        session.add(teacher_change_detail)
        await session.commit()
        await session.refresh(teacher_change_detail)
        return teacher_change_detail

    async def get_teacher_change_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherChangeLog))
        return result.scalar()

    async def delete_teacher_change(self, teacher_change: TeacherChangeLog):
        session = await self.master_db()
        await session.delete(teacher_change)
        await session.commit()

    async def get_teacher_change_detail_by_teacher_id(self, teacher_id, teacher_change_id):
        """
        通过教师id和变更id获取变更详情
        """
        session = await self.slave_db()
        result = await session.execute(select(TeacherChangeDetail).join(TeacherChangeLog,
                                                                        TeacherChangeDetail.teacher_change_id == TeacherChangeLog.teacher_change_id).join(
            Teacher, TeacherChangeDetail.teacher_id == Teacher.teacher_id).where(
            TeacherChangeDetail.teacher_id == teacher_id,
            TeacherChangeDetail.teacher_change_id == teacher_change_id))
        return result.scalars().all()

    async def query_teacher_change_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherChangeLog)
        paging = await self.query_page(query, page_request)
        return paging

    async def get_all_teacher_change(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherChangeLog).join(Teacher,
                                              TeacherChangeLog.teacher_id == Teacher.teacher_id).where(
            TeacherChangeLog.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
