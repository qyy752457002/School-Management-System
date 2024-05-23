from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherLearnExperience(BaseDBModel):
    """
    teacher_learn_experience：teacher_learn_experience_id
    教师ID：teacher_id
    获的学历：education_obtained
    获得学历国家/地区：country_or_region_of_education
    获得学历的院校机构：institution_of_education_obtained
    所学妆业：major_learned
    是否师范类专业：is_major_normal
    入学时间：admission_date
    毕业时间：graduation_date
    学位层次：degree_level
    学位名称：degree_name
    获取学位过家地区：country_or_region_of_degree_obtained
    获得学位院校机构：institution_of_degree_obtained
    学位授予时间：degree_award_date
    学习方式：study_mode
    在学单位类别：type_of_institution
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_learn_experience'
    __table_args__ = {'comment': 'teacher_learn_experience信息表'}

    teacher_learn_experience_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_learn_experienceID")
    teacher_id: Mapped[int] = mapped_column(nullable=True, comment="教师ID")
    education_obtained: Mapped[str] = mapped_column(String(64), nullable=True, comment="获的学历")
    country_or_region_of_education: Mapped[str] = mapped_column(String(64), nullable=True, comment="获得学历国家/地区")
    institution_of_education_obtained: Mapped[str] = mapped_column(String(64), nullable=True, comment="获得学历的院校机构")
    major_learned: Mapped[str] = mapped_column(String(64), nullable=True, comment="所学妆业")
    is_major_normal: Mapped[bool] = mapped_column(String(64),default=False, nullable=True, comment="是否师范类专业")
    admission_date: Mapped[date] = mapped_column(Date, nullable=True, comment="入学时间")
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True, comment="毕业时间")
    degree_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="学位层次")
    degree_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="学位名称")
    country_or_region_of_degree_obtained: Mapped[str] = mapped_column(String(64), nullable=True, comment="获取学位过家地区")
    institution_of_degree_obtained: Mapped[str] = mapped_column(String(64), nullable=True, comment="获得学位院校机构")
    degree_award_date: Mapped[date] = mapped_column(Date, nullable=True, comment="学位授予时间")
    study_mode: Mapped[str] = mapped_column(String(64), nullable=True, comment="学习方式")
    type_of_institution: Mapped[str] = mapped_column(String(64), nullable=True, comment="在学单位类别")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
