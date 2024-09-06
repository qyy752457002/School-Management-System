from datetime import datetime, date
from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import String, DateTime, BigInteger, Date
from sqlalchemy.orm import mapped_column, Mapped


class GraduationStudent(BaseDBModel):
    """
    归档状态
    归档时间
    """
    __tablename__ = 'lfun_graduation_student'
    __table_args__ = {'comment': '毕业生表模型'}

    student_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="学生ID", )
    student_name: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学生姓名")
    school: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学校")
    school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="学校id", default=0)
    borough: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="行政属地")
    edu_number: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学籍号码")
    class_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="班级id", default=0)
    session: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="届别")
    session_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="届别id", default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="毕业状态")
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True, comment="出生日期")
    graduation_remark: Mapped[str] = mapped_column(String(200), nullable=True, default='', comment="毕业备注")
    photo: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片", default='')  # 图像处理再定
    archive_status: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否已归档")
    archive_date: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="归档年份")
    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
