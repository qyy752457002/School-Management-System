from enum import Enum


class Gender(str, Enum):
    """
    性别
    """
    MALE = "male"
    FEMALE = "female"
    NULL = ""

    @classmethod
    def to_list(cls):
        return [cls.FEMALE, cls.MALE, cls.NULL]

    @classmethod
    def to_dict(cls):
        return {"男": cls.MALE, "女": cls.FEMALE}

    @classmethod
    def from_chinese(cls, chinese):
        return cls.to_dict().get(chinese, cls.NULL)


class YesOrNo(str, Enum):
    """
    是否
    """
    YES = "Y"
    NO = "N"

    @classmethod
    def to_list(cls):
        return [cls.YES, cls.NO]


class IDtype(str, Enum):
    """
    { label: "居民身份证", value: "resident_identity_card"},
    { label: "外国人永久居留身份证", value: "wgr_yjjl_sfz"},
    { label: "港澳居民来往内地通行证", value: "ga_nd_txz"},
    { label: "外国(地区)护照", value: "id_card_type_passport"},
    { label: "其他", value: "id_card_type_other"}
    """
    RESIDENT_IDENTITY_CARD = "resident_identity_card"
    WGR_YJJL_SFZ = "wgr_yjjl_sfz"
    GA_ND_TXZ = "ga_nd_txz"
    ID_CARD_TYPE_PASSPORT = "id_card_type_passport"
    ID_CARD_TYPE_OTHER = "id_card_type_other"

    @classmethod
    def to_list(cls):
        return [cls.RESIDENT_IDENTITY_CARD, cls.WGR_YJJL_SFZ, cls.GA_ND_TXZ, cls.ID_CARD_TYPE_PASSPORT,
                cls.ID_CARD_TYPE_OTHER]

class IdentityType(str, Enum):
    """
    学生 - Student
    教职工 - Staff
    管理者 - Manager
    家长 - Parent
    第三方 - Third Party
    """
    STUDENT = "student_identity"
    STAFF = "staff_identity"
    MANAGER = "manager_identity"
    PARENT = "parent_identity"
    THIRD_PARTY = "third_party_identity"
    @classmethod
    def to_list(cls):
        return [cls.STUDENT, cls.STAFF, cls.MANAGER, cls.PARENT, cls.THIRD_PARTY]



class Section(str, Enum):
    """
    学段信息
    幼儿园 - kindergarten
    小学 - primary_school
    初中 - junior_middle_school
    高中 - high_school
    中职 - vocational_school
    """
    KINDERGARTEN = "kindergarten"
    PRIMARY_SCHOOL = "primary_school"
    JUNIOR_MIDDLE_SCHOOL = "junior_middle_school"
    HIGH_SCHOOL = "high_school"
    VOCATIONAL_SCHOOL = "vocational_school"

    @classmethod
    def to_list(cls):
        return [cls.KINDERGARTEN, cls.PRIMARY_SCHOOL, cls.JUNIOR_MIDDLE_SCHOOL, cls.HIGH_SCHOOL, cls.VOCATIONAL_SCHOOL]

    @classmethod
    def to_grade_level(cls):
        return {
            cls.KINDERGARTEN.value: 3,
            cls.PRIMARY_SCHOOL.value: 6,
            cls.JUNIOR_MIDDLE_SCHOOL.value: 3,
            cls.HIGH_SCHOOL.value: 3,
            cls.VOCATIONAL_SCHOOL.value: 0
        }
    @classmethod
    def get_grade_level(cls, key):
       return cls.to_grade_level().get(key, 0)
