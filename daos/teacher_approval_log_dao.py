from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teacher_approval_log import TeacherApprovalLog
from models.teachers import Teacher



class TeacherApprovalLogDao(DAOBase):
    # 新增教师关键信息
    async def add_teacher_approval_log(self, teacher_approval_log):
        session = await self.master_db()
        session.add(teacher_approval_log)
        await session.commit()
        await session.refresh(teacher_approval_log)
        return teacher_approval_log

    async def update_teachers(self, teacher_approval_log: TeacherApprovalLog, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_approval_log, *args)
        query = update(TeacherApprovalLog).where(
            TeacherApprovalLog.teacher_id == teacher_approval_log.teacher_id).values(**update_contents)
        return await self.update(session, query, teacher_approval_log, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teacher_approval_log_by_process_instance_id(self, process_instance_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherApprovalLog).where(
                TeacherApprovalLog.process_instance_id == process_instance_id))
        return result.scalar_one_or_none()
