from enum import Enum

from pydantic import BaseModel, Field

class UnitType(str, Enum):
    """
    """
    SCHOOL = "school"
    COUNTRY = "county"
    CITY = "city"

    @classmethod
    def to_list(cls):
        return [cls.CITY, cls.COUNTRY, cls.SCHOOL]

