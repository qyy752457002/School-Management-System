from datetime import datetime
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from mini_framework.databases.entities import BaseDBModel

class CertificateBatch(BaseDBModel):
    """
    制证批次表
    """
    __tablename__ = 'lfun_certificate_batch'
    __table_args__ = {'comment': '制证批次表'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID", autoincrement=False)
    batch_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="批次名称")
    status: Mapped[bool] = mapped_column(nullable=False, default=False, comment="状态")
    year: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="毕业年份")
    certification: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="制证模板")
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
    
