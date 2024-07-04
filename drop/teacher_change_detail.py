from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime


class TeacherChangeDetail(BaseDBModel):
    __tablename__ = 'lfun_teacher_change_datail'
    __table_args__ = {'comment': 'teacher_change_detail详情信息表'}

    teacher_change_detail_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_changeID")
    teacher_change_id: Mapped[int] = mapped_column(nullable=False, comment="teacher_changeID")
    teacher_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="教师ID")
    change_module: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更模块")
    changed_field: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更字段")
    before_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更前")
    after_change: Mapped[str] = mapped_column(String(64), nullable=False, comment="变更后")
