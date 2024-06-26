from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teacher_entry_approval import TeacherEntryApproval
from models.teachers import Teacher
from views.models.teacher_transaction import TeacherTransactionQuery
from views.models.teachers import TeacherApprovalQuery
from models.school import School


class TeacherEntryApprovalDao(DAOBase):
    # 新增教师关键信息
    async def add_teacher_entry_approval(self, teacher_entry_approval):
        session = await self.master_db()
        session.add(teacher_entry_approval)
        await session.commit()
        await session.refresh(teacher_entry_approval)
        return teacher_entry_approval

    async def update_teachers(self, teacher_entry_approval: TeacherEntryApproval, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_entry_approval, *args)
        query = update(TeacherEntryApproval).where(
            TeacherEntryApproval.teacher_id == teacher_entry_approval.teacher_id).values(**update_contents)
        return await self.update(session, query, teacher_entry_approval, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teacher_entry_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherEntryApproval).join(Teacher, Teacher.teacher_id == TeacherEntryApproval.teacher_id).where(
                TeacherEntryApproval.teacher_id == teacher_id))
        return result.scalar_one_or_none()

    async def get_teacher_entry_status_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherEntryApproval).join(Teacher, Teacher.teacher_id == TeacherEntryApproval.teacher_id).where(
                TeacherEntryApproval.teacher_id == teacher_id))
        if result.scalar_one_or_none():
            return result.scalar_one_or_none().approval_status
