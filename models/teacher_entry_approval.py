from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TeacherEntryApproval(BaseDBModel):
    """
    教师入职审批表
    操作人
    教师ID
    操作时间
    审批状态
    """
    __tablename__ = 'lfun_teacher_entry_approval'
    __table_args__ = {'comment': '教师入职审批表'}

    teacher_entry_approval_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="审批主键id")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID", unique=True)  # 与教师表关联，关系为一对n
    teacher_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="教师姓名")
    creat_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
                                                 comment="创建时间")
    # operator_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="操作人", default='')
    operator_id: Mapped[int] = mapped_column(nullable=False, comment="操作人ID", default=0)
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="pending")
    process_instance_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="流程ID", default=0)
