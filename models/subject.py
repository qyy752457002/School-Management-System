from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Subject(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_subject'
    __table_args__ = {'comment': '课程表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="ID",autoincrement=False)
    subject_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="课程名称=年级+学科")
    subject_alias: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="课程别名")
    subject_level: Mapped[str] = mapped_column(String(64), nullable=True, default='',comment="课程等级 国家/地方/校本,枚举subject_level")
    course_name: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科名称")
    grade_id: Mapped[int] = mapped_column(BigInteger, comment="年级ID",default=0,nullable=True)
    school_id: Mapped[int] = mapped_column(BigInteger, comment="学校ID",nullable=True,default=0)
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码")

    subject_description: Mapped[str] = mapped_column(String(255), nullable=True,default='', comment="课程简介")
    subject_requirement: Mapped[str] = mapped_column(String(255), nullable=True,default='', comment="课程要求")
    credit_hour: Mapped[int] = mapped_column( comment="总学时",nullable=True,default=0)
    week_credit_hour: Mapped[int] = mapped_column( comment="周学时",nullable=True,default=0)
    self_study_credit_hour: Mapped[int] = mapped_column( comment="自学学时",nullable=True,default=0)
    teach_method: Mapped[str] = mapped_column(String(40), nullable=True,default='', comment="授课方式,枚举teach_method")
    textbook_code: Mapped[str] = mapped_column(String(40), nullable=True,default='', comment="教材编码")
    reference_book: Mapped[str] = mapped_column(String(40), nullable=True,default='', comment="参考书目")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    # @staticmethod
    # def seed():
    #     return [
    #
    #     ]



