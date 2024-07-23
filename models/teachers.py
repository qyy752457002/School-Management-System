from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date
from enum import Enum


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

    teacher_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="教师ID")
    teacher_gender: Mapped[str] = mapped_column(String(64), nullable=True, default="", comment="教师性别")
    teacher_name: Mapped[str] = mapped_column(String(64), nullable=True, default="", comment="教师名称")
    teacher_id_type: Mapped[str] = mapped_column(String(64), nullable=True, default="", comment="证件类型")
    teacher_id_number: Mapped[str] = mapped_column(String(64), nullable=True, default="", comment="证件号")
    teacher_date_of_birth: Mapped[date] = mapped_column(Date, nullable=True, comment="出生日期")
    teacher_employer: Mapped[int] = mapped_column(BigInteger, default=0, nullable=True, comment="任职单位")
    teacher_avatar: Mapped[str] = mapped_column(nullable=True, default="", comment="头像")  # 图像处理再定
    teacher_main_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="主状态",
                                                     default="unemployed")
    teacher_sub_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="子状态",
                                                    default="unsubmitted")
    identity: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份", default='')
    identity_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份类型", default='')
    mobile: Mapped[str] = mapped_column(String(64), nullable=True, default="", comment="手机号")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    is_approval: Mapped[bool] = mapped_column(default=False, comment="是否在审批中")
