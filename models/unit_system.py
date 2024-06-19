from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime


class UnitSystem(BaseDBModel):
    """
    # 各单位部署系统的 模型

    """
    __tablename__ = 'lfun_unit_system'
    __table_args__ = {'comment': '单位部署系统的 模型 '}

    school_id: Mapped[int] = mapped_column(primary_key=True, comment="学校ID")
    institution_id: Mapped[int] = mapped_column(primary_key=True, comment="行政单位ID 例如区 市教育局")
    unit_url: Mapped[str] = mapped_column(comment="api地址")
    remark: Mapped[str] = mapped_column(comment="")
    created_at: Mapped[datetime] = mapped_column(comment="创建时间")