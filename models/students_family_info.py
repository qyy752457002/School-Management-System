from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date


class StudentFamilyInfo(BaseDBModel):
    """
    学生id：student_id
    姓名：name
    性别：gender
    关系：relationship
    是否监护人：is_guardian
    证件类型：identification_type
    证件号码：identification_number
    出生日期：birthday
    手机号码：phone_number
    民族：ethnicity
    健康状态：health_status
    国籍：nationality
    政治面貌：political_status
    联系地址：contact_address
    工作单位：workplace
    家庭成员职业：family_member_occupation
    """
    __tablename__ = 'lfun_student_family_info'
    __table_args__ = {'comment': '学生家庭信息模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID", autoincrement=True)  # 主键
    student_id: Mapped[int] = mapped_column(nullable=False, comment="学生ID")  # 外键，与学生表关联，关系为一对多
    name: Mapped[str] = mapped_column(String(64), nullable=False, comment="姓名")
    gender: Mapped[str] = mapped_column(String(64), nullable=False, comment="性别")
    relationship: Mapped[str] = mapped_column(String(64), nullable=False, comment="关系")
    is_guardian: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否监护人")
    identification_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="证件类型")
    identification_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="证件号码")
    birthday: Mapped[date] = mapped_column(Date, nullable=False, comment="出生日期")
    phone_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="手机号")
    ethnicity: Mapped[str] = mapped_column(String(64), nullable=False, comment="民族")
    health_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="健康状态")
    nationality: Mapped[str] = mapped_column(String(64), nullable=False, comment="国籍")
    political_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="政治面貌")
    contact_address: Mapped[str] = mapped_column(String(64), nullable=False, comment="联系地址")
    workplace: Mapped[str] = mapped_column(String(64), nullable=False, comment="工作单位")
    family_member_occupation: Mapped[str] = mapped_column(String(64), nullable=False, comment="家庭成员职业")
    deleted: Mapped[int] = mapped_column(nullable=True, comment="删除态", default=0)
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
