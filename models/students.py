from sqlalchemy import String,Date
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date

class Student(BaseDBModel):
    """
    学生id：student_id
    学生姓名：student_name
    学生性别：student_gender
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    照片：photo
    审核状态：approval_status

    """
    __tablename__ = 'lfun_students'
    __table_args__ = {'comment': '学生表关键信息模型'}

    student_id: Mapped[int] = mapped_column(primary_key=True, comment="学生ID",autoincrement=True)#主键
    student_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生姓名")
    student_gender: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生性别")
    enrollment_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="报名号")
    birthday: Mapped[date] = mapped_column(Date, nullable=False, comment="生日")
    gender: Mapped[str] = mapped_column(String(64), nullable=True, comment="性别")
    id_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件类别")
    id_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件号码")
    photo: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片") #图像处理再定
    deleted: Mapped[int] = mapped_column(nullable=True, comment="删除态", default=0)
    approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="状态",default="分班")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")


