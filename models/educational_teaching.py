from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class EducationalTeaching(BaseDBModel):
    """
    educational_teaching：educational_teaching_id
    教师ID：teacher_id
    学年：academic_year
    学期：semester
    任教阶段：teaching_stage
    任课课程类别：course_category
    任课学科类别：subject_category
    任课课程：course_name
    平均每周教学课时：average_weekly_teaching_hours
    承担其他工作：other_responsibilities
    平均每周其他工作折合课时：average_weekly_other_duties_hours
    兼任工作：concurrent_job
    兼任工作名称：concurrent_job_name
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_educational_teaching'
    __table_args__ = {'comment': 'educational_teaching信息表'}

    educational_teaching_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="educational_teachingID")
    teacher_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="教师ID")
    academic_year: Mapped[str] = mapped_column(String(64), nullable=False, comment="学年")
    semester: Mapped[str] = mapped_column(String(64), nullable=False, comment="学期")
    teaching_stage: Mapped[str] = mapped_column(String(64), nullable=False, comment="任教阶段")
    course_category: Mapped[str] = mapped_column(String(64), nullable=False, comment="任课课程类别")
    subject_category: Mapped[str] = mapped_column(String(64), nullable=False, comment="任课学科类别")
    course_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="任课课程")
    average_weekly_teaching_hours: Mapped[str] = mapped_column(String(64), nullable=False, comment="平均每周教学课时")
    other_responsibilities: Mapped[str] = mapped_column(String(64), nullable=False, comment="承担其他工作")
    average_weekly_other_duties_hours: Mapped[str] = mapped_column(String(64), nullable=False, comment="平均每周其他工作折合课时")
    concurrent_job: Mapped[str] = mapped_column(String(64), nullable=False, comment="兼任工作")
    concurrent_job_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="兼任工作名称")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
