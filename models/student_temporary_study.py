from datetime import datetime

from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped


class StudentTemporaryStudy(BaseDBModel):
    """

    """
    __tablename__ = 'lfun_student_temporary_study'
    __table_args__ = {'comment': '临时就读表'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="", autoincrement=False)
    student_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="学生ID", default=0)
    student_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="学生姓名", default='')
    id_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件号码",default='')
    student_gender: Mapped[str] = mapped_column(String(64), nullable=True, comment="学生性别",default='')
    edu_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学籍号",)
    student_no: Mapped[str] = mapped_column(String(255), nullable=True, comment="学号", default='')

    # 现在学校的情况
    school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="学校ID", default=0)
    session_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="届别id", default=0)
    grade_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="年级ID", default=0)

    class_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="班级id", default=0)
    # 原学校情况
    origin_school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="原学校ID", default=0)
    origin_session_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="原届别id", default=0)
    origin_grade_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="原年级ID", default=0)

    origin_class_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="原班级id", default=0)
    apply_user: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请人", default='')
    apply_time: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请时间", default='')

    doc_upload: Mapped[str] = mapped_column(String(255), nullable=True, comment="附件", default='')
    process_instance_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="流程ID", default=0)

    reason: Mapped[str] = mapped_column(String(255), nullable=True, comment="原因", default='')

    remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注", default='')
    status: Mapped[str] = mapped_column(String(64), nullable=True, comment="状态", default='')

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,   comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
