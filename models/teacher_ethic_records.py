from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherEthicRecords(BaseDBModel):
    """
    teacher_ethic_records：teacher_ethic_records_id
    教师ID：teacher_id
    师德考核时间：ethics_assessment_date
    师德考核结论：ethics_assessment_conclusion
    考核单位名称：assessment_institution_name
    荣誉级别：honor_level
    荣誉称号：honor_title
    荣誉日期：honor_date
    荣誉授予单位名称：awarding_institution_name
    荣誉记录描述：honor_record_description
    处分类别：disciplinary_category
    处分原因：disciplinary_reason
    处分日期：disciplinary_date
    处分单位名称：disciplinary_institution_name
    处分记录描述：disciplinary_record_description
    处分发生日期：disciplinary_occurrence_date
    处分撤销日期：disciplinary_revocation_date
    处分撤销原因：disciplinary_revocation_reason
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_ethic_records'
    __table_args__ = {'comment': 'teacher_ethic_records信息表'}

    teacher_ethic_records_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_ethic_recordsID")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    ethics_assessment_date: Mapped[date] = mapped_column(Date, nullable=False, comment="师德考核时间")
    ethics_assessment_conclusion: Mapped[str] = mapped_column(String(64), nullable=False, comment="师德考核结论")
    assessment_institution_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="考核单位名称")
    honor_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="荣誉级别")
    honor_title: Mapped[str] = mapped_column(String(64), nullable=False, comment="荣誉称号")
    honor_date: Mapped[date] = mapped_column(Date, nullable=False, comment="荣誉日期")
    awarding_institution_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="荣誉授予单位名称")
    honor_record_description: Mapped[str] = mapped_column(String(64), nullable=False, comment="荣誉记录描述")
    disciplinary_category: Mapped[str] = mapped_column(String(64), nullable=False, comment="处分类别")
    disciplinary_reason: Mapped[str] = mapped_column(String(64), nullable=False, comment="处分原因")
    disciplinary_date: Mapped[date] = mapped_column(Date, nullable=False, comment="处分日期")
    disciplinary_institution_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="处分单位名称")
    disciplinary_record_description: Mapped[str] = mapped_column(String(64), nullable=False, comment="处分记录描述")
    disciplinary_occurrence_date: Mapped[date] = mapped_column(Date, nullable=False, comment="处分发生日期")
    disciplinary_revocation_date: Mapped[date] = mapped_column(Date, nullable=False, comment="处分撤销日期")
    disciplinary_revocation_reason: Mapped[str] = mapped_column(String(64), nullable=False, comment="处分撤销原因")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
