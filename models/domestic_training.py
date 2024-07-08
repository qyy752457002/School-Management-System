from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class DomesticTraining(BaseDBModel):
    """
    domestic_training：domestic_training_id
    教师ID：teacher_id
    培训年度：training_year
    培训类型：training_type
    培训项目：training_project
    培训机构：training_institution
    培训方式：training_mode
    培训学时：training_hours
    培训学分：training_credits
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_domestic_training'
    __table_args__ = {'comment': 'domestic_training信息表'}

    domestic_training_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="domestic_trainingID")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")
    training_year: Mapped[str] = mapped_column(String(64), nullable=False, comment="培训年度")
    training_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="培训类型")
    training_project: Mapped[str] = mapped_column(String(64), nullable=False, comment="培训项目")
    training_institution: Mapped[str] = mapped_column(String(64), nullable=True, comment="培训机构")
    training_mode: Mapped[str] = mapped_column(String(64), nullable=False, comment="培训方式")
    training_hours: Mapped[str] = mapped_column(String(64), nullable=False, comment="培训学时")
    training_credits: Mapped[str] = mapped_column(String(64), nullable=True, comment="培训学分")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
