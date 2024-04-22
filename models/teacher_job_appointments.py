from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherJobAppointments(BaseDBModel):
    """
    teacher_job_appointments：teacher_job_appointments_id
    教师ID：teacher_id
    岗位类别：position_category
    岗位等级：position_level
    校级职务：school_level_position
    是否兼任其他岗位：is_concurrent_other_positions
    兼任岗位类别：concurrent_position_category
    兼任岗位登记：concurrent_position_registration
    任职单位名称：employment_institution_name
    聘任开始时间：appointment_start_date
    结束时间：end_date
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_job_appointments'
    __table_args__ = {'comment': 'teacher_job_appointments信息表'}

    teacher_job_appointments_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_job_appointmentsID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    position_category: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位类别")
    position_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="岗位等级")
    school_level_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="校级职务")
    is_concurrent_other_positions: Mapped[bool] = mapped_column(default=False, comment="是否兼任其他岗位")
    concurrent_position_category: Mapped[str] = mapped_column(String(64), nullable=False, comment="兼任岗位类别")
    concurrent_position_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="兼任岗位登记")
    employment_institution_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="任职单位名称")
    appointment_start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="聘任开始时间")
    start_date: Mapped[date] = mapped_column(Date, nullable=True, comment="任职开始年月时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
