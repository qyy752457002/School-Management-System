from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teacher_key_info_approval import TeacherKeyInfoApproval
from models.teachers import Teacher
from views.models.teacher_transaction import TeacherTransactionQuery
from views.models.teachers import TeacherApprovalQuery
from models.school import School


class TeacherKeyInfoApprovalDao(DAOBase):
    # 新增教师关键信息
    async def add_teacher_key_info_approval(self, teacher_key_info_approval):
        session = await self.master_db()
        session.add(teacher_key_info_approval)
        await session.commit()
        await session.refresh(teacher_key_info_approval)
        return teacher_key_info_approval

    async def update_teachers(self, teacher_key_info_approval: TeacherKeyInfoApproval, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_key_info_approval, *args)
        query = update(TeacherKeyInfoApproval).where(
            TeacherKeyInfoApproval.teacher_id == teacher_key_info_approval.teacher_id).values(**update_contents)
        return await self.update(session, query, teacher_key_info_approval, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teacher_key_info_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherKeyInfoApproval).join(Teacher, Teacher.teacher_id == TeacherKeyInfoApproval.teacher_id).where(
                TeacherKeyInfoApproval.teacher_id == teacher_id))
        return result.scalar_one_or_none()

    async def get_teacher_key_info_status_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherKeyInfoApproval).join(Teacher, Teacher.teacher_id == TeacherKeyInfoApproval.teacher_id).where(
                TeacherKeyInfoApproval.teacher_id == teacher_id))
        if result.scalar_one_or_none():
            return result.scalar_one_or_none().approval_status
