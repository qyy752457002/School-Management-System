from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class StandardGrade(BaseDBModel):
    """
    标准年级表
    """

    __tablename__ = "lfun_standard_grade"
    __table_args__ = {"comment": "标准年级表模型"}

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, comment="年级ID", autoincrement=False
    )
    grade_name: Mapped[str] = mapped_column(
        String(64), nullable=False, comment="年级名称/班级名称"
    )
    grade_index: Mapped[int] = mapped_column(
        nullable=True, comment="年级序号,用来判断怎么选择"
    )

    created_at = mapped_column(
        DateTime, default=datetime.now, nullable=True, comment="创建时间"
    )
