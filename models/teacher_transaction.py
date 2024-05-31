from datetime import datetime, date

from sqlalchemy import String, DateTime, TIMESTAMP, func, Date
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
    transaction_id: Mapped[int] = mapped_column(primary_key=True, comment="教师变动ID", autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(nullable=True, comment="教师ID", default=0)  # 与教师表关联，关系为一对n
    transaction_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="异动类型", default='')
    transaction_reason: Mapped[str] = mapped_column(String(255), nullable=False, comment="异动原因", default='')
    transaction_remark: Mapped[str] = mapped_column(String(255), nullable=False, comment="备注", default='')
    original_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="原任职岗位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="现任职岗位")
    position_date: Mapped[date] = mapped_column(Date, nullable=False, comment="任职日期")
    transaction_time: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.current_timestamp(), nullable=False,
                                                       comment="创建时间")
    operator_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="操作人", default='')
    operator_id: Mapped[int] = mapped_column(nullable=False, comment="操作人ID", default=0)
    # approval_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="审批人", default='')
    # approval_id: Mapped[int] = mapped_column(nullable=True, comment="审批人ID", default=0)
    # approval_time: Mapped[datetime] = mapped_column(TIMESTAMP, default=func.now(), nullable=False, comment="创建时间")
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="submitting")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
