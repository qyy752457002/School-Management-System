from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import datetime


class WorkFlowNodeInstance(BaseDBModel):
    """
    节点实例id：node_instance_id
    流程实例id：process_instance_id
    节点定义的id：node_code
    节点状态：node_status
    操作人角色：operator_role
    操作人id：operator_id
    操作时间：operation_time
    操作：action
    说明：description
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow_node_instance'
    __table_args__ = {'comment': 'work_flow_node_instance信息表'}

    node_instance_id: Mapped[int] = mapped_column(primary_key=True, comment="节点实例id", autoincrement=True)
    process_instance_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程实例id")
    node_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="关联到节点定义表")
    node_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="节点状态")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID", default=0)
    # operator_role: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人角色")
    operator_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人姓名")
    operation_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="操作时间")
    created_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="创建时间")
    action: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作")
    description: Mapped[str] = mapped_column(String(64), nullable=False, comment="说明")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
