from sqlalchemy import String, Date,DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime

class TeacherChangeLog(BaseDBModel):
    """
    teacher_change：teacher_change_id
    变更ID：change_id
    教师ID：teacher_id
    操作人ID：operator_id
    操作人姓名：operator_name
    变更模块：change_module
    变更时间：change_time
    变更字段：changed_field
    变更前：before_change
    变更后：after_change
    操作时间：operation_time
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_change_log'
    __table_args__ = {'comment': 'teacher_change_log信息表'}

    teacher_change_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_changeID")
    teacher_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="教师ID")
    change_module: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更模块")
    change_detail: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更详情")
    log_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="审核状态")
    apply_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="申请人姓名")
    approval_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="审核人姓名")
    apply_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="申请时间")
    approval_time: Mapped[datetime] = mapped_column(DateTime, nullable=True, comment="审核时间")


    changed_field: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更字段")
    before_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更前")
    after_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更后")

    
