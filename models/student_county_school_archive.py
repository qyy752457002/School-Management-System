from datetime import datetime

from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped


class CountyGraduationStudent(BaseDBModel):
    """
    归档状态
    归档时间
    """
    __tablename__ = 'lfun_county_graduation_student'
    __table_args__ = {'comment': '判断学校是否已经归档表'}

    school: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学校")
    school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="学校id", default=0)
    borough: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="行政属地")
    graduate_count: Mapped[int] = mapped_column(nullable=True, comment="毕业人数")
    county_archive_status: Mapped[bool] = mapped_column(nullable=True, comment="是否已归档", default=False)
    year: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="年份")
    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)