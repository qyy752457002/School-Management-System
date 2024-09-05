from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Tenant(BaseDBModel):
    """
    租户表

    """
    __tablename__ = 'lfun_tenant'
    __table_args__ = {'comment': '租户表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="年级ID",autoincrement=False)
    tenant_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    code: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    description: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    status: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    client_id: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="")
    client_secret: Mapped[str] = mapped_column(String(128), nullable=True,default='', comment="")
    cert_public_key: Mapped[str] = mapped_column(String(4096), nullable=True,default='', comment="")
    home_url: Mapped[str] = mapped_column(String(128), nullable=True,default='', comment="")
    redirect_url: Mapped[str] = mapped_column(String(512), nullable=True,default='', comment="")

    origin_id: Mapped[int] = mapped_column(BigInteger, comment="",default=0,nullable=True)

    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
