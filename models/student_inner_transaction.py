from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class StudentInnerTransaction(BaseDBModel):

    """
    学生校内异动表
    异动类型
    异动原因
    备注
    操作人
    操作时间
    审批状态

    """
    __tablename__ = 'lfun_student_inner_transaction'
    __table_args__ = {'comment': '学生校内异动表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="ID",autoincrement=False)
    student_id: Mapped[int] = mapped_column(BigInteger,nullable=True , comment="学生ID",default=0)  #
    school_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="学校ID", default=0)
    class_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="班级id", default='')

    transaction_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="异动类型",default='')
    transaction_reason: Mapped[str] = mapped_column(String(255),  nullable=True, comment="异动原因",default='')
    transaction_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="备注",default='')
    transaction_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="操作时间")
    transaction_user: Mapped[str] = mapped_column(String(255),  nullable=True, comment="操作人",default='')
    transaction_user_id: Mapped[int] = mapped_column(  nullable=True , comment="操作人ID",default=0)

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                         default="")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





