from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date
from enum import Enum


class TeacherApprovalAtatus(str, Enum):
    """
    待提交
    待审核
    已通过
    已拒绝
    """
    SUBMITTING = "submitting"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"

    @classmethod
    def to_list(cls):
        return [cls.SUBMITTING, cls.SUBMITTED, cls.APPROVED, cls.REJECTED]

# class Gender(str, Enum):



class Teacher(BaseDBModel):
    """
    教师表
    教师ID：teacher_id
    用户名：username
    密码：hash_password
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    任职单位：teacher_employer
    头像：teacher_avatar
    审批状态：teacher_approval_status

    """

    __tablename__ = 'lfun_teachers'
    __table_args__ = {'comment': '教师表模型'}

    teacher_id: Mapped[int] = mapped_column(primary_key=True, comment="教师ID", autoincrement=True)
    teacher_gender: Mapped[str] = mapped_column(String(64), nullable=True,default="", comment="教师性别")
    teacher_name: Mapped[str] = mapped_column(String(64), nullable=True,default="", comment="教师名称")
    teacher_id_type: Mapped[str] = mapped_column(String(64), nullable=True,default="", comment="证件类型")
    teacher_id_number: Mapped[str] = mapped_column(String(64), nullable=True,default="", comment="证件号")
    teacher_date_of_birth: Mapped[date] = mapped_column(Date, nullable=True, comment="出生日期")
    teacher_employer: Mapped[int] = mapped_column(default=0, nullable=True, comment="任职单位")
    teacher_avatar: Mapped[str] = mapped_column(String(64), nullable=True, default="",comment="头像")  # 图像处理再定
    teacher_approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="审批状态",
                                                         default="submitting")  # 审批状态待定
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")

