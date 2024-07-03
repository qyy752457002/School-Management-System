from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class WorkFlowNodeDependStrategy(BaseDBModel):
    """
    work_flow_node_depend_strategy：work_flow_node_depend_strategy_id
    依赖code：depend_code
    参数名：parameter_name
    参数值：parameter_value
    操作：action
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow_node_depend_strategy'
    __table_args__ = {'comment': 'work_flow_node_depend_strategy信息表'}

    work_flow_node_depend_strategy_id: Mapped[int] = mapped_column(primary_key=True, comment="work_flow_node_depend_strategyID")
    depend_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="依赖code")
    parameter_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="参数名")
    parameter_value: Mapped[str] = mapped_column(String(64), nullable=False, comment="参数值")
    operation: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
