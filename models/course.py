from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Course(BaseDBModel):
    """
    school_id: str = Field(..., title="学校ID", description="学校ID",examples=[''])
    course_no: str = Field(..., title="", description="课程编码",examples=['19'])
    grade_id: str = Field(None, title="年级ID", description="年级ID",examples=['一年级'])

    course_name: str = Field(..., title="Grade_name",description="课程名称",examples=['语文'])
    """
    __tablename__ = 'lfun_course'
    __table_args__ = {'comment': '课程表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID",nullable=True,default=0)
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="课程编码")
    grade_id: Mapped[int] = mapped_column( comment="年级ID",nullable=True,default=0)
    course_name: Mapped[str] = mapped_column(String(24), nullable=False, comment="课程名称")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)



