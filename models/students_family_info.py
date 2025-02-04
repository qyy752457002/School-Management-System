from sqlalchemy import String, Date, BigInteger
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

    student_family_info_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="ID", autoincrement=False)  # 主键
    student_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="学生ID")  # 外键，与学生表关联，关系为一对多
    name: Mapped[str] = mapped_column(String(64), nullable=True, comment="姓名")
    gender: Mapped[str] = mapped_column(String(64), nullable=True, comment="性别")
    relationship: Mapped[str] = mapped_column(String(64), nullable=True, comment="关系枚举relation")
    is_guardian: Mapped[bool] = mapped_column( default=False, nullable=True, comment="是否监护人")
    identification_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="证件类型")
    identification_number: Mapped[str] = mapped_column(String(255), nullable=True, comment="证件号码")
    birthday: Mapped[date] = mapped_column(Date, nullable=True, comment="出生日期")
    phone_number: Mapped[str] = mapped_column(String(255), nullable=True, comment="手机号")
    ethnicity: Mapped[str] = mapped_column(String(64), nullable=True, comment="民族")
    health_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="健康状态")
    nationality: Mapped[str] = mapped_column(String(64), nullable=True, comment="国籍")
    political_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="政治面貌")
    contact_address: Mapped[str] = mapped_column(String(64), nullable=True, comment="联系地址")
    workplace: Mapped[str] = mapped_column(String(255), nullable=True, comment="工作单位")
    identity: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份",default='')
    identity_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份类型",default='')
    # 职业(family_member_occupation)
    family_member_occupation: Mapped[str] = mapped_column(String(128), nullable=True,default='', comment="家庭成员职业枚举family_member_occupation")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
