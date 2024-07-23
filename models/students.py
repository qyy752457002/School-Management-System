from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date
from enum import Enum

class StudentGraduatedType(str, Enum):
    """
    毕业
    结业
    肄业
    """
    GRADUATION = "graduation"
    COMPLETION = "completion"
    WITHDRAWAL = "withdrawal"
    @classmethod
    def to_list(cls):
        return [cls.GRADUATION, cls.COMPLETION, cls.WITHDRAWAL]

class StudentApprovalAtatus(str, Enum):
    """
    入学   存在2个模式  先入学  再分班 和先分班  再入学
    分班
    正式在校
    流出
    毕业
    归档完成

    """
    ENROLLMENT = "enrollment"
    ASSIGNMENT = "assignment"
    FORMAL = "formal"
    OUT = "out"
    GRADUATED = "graduated"
    ARCHIVED = "archived"

    @classmethod
    def to_list(cls):
        return [cls.ENROLLMENT, cls.ASSIGNMENT,cls.FORMAL, cls.OUT, cls.GRADUATED,cls.ARCHIVED]


class Relationship(str, Enum):
    """
    父亲
    母亲
    爷爷
    奶奶
    外公
    外婆
    其他

    """
    FATHER = "father"
    MOTHER = "mother"
    GRANDFATHER = "grandfather"
    GRANDMOTHER = "grandmother"
    PATERNAL_GRANDFATHER = "paternal_grandfather"
    PATERNAL_GRANDMOTHER = "paternal_grandmother"

    @classmethod
    def to_list(cls):
        return [cls.FATHER, cls.MOTHER, cls.GRANDFATHER, cls.GRANDMOTHER, cls.PATERNAL_GRANDFATHER,
                cls.PATERNAL_GRANDMOTHER]
    @classmethod
    def to_dict(cls):
        return {"父亲": cls.FATHER, "母亲": cls.MOTHER, "爷爷": cls.GRANDFATHER, "奶奶": cls.GRANDMOTHER, "外公": cls.PATERNAL_GRANDFATHER, "外婆": cls.PATERNAL_GRANDMOTHER}

    @classmethod
    def from_chinese(cls, chinese):
        return cls.to_dict().get(chinese, None)


class Registration(str, Enum):
    """
    农村
    县镇
    城市
    """
    RURAL = "rural_area"
    COUNTY = "county_town"
    CITY = "city"

    @classmethod
    def to_list(cls):
        return [cls.RURAL, cls.COUNTY, cls.CITY]


class HealthStatus(str, Enum):
    """
    健康
    一般
    较差
    """
    HEALTHY = "healthy"
    NORMAL = "normal"
    POOR = "poor"

    @classmethod
    def to_list(cls):
        return [cls.HEALTHY, cls.NORMAL, cls.POOR]


class BloodType(str, Enum):
    """
    A型
    B型
    AB型
    O型
    Rh阳性
    Rh阴性
    """
    A = "blood_type_a"
    B = "blood_type_b"
    AB = "blood_type_ab"
    O = "blood_type_o"
    RH_POSITIVE = "rh_positive"
    RH_NEGATIVE = "rh_negative"

    @classmethod
    def to_list(cls):
        return [cls.A, cls.B, cls.AB, cls.O, cls.RH_POSITIVE, cls.RH_NEGATIVE]


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

    student_id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="学生ID", autoincrement=False)  # 主键
    student_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="学生姓名")
    student_gender: Mapped[str] = mapped_column(String(64), nullable=True, comment="学生性别")
    enrollment_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="报名号")
    birthday: Mapped[date] = mapped_column(Date, nullable=True, comment="生日", default='')
    id_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件类别")
    id_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件号码")
    photo: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片")  # 图像处理再定
    approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="状态", default="enrollment")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
