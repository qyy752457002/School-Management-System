from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime


class TeacherApprovalLog(BaseDBModel):
    """
    teacher_approval_log：teacher_approval_log_id
    """
    __tablename__ = 'lfun_teacher_approval_log'
    __table_args__ = {'comment': '老师审批相关log表'}

    teacher_approval_log_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_changeID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    operator_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人ID")
    process_instance_id: Mapped[int] = mapped_column(nullable=True, comment="流程ID")
    change_module: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更模块")
    action: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作")
    operation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="操作时间")
