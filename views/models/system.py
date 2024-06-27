from datetime import datetime
from enum import Enum
from typing import Final

from pydantic import BaseModel, Field
# 系统常量 定义在这里
GRADE_ENUM_KEY:Final = 'grade'
MAJOR_LV3_ENUM_KEY:Final = 'major_lv3'
DISTRICT_ENUM_KEY:Final = 'country'
STUDENT_TRANSFER_WORKFLOW_CODE:Final = 's_transfer_in_inner'
PLANNING_SCHOOL_OPEN_WORKFLOW_CODE:Final = 'p_school_open'

class UnitType(str, Enum):
    """
    """
    SCHOOL = "school"
    COUNTRY = "county"
    CITY = "city"

    @classmethod
    def to_list(cls):
        return [cls.CITY, cls.COUNTRY, cls.SCHOOL]

class SystemType(str, Enum):
    """
    """
    UNIT = "unit"
    STUDENT = "student"
    TEACHER = "teacher"

    @classmethod
    def to_list(cls):
        return [cls.UNIT, cls.STUDENT, cls.TEACHER]
class EduType(str, Enum):
    """
    """
    KG = "kg"
    K12 = "k12"
    VOCATIONAL = "vocational"

    @classmethod
    def to_list(cls):
        return [cls.KG, cls.K12, cls.VOCATIONAL]
class SystemConfig(BaseModel):
    """
     config_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项",default='')
    config_code: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项编码",default='')
    config_value: Mapped[str] = mapped_column(String(255),  nullable=True, comment="配置项值",default='')
    config_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="简述",default='')
    school_id: Mapped[int] = mapped_column(  nullable=True , comment="",default=0)
    """
    config_name: str = Field(..., title="",description="配置项",examples=[''])
    config_code: str = Field('', title="",description="配置项编码",examples=['02'])
    config_value: str = Field(..., title="",description="配置项值",examples=[''])
    config_remark: str = Field('', title="",description="简述",examples=[''])
    school_id: int = Field(0, title="",description="学校id",examples=['1'])
    created_uid: int = Field(0, title="",description="创建人",examples=['1'])
    updated_uid: int = Field(0, title="",description="操作人",examples=['1'])
    id: int = Field(0, title="",description="id",examples=['1'])
    # created_at: datetime|None = Field('',  description="",examples=[''])







