from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TeacherKeyInfoApproval(BaseDBModel):
    """
    教师入职审批表
    操作人
    教师ID
    操作时间
    审批状态
    """
    __tablename__ = 'lfun_teacher_key_info_approval'
    __table_args__ = {'comment': '教师关键信息修改审批表'}

    teacher_key_info_approval_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="审批主键id")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")  # 与教师表关联，关系为一对n
    teacher_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="教师姓名", default='')
    # creat_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
    #                                                    comment="操作时间")
    # operator_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="操作人", default='')
    # operator_id: Mapped[int] = mapped_column(nullable=False, comment="操作人ID", default=0)
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="submitted")
    process_instance_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="流程ID", default=0)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)