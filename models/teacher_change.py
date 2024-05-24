from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherChange(BaseDBModel):
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
    __tablename__ = 'lfun_teacher_change'
    __table_args__ = {'comment': 'teacher_change信息表'}

    teacher_change_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_changeID")
    change_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更ID")
    teacher_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="教师ID")
    operator_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人ID")
    operator_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人姓名")
    change_module: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更模块")
    change_time: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更时间")
    changed_field: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更字段")
    before_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更前")
    after_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更后")
    operation_time: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
