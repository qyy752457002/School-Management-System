from enum import Enum
from typing import Final

from pydantic import BaseModel, Field

GRADE_ENUM_KEY:Final = 'grade'

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
