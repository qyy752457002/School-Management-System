from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class EducationYear(BaseDBModel):
    """
    学制表
    """
    __tablename__ = 'lfun_education_year'
    __table_args__ = {'comment': '学制表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="年级ID",autoincrement=True)
    school_type: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学校类型（小学/初中）")

    education_year: Mapped[int] = mapped_column( comment="学制年限（如：6年/3年）",)
    city: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城市")
    district: Mapped[str] = mapped_column(String(64), nullable=True, comment="",default='')

    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
