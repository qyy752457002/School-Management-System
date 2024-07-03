from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class OverseasStudy(BaseDBModel):
    """
    overseas_study：overseas_study_id
    教师ID：teacher_id
    开始日期：start_date
    结束日期：end_date
    国家地区：country_region
    研修机构名称：training_institution_name
    项目名称：project_name
    项目组织单位名称：organizing_institution_name
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_overseas_study'
    __table_args__ = {'comment': 'overseas_study信息表'}

    overseas_study_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="overseas_studyID")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="开始日期")
    end_date: Mapped[date] = mapped_column(Date, nullable=False, comment="结束日期")
    country_region: Mapped[str] = mapped_column(String(64), nullable=False, comment="国家地区")
    training_institution_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="研修机构名称")
    project_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="项目名称")
    organizing_institution_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="项目组织单位名称")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
