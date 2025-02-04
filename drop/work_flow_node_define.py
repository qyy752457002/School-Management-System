from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date


class WorkFlowNodeDefine(BaseDBModel):
    """
    节点id：node_id
    流程code：process_code
    节点名称：node_name
    节点code：node_code
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow_node_define'
    __table_args__ = {'comment': 'work_flow_node_define信息表'}

    node_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="work_flow_node_defineID")
    node_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="节点code")
    process_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程code,外键到work_flow_define表")
    node_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="节点名称")
    # required_role: Mapped[str] = mapped_column(String(64), nullable=False, comment="需要的角色")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
