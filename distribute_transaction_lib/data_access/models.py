from datetime import datetime

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from mini_framework.databases.entities import BaseDBModel
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

class TransactionInfo(BaseDBModel):
    """
    事务表模型
    """
    __tablename__ = 'lfun_transactions'
    __table_args__ = {'comment': '事务表模型'}

    transaction_id: Mapped[int] = mapped_column(primary_key=True, comment="事务ID")
    transaction_type: Mapped[str] = mapped_column(comment="事务类型")
    payload: Mapped[dict] = mapped_column(JSON, comment="事务负载")
    operator: Mapped[str] = mapped_column(comment="操作人")
    created_at: Mapped[datetime] = mapped_column(comment="创建时间")


class TransactionProgress(BaseDBModel):
    """
    事务进度表模型
    """
    __tablename__ = 'lfun_transaction_progress'
    __table_args__ = {'comment': '事务进度表模型'}

    transaction_id: Mapped[int] = mapped_column(primary_key=True, comment="事务ID")
    progress: Mapped[float] = mapped_column(comment="事务进度")
    process_desc: Mapped[str] = mapped_column(comment="事务进度描述")
    last_updated: Mapped[datetime] = mapped_column(comment="最后更新时间")


class TransactionResults(BaseDBModel):
    """
    事务结果表模型
    """
    __tablename__ = 'lfun_transaction_results'
    __table_args__ = {'comment': '事务结果表模型'}

    transaction_id: Mapped[int] = mapped_column(primary_key=True, comment="事务ID")
    result_extra: Mapped[dict] = mapped_column(JSON, comment="事务额外结果")
    state: Mapped[str] = mapped_column(comment="事务状态")
    last_updated: Mapped[datetime] = mapped_column(comment="完成时间")

#
# class UnitSystem(BaseDBModel):
#     """
#     # 各单位部署系统的 模型
#
#     """
#     __tablename__ = 'lfun_unit_system'
#     __table_args__ = {'comment': '单位部署系统的 模型 '}
#
#     school_id: Mapped[int] = mapped_column(primary_key=True, comment="学校ID")
#     institution_id: Mapped[int] = mapped_column(primary_key=True, comment="行政单位ID 例如区 市教育局")
#     unit_url: Mapped[str] = mapped_column(comment="api地址")
#     remark: Mapped[str] = mapped_column(comment="")
#     created_at: Mapped[datetime] = mapped_column(comment="创建时间")
