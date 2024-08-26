from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class GraduationStudent(BaseDBModel):
    """
     student_id: str = Field(..., title="学生id", description="学生id")
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    gender: str = Field(..., title="性别", description="性别")
    school: str = Field(..., title="学校", description="学校")
    county: str = Field(..., title="", description="行政属地")
    edu_number: str = Field(..., title="", description="学籍号码")
    class_id: str = Field(..., title="", description="班级")
    归档状态
    归档时间
    """
    __tablename__ = 'lfun_graduation_student'
    __table_args__ = {'comment': '毕业生表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID", autoincrement=True)
    student_id: Mapped[int] = mapped_column(String(32), nullable=False, comment="学生id", default=0)
    student_name: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学生姓名")
    gender: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="性别")
    school: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学校")
    school_id: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学校ID")
    county: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="行政属地")
    edu_number: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="学籍号码")
    class_id: Mapped[str] = mapped_column(String(32), nullable=False, comment="班级id")
    class_name: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="班级")

    status: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="毕业状态")

    graduation_date: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="毕业年份")
    graduation_remark: Mapped[str] = mapped_column(String(200), nullable=True, default='', comment="毕业备注")
    photo: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片", default='')  # 图像处理再定

    archive_status: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="归档状态")
    archive_date: Mapped[str] = mapped_column(String(32), nullable=True, default='', comment="归档年份")

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
