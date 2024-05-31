from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class WorkFlowNodeDepend(BaseDBModel):
    """
    work_flow_node_depend：work_flow_node_depend_id
    依赖code：depend_code
    来源节点：source_node
    下一个节点：next_node
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow_node_depend'
    __table_args__ = {'comment': 'work_flow_node_depend信息表'}

    depend_code: Mapped[int] = mapped_column(primary_key=True, comment="work_flow_node_dependID")
    source_node: Mapped[str] = mapped_column(String(64), nullable=False, comment="来源节点")#外键到work_flow_node_define表
    next_node: Mapped[str] = mapped_column(String(64), nullable=False, comment="下一个节点")#外键到work_flow_node_define表
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
