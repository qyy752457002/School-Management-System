from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date, datetime


class StudentKeyInfoChange(BaseDBModel):
    """
    学生id：student_id
    姓名拼音：name_pinyin
    届别：session
    年级：grade
    班级：classroom
    班号：class_number
    学校：school

    """
    __tablename__ = 'lfun_students_key_info_change'
    __table_args__ = {'comment': '学生关键信息变更表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键",
                                                 autoincrement=True)  # 与学生表关联，关系为一对一，主键

    student_id: Mapped[int] = mapped_column(nullable=False, comment="学生ID", autoincrement=True)  # 与学生表关联，关系为一对一，主键

    name_pinyin: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="姓名拼音")

    grade: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="年级")
    classroom: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="班级")
    class_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="班号")
    class_id: Mapped[int] = mapped_column(nullable=True, comment="班级id", default=0)
    grade_id: Mapped[int] = mapped_column(nullable=True, comment="年级id", default=0)

    school_id: Mapped[int] = mapped_column(nullable=True, comment="学校id", default=0)

    school: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校")
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
