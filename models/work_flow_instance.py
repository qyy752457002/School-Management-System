from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import datetime

class WorkFlowInstance(BaseDBModel):
    """
    流程实例id：process_instance_id
    流程定义id：process_code
    申请人id：applicant_id
    开始时间：start_time
    结束时间：end_time
    流程状态：process_status
    说明：description
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow__instance'
    __table_args__ = {'comment': 'work_flow__instance信息表'}

    process_instance_id: Mapped[str] = mapped_column(primary_key=True, comment="流程实例id")
    process_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="关联流程定义主键")
    applicant_id: Mapped[str] = mapped_column(String(64), nullable=False, comment="申请人id")
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="开始时间")
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="结束时间")
    process_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程状态")
    description: Mapped[str] = mapped_column(String(64), nullable=False, comment="说明")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
