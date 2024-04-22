from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Grade(BaseDBModel):
    """
    年级表
    """
    __tablename__ = 'lfun_grade'
    __table_args__ = {'comment': '年级表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="年级ID",autoincrement=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID")
    grade_no: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级编号")
    grade_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级名称")
    grade_alias: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级别名")
    description: Mapped[str] = mapped_column(String(64), nullable=False, comment="简介")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
