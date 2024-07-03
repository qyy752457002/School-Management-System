from datetime import datetime, date

from sqlalchemy import String, DateTime, Date, BigInteger,BIGINT
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TeacherRetire(BaseDBModel):

    __tablename__ = 'lfun_teacher_retire'
    __table_args__ = {'comment': '教师离退休表'}

    teacher_retire_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="变动主键id")
    teacher_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="教师ID")  # 与教师表关联，关系为一对n
    transaction_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="变动类型", default='')
    transaction_remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注", default='')
    retire_date: Mapped[date] = mapped_column(Date, nullable=True, comment="任职日期")
    transaction_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), nullable=False,
                                                       comment="操作时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
