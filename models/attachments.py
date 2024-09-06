from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Attachment(BaseDBModel):

    """
    附件名称
    attach_name
    路径    path url


    """
    __tablename__ = 'lfun_attachments'
    __table_args__ = {'comment': '附件表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    attach_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件名称",default='')
    attach_path: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件路径",default='')
    attach_url: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件url",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
