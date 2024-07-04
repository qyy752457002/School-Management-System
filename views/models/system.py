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
PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE:Final = 'p_school_close'
PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE:Final = 'p_school_keyinfo_change'
SCHOOL_OPEN_WORKFLOW_CODE:Final = 's_school_open'
SCHOOL_CLOSE_WORKFLOW_CODE:Final = 's_school_close'
SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE:Final = 's_school_keyinfo_change'
INSTITUTION_OPEN_WORKFLOW_CODE:Final = 'i_institution_open'
INSTITUTION_CLOSE_WORKFLOW_CODE:Final = 'i_institution_close'
INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE:Final = 'i_institution_keyinfo_change'


class InstitutionType(str, Enum):
    """
    """
    INSTITUTION = "institution"
    ADMINISTRATION = "administration"
    @classmethod
    def to_list(cls):
        return [cls.INSTITUTION, cls.ADMINISTRATION,]
class ProcessCodeType(str, Enum):
    """
    """

    @classmethod
    def to_list(cls):
        return [
            PLANNING_SCHOOL_OPEN_WORKFLOW_CODE,
            PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE,
            PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE,
            SCHOOL_OPEN_WORKFLOW_CODE,
            SCHOOL_CLOSE_WORKFLOW_CODE,
            SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE,
            INSTITUTION_OPEN_WORKFLOW_CODE,
            INSTITUTION_CLOSE_WORKFLOW_CODE,
            INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE,
                 ]

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

class ImportScene(str, Enum):
    """ 导入场景的模版场景定义
    planning_school: '', // 学校模版模版
  school: '', // 分校模版
  new_teachers: '', // 新教师模版
  teachers_basic: '', // 教师基础信息模版
  teachers_shortcut: '', // 教师快捷模版
  teachers_extend: '', // 教师扩展信息模版
  institution: '', // 行政事业单位管理模版
  new_student: '', // 新学生模版
  class: '', // 班级模版
    """
    PLANNING_SCHOOL = "planning_school"
    SCHOOL = "school"
    NEW_TEACHERS = "new_teachers"
    TEACHERS_BASIC = "teachers_basic"
    TEACHERS_SHORTCUT = "teachers_shortcut"
    TEACHERS_EXTEND = "teachers_extend"
    INSTITUTION = "institution"
    NEWSTUDENT = "new_student"
    CLASS = "class"

    @classmethod
    def to_list(cls):
        return [cls.PLANNING_SCHOOL, cls.SCHOOL, cls.NEW_TEACHERS, cls.TEACHERS_BASIC, cls.TEACHERS_SHORTCUT,
                cls.TEACHERS_EXTEND, cls.INSTITUTION, cls.NEWSTUDENT, cls.CLASS
                ]
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
    id: int|str|None = Field('0', title="",description="id",examples=['1'])
    # created_at: datetime|None = Field('',  description="",examples=[''])







