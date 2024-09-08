from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class StudentTransactionFlow(BaseDBModel):

    """
    转学休学入学毕业申请流程表
    申请ID
    阶段
    流程描述
    流程备注

    """
    __tablename__ = 'lfun_student_transaction_flow'
    __table_args__ = {'comment': '转学休学入学毕业申请流程表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    student_id: Mapped[int] = mapped_column(nullable=True , comment="学生ID",default=0)
    apply_id: Mapped[int] = mapped_column(nullable=True , comment="申请ID",default=0)

    stage: Mapped[str] = mapped_column(String(255),  nullable=True, comment="阶段",default='')
    description: Mapped[str] = mapped_column(String(600),  nullable=True, comment="流程描述",default='')
    remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程备注",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
