from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherQualifications(BaseDBModel):
    """
    teacher_qualifications：teacher_qualifications_id
    教师ID：teacher_id
    教师资格证种类：teacher_qualification_type
    资格证号码：qualification_number
    任教学科：teaching_subject
    证书颁发时间：certificate_issue_date
    颁发机构：issuing_authority
    首次注册日期：first_registration_date
    定期注册日期：regular_registration_date
    定期注册结论：regular_registration_conclusion
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_qualifications'
    __table_args__ = {'comment': 'teacher_qualifications信息表'}

    teacher_qualifications_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="teacher_qualificationsID")
    teacher_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="教师ID")
    teacher_qualification_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="教师资格证种类")
    qualification_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="资格证号码")
    teaching_subject: Mapped[str] = mapped_column(String(64), nullable=False, comment="任教学科")
    certificate_issue_date: Mapped[date] = mapped_column(Date, nullable=False, comment="证书颁发时间")
    issuing_authority: Mapped[str] = mapped_column(String(64), nullable=True, comment="颁发机构")
    first_registration_date: Mapped[date] = mapped_column(Date, nullable=True, comment="首次注册日期")
    regular_registration_date: Mapped[date] = mapped_column(Date, nullable=True, comment="定期注册日期")
    regular_registration_conclusion: Mapped[str] = mapped_column(String(64), nullable=True, comment="定期注册结论")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
