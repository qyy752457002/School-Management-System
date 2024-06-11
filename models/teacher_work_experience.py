from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherWorkExperience(BaseDBModel):
    """
    teacher_work_experience：teacher_work_experience_id
    教师ID：teacher_id
    任职单位名称：employment_institution_name
    开始时间：start_date
    结束时间：end_date
    在职岗位：on_duty_position

    单位性质类别：institution_nature_category
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_work_experience'
    __table_args__ = {'comment': 'teacher_work_experience信息表'}

    teacher_work_experience_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_work_experienceID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    employment_institution_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="任职单位名称")
    start_date: Mapped[date] = mapped_column(Date, nullable=True, comment="开始时间")
    end_date: Mapped[date] = mapped_column(Date, nullable=True, comment="结束时间")
    on_duty_position: Mapped[str] = mapped_column(String(64), nullable=True, comment="在职岗位")
    institution_nature_category: Mapped[str] = mapped_column(String(64), nullable=True, comment="单位性质类别")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
