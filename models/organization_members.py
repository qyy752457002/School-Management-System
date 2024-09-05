from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class OrganizationMembers(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_organization_members'
    __table_args__ = {'comment': '组织部门成员表模型'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID", autoincrement=False)
    org_id: Mapped[int] = mapped_column(BigInteger, comment="部门ID", default=0, nullable=True)
    # 要求 这里出现的所有人必须在 教师表里有 
    teacher_id: Mapped[int] = mapped_column(BigInteger, comment="教师ID", default=0, nullable=True)

    member_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="姓名")

    member_type: Mapped[str] = mapped_column(String(64), nullable=True, default='老师',
                                             comment="成员类型/岗位 例如老师 领导 职工等")
    birthday: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="生日")
    gender: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="性别")
    mobile: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="手机")
    card_type: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="证件类型")
    card_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="证件号码")
    identity: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份", default='')

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=True, comment="删除态", default=False)
