from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class UploadRecords(BaseDBModel):

    """
    上传记录表


    """
    __tablename__ = 'lfun_upload_records'
    __table_args__ = {'comment': '上传记录表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件名称",default='')
    file_path: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件路径",default='')
    file_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件类型",default='')
    file_size: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件大小",default='')
    file_status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件状态",default='')
    file_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="文件备注",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





