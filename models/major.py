from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Major(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_major'
    __table_args__ = {'comment': '专业表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    school_id: Mapped[int] = mapped_column( BigInteger,comment="学校ID",nullable=True,default=0)
    city: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城市")

    district: Mapped[str] = mapped_column(String(64), nullable=True, comment="",default='')

    major_name: Mapped[str] = mapped_column(String(24), nullable=False, comment="专业名称")
    major_id: Mapped[str] = mapped_column(String(60), nullable=True,default='', comment="专业code,枚举major")
    major_type: Mapped[str|None] = mapped_column(String(24), nullable=True,default='', comment="专业类型")
    major_id_lv2: Mapped[str|None] = mapped_column(String(24), nullable=True,default='', comment="2级专业code,枚举major_lv2")
    major_id_lv3: Mapped[str|None] = mapped_column(String(24), nullable=True,default='', comment="3级专业code,枚举major_lv3")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
