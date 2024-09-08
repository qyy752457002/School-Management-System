from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Organization(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_organization'
    __table_args__ = {'comment': '组织架构模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="ID",autoincrement=False)
    org_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="组织分类 行政类等")

    org_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="组织或者部门名称 例如行政部")
    org_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="组织或者部门编号 学校内唯一")
    parent_id: Mapped[int] = mapped_column(BigInteger, comment="父级ID",default=0,nullable=True)
    school_id: Mapped[int] = mapped_column(BigInteger, comment="学校ID",default=0,nullable=True)
    member_cnt: Mapped[int] = mapped_column( comment="人数",default=0,nullable=True)

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
