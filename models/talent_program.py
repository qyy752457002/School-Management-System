from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TalentProgram(BaseDBModel):
    """
    talent_program：talent_program_id
    教师ID：teacher_id
    人才项目名称：talent_project_name
    入选年份：selected_year
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_talent_program'
    __table_args__ = {'comment': 'talent_program信息表'}

    talent_program_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="talent_programID")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")
    talent_project_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="人才项目名称")
    selected_year: Mapped[str] = mapped_column(String(64), nullable=True, comment="入选年份")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="审批状态",
                                                 default="submitting")
    
