from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, BigInteger
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

    transaction_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="变动主键id")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")  # 与教师表关联，关系为一对n
    transaction_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="变动类型", default='')
    transaction_remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注", default='')
    original_position: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="原任职岗位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="现任职岗位")
    position_date: Mapped[date] = mapped_column(Date, nullable=True, comment="任职日期")
    transaction_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
                                                       comment="操作时间")
    is_active: Mapped[bool] = mapped_column(nullable=False, comment="是否已经恢复在职", default=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
