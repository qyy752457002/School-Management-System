from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date


class AnnualReview(BaseDBModel):
    """
    annual_review：annual_review_id
    教师ID：teacher_id
    考核年度：assessment_year
    考核结果：assessment_result
    考核单位名称：assessment_institution_name
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_annual_review'
    __table_args__ = {'comment': 'annual_review信息表'}

    annual_review_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="annual_reviewID")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")
    assessment_year: Mapped[str] = mapped_column(String(64), nullable=False, comment="考核年度")
    assessment_result: Mapped[str] = mapped_column(String(64), nullable=False, comment="考核结果枚举assessment_result_lv1")
    assessment_institution_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="考核单位名称")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="审批状态",
                                                 default="submitting")
