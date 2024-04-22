from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherProfessionalTitles(BaseDBModel):
    """
    teacher_professional_titles：teacher_professional_titles_id
    教师ID：teacher_id
    现专业技术职务：current_professional_title
    聘任单位名称：employing_institution_name
    聘任开始时间：employment_start_date
    聘任结束时间：employment_end_date
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_professional_titles'
    __table_args__ = {'comment': 'teacher_professional_titles信息表'}

    teacher_professional_titles_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_professional_titlesID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    current_professional_title: Mapped[str] = mapped_column(String(64), nullable=False, comment="现专业技术职务")
    employing_institution_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="聘任单位名称")
    employment_start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="聘任开始时间")
    employment_end_date: Mapped[date] = mapped_column(Date, nullable=True, comment="聘任结束时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
