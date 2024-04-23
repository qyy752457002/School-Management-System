from enum import Enum


class Gender(str, Enum):
    """
    性别
    """
    MALE = "male"
    FEMALE = "female"

    @classmethod
    def to_list(cls):
        return [cls.FEMALE, cls.MALE]


class YesOrNo(str, Enum):
    """
    是否
    """
    YES = "yes"
    NO = "no"

    @classmethod
    def to_list(cls):
        return [cls.YES, cls.NO]

