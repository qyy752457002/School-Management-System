from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherSkillCertificates(BaseDBModel):
    """
    teacher_skill_certificates：teacher_skill_certificates_id
    教师ID：teacher_id
    语种：language
    掌握程度：proficiency_level
    其他技能名称：other_skill_name
    其他技能程度：other_skill_level
    证书类型：certificate_type
    语言证书名称：language_certificate_name
    发证年月：issue_year_month
    发证单位：issuing_authority
    证书编号：certificate_number
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_skill_certificates'
    __table_args__ = {'comment': 'teacher_skill_certificates信息表'}

    teacher_skill_certificates_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="teacher_skill_certificatesID")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")
    language: Mapped[str] = mapped_column(String(64), nullable=True, comment="语种")
    proficiency_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="掌握程度")
    other_skill_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="其他技能名称")
    other_skill_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="其他技能程度")
    certificate_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="证书类型")
    language_certificate_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="语言证书名称")
    issue_year_month: Mapped[date] = mapped_column(Date, nullable=True, comment="发证年月")
    issuing_authority: Mapped[str] = mapped_column(String(64), nullable=True, comment="发证单位")
    certificate_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证书编号")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
