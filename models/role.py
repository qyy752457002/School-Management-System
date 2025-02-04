from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Role(BaseDBModel):

    """
    角色

    """
    __tablename__ = 'lfun_role'
    __table_args__ = {'comment': '角色表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="角色ID",autoincrement=False)
    system_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="系统类型",default='')
    edu_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="教育类型",default='')
    unit_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="单位类型",default='')
    app_name: Mapped[str] = mapped_column(String(64),  nullable=True, comment="系统名称",default='')
    remark: Mapped[str] = mapped_column(String(64),  nullable=True, comment="备注",default='')
    unit_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="单位ID",default=0)
    school_id: Mapped[int] =mapped_column(BigInteger,nullable=True, comment="学校id",default=0)
    county_id: Mapped[int] =mapped_column(BigInteger,nullable=True, comment="区id",default=0)
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
