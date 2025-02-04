from enum import Enum

from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class StudentSessionstatus(str, Enum):
    """
    """
    ENABLE = "enable"
    DISABLE = "disable"
    @classmethod
    def to_list(cls):
        return [cls.ENABLE, cls.DISABLE]
class StudentSession(BaseDBModel):
    """
    届别表
    """
    __tablename__ = 'lfun_student_session'
    __table_args__ = {'comment': '学生届别模型'}
    session_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="届别ID",autoincrement=False)#主键
    session_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="届别名称")
    session_alias: Mapped[str] = mapped_column(String(64), nullable=False, comment="届别别名")
    session_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="届别状态")
    year: Mapped[str] = mapped_column(String(64), nullable=True, comment="年度",default='')
    school_id: Mapped[int] = mapped_column( BigInteger,nullable=True  , comment="学校id",default=0)
    section: Mapped[str] = mapped_column(String(64), nullable=True, comment="学段",default='')
    major: Mapped[str] = mapped_column(String(64), nullable=True, comment="专业",default='')

