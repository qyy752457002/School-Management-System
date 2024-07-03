from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class OperationRecord(BaseDBModel):
    """
action_target_id: str = Field(..., title="操作对象ID", description="操作对象ID",examples=[''])
    action_type: str = Field(..., title="操作类型", description="操作类型",examples=[''])
    ip: str = Field(..., title=" Description",  description="操作IP",examples=[''])
    change_data: str = Field(..., title=" Author", description="变更前后数据",examples=[''])
    change_field: str = Field(...,   description=" 变更字段",examples=[''])
    change_item: str = Field(...,   description=" 变更项",examples=[''])
    timestamp: str = Field(...,   description="操作时间 ",examples=[''])
    action_reason: str = Field(...,   description=" 操作原因",examples=[''])
    doc_upload: str = Field(...,   description=" 附件",examples=[''])
    status: str = Field(...,   description=" 状态",examples=[''])
    account: str = Field(...,   description=" 操作账号",examples=[''])
    operator: str = Field(...,   description=" 操作人",examples=[''])
    module: str = Field(...,   description=" 操作模块",examples=[''])
    target: str = Field(...,   description=" 操作对象",examples=[''])
    """
    __tablename__ = 'lfun_operation_record'
    __table_args__ = {'comment': '操作记录表模型'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="班级ID")
    action_target_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="操作对象ID")
    target: Mapped[str] = mapped_column(String(255), nullable=True, comment=" 操作对象", default='')
    action_type: Mapped[str] = mapped_column(String(40), nullable=True, comment="操作类型", default='')
    ip: Mapped[str] = mapped_column(String(40), nullable=True, comment=" Description", default='')
    change_data: Mapped[str] = mapped_column(String(3072), nullable=True, comment="", default='')
    operation_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
                                                     comment="操作时间")
    doc_upload: Mapped[str] = mapped_column(String(255), nullable=True, comment=" 附件", default='')
    status: Mapped[str] = mapped_column(String(255), nullable=True, comment=" 状态", default='')

    operator_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment=" 操作人", default=0)
    operator_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="操作人姓名", default='')

    change_module: Mapped[str] = mapped_column(String(64), nullable=True, comment="变更模块")
    change_detail: Mapped[str] = mapped_column(String(64), nullable=True, comment="变更详情")

    process_instance_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="流程ID")

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
