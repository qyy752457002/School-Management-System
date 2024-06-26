from datetime import datetime, date

from sqlalchemy import String, DateTime, Date
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TeacherTransaction(BaseDBModel):
    """
    教师校内异动表
    异动类型
    异动原因
    备注
    操作人
    教师ID
    操作时间
    审批状态

    """
    __tablename__ = 'lfun_teacher_transaction'
    __table_args__ = {'comment': '教师变动修改表'}

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="变动主键id")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")  # 与教师表关联，关系为一对n

    transaction_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="变动类型", default='')
    transaction_remark: Mapped[str] = mapped_column(String(255), nullable=False, comment="备注", default='')
    original_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="原任职岗位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="现任职岗位")
    position_date: Mapped[date|None] = mapped_column(Date, nullable=True, comment="任职日期")
    transaction_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
                                                       comment="操作时间")
    operator_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="操作人", default='')
    operator_id: Mapped[int] = mapped_column(nullable=False, comment="操作人ID", default=0)
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="pending")
    process_instance_id: Mapped[int] = mapped_column(nullable=False, comment="流程ID", default=0)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
