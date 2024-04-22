from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class SubDbInfo(BaseDBModel):
    """
    sync_log_id
sync_task_id
source_system
target_system
sync_entity_type
sync_start_date
sync_end_date
total_records
successful_records
failed_records
sync_status
error_message
error_stack_trace
last_updated_time
    """
    __tablename__ = 'lfun_data_sync_records'
    __table_args__ = {'comment': '数据同步记录表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    sync_log_id: Mapped[int] = mapped_column(  nullable=True , comment="同步日志ID",default=0)
    sync_task_id: Mapped[int] = mapped_column(  nullable=True , comment="同步任务ID",default=0)
    source_system: Mapped[str] = mapped_column(String(255),  nullable=True, comment="源系统",default='')
    target_system: Mapped[str] = mapped_column(String(255),  nullable=True, comment="目标系统",default='')
    sync_entity_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="同步实体类型",default='')
    sync_start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="同步开始时间")
    sync_end_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="同步结束时间")
    total_records: Mapped[int] = mapped_column(  nullable=True , comment="总记录数",default=0)
    successful_records: Mapped[int] = mapped_column(  nullable=True , comment="成功记录数",default=0)
    failed_records: Mapped[int] = mapped_column(  nullable=True , comment="失败记录数",default=0)
    sync_status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="同步状态",default='')
    error_message: Mapped[str] = mapped_column(String(255),  nullable=True, comment="错误消息",default='')
    error_stack_trace: Mapped[str] = mapped_column(String(255),  nullable=True, comment="错误堆栈",default='')
    last_updated_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="最后更新时间")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





