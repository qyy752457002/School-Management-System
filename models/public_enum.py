from enum import Enum

class OrgIdentity(str, Enum):
    """
    幼儿园学生-kindergarten_student
    小学学生-primary_school_student
    初中学生-middle_school_student
    高中学生-high_school_student
    中职学生-vocational_student
    幼儿园幼师-kindergarten_teacher
    小学专任教师-primary_school_teacher
    初中专任教师-middle_school_teacher
    高中专任教师-high_school_teacher
    中等职业学校专任教师-vocational_teacher
    九年一贯制学校专任教师-nine_year_teacher
    十二年一贯制学校专任教师-twelve_year_teacher
    特殊教育学校专任教师-special_education_teacher
    完全中学专任老师-full_secondary_school_teacher
    幼儿园职工-kindergarten_staff
    小学职工-primary_school_staff
    初中职工-middle_school_staff
    高中职工-high_school_staff
    中等职业学校职工-vocational_staff
    九年一贯制学校职工-nine_year_staff
    十二年一贯制学校职工-twelve_year_staff
    特殊教育学校职工-special_education_staff
    教育单位职工-education_unit_staff
    幼儿园校长-kindergarten_principal
    小学校长-primary_school_principal
    初中校长-middle_school_principal
    高中校长-high_school_principal
    中等职业学校校长-vocational_principal
    九年一贯制学校校长-nine_year_principal
    十二年一贯制学校校长-twelve_year_principal
    特殊教育学校校长-special_education_principal
    幼儿园家长-kindergarten_parent
    小学家长-primary_school_parent
    初中家长-middle_school_parent
    高中家长-high_school_parent
    中等职业学校家长-vocational_parent
    技术人员-technical_staff
    运维人员-operation_staff
    """
    KINDERGARTEN_STUDENT = "kindergarten_student"
    PRIMARY_SCHOOL_STUDENT = "primary_school_student"
    MIDDLE_SCHOOL_STUDENT = "middle_school_student"
    HIGH_SCHOOL_STUDENT = "high_school_student"
    VOCATIONAL_STUDENT = "vocational_student"
    KINDERGARTEN_TEACHER = "kindergarten_teacher"
    PRIMARY_SCHOOL_TEACHER = "primary_school_teacher"
    MIDDLE_SCHOOL_TEACHER = "middle_school_teacher"
    HIGH_SCHOOL_TEACHER = "high_school_teacher"
    VOCATIONAL_TEACHER = "vocational_teacher"
    NINE_YEAR_TEACHER = "nine_year_teacher"
    TWELVE_YEAR_TEACHER = "twelve_year_teacher"
    SPECIAL_EDUCATION_TEACHER = "special_education_teacher"
    KINDERGARTEN_STAFF = "kindergarten_staff"
    PRIMARY_SCHOOL_STAFF = "primary_school_staff"
    MIDDLE_SCHOOL_STAFF = "middle_school_staff"
    HIGH_SCHOOL_STAFF = "high_school_staff"
    VOCATIONAL_STAFF = "vocational_staff"
    NINE_YEAR_STAFF = "nine_year_staff"
    TWELVE_YEAR_STAFF = "twelve_year_staff"
    SPECIAL_EDUCATION_STAFF = "special_education_staff"
    EDUCATION_UNIT_STAFF = "education_unit_staff"
    KINDERGARTEN_PRINCIPAL = "kindergarten_principal"
    PRIMARY_SCHOOL_PRINCIPAL = "primary_school_principal"
    MIDDLE_SCHOOL_PRINCIPAL = "middle_school_principal"
    HIGH_SCHOOL_PRINCIPAL = "high_school_principal"
    VOCATIONAL_PRINCIPAL = "vocational_principal"
    NINE_YEAR_PRINCIPAL = "nine_year_principal"
    TWELVE_YEAR_PRINCIPAL = "twelve_year_principal"
    SPECIAL_EDUCATION_PRINCIPAL = "special_education_principal"
    KINDERGARTEN_PARENT = "kindergarten_parent"
    PRIMARY_SCHOOL_PARENT = "primary_school_parent"
    MIDDLE_SCHOOL_PARENT = "middle_school_parent"
    HIGH_SCHOOL_PARENT = "high_school_parent"
    VOCATIONAL_PARENT = "vocational_parent"
    TECHNICAL_STAFF = "technical_staff"
    OPERATION_STAFF = "operation_staff"
    FULL_SECONDARY_SCHOOL_TEACHER = "full_secondary_school_teacher"

    @classmethod
    def to_dict(cls):
        return {
            "幼儿园学生": cls.KINDERGARTEN_STUDENT,
            "小学学生": cls.PRIMARY_SCHOOL_STUDENT,
            "初中学生": cls.MIDDLE_SCHOOL_STUDENT,
            "高中学生": cls.HIGH_SCHOOL_STUDENT,
            "中职学生": cls.VOCATIONAL_STUDENT,
            "幼儿园幼师": cls.KINDERGARTEN_TEACHER,
            "小学专任教师": cls.PRIMARY_SCHOOL_TEACHER,
            "初中专任教师": cls.MIDDLE_SCHOOL_TEACHER,
            "高中专任教师": cls.HIGH_SCHOOL_TEACHER,
            "中等职业学校专任教师": cls.VOCATIONAL_TEACHER,
            "九年一贯制学校专任教师": cls.NINE_YEAR_TEACHER,
            "十二年一贯制学校专任教师": cls.TWELVE_YEAR_TEACHER,
            "特殊教育学校专任教师": cls.SPECIAL_EDUCATION_TEACHER,
            "幼儿园职工": cls.KINDERGARTEN_STAFF,
            "小学职工": cls.PRIMARY_SCHOOL_STAFF,
            "初中职工": cls.MIDDLE_SCHOOL_STAFF,
            "高中职工": cls.HIGH_SCHOOL_STAFF,
            "中等职业学校职工": cls.VOCATIONAL_STAFF,
            "九年一贯制学校职工": cls.NINE_YEAR_STAFF,
            "十二年一贯制学校职工": cls.TWELVE_YEAR_STAFF,
            "特殊教育学校职工": cls.SPECIAL_EDUCATION_STAFF,
            "教育单位职工": cls.EDUCATION_UNIT_STAFF,
            "幼儿园校长": cls.KINDERGARTEN_PRINCIPAL,
            "小学校长": cls.PRIMARY_SCHOOL_PRINCIPAL,
            "初中校长": cls.MIDDLE_SCHOOL_PRINCIPAL,
            "高中校长": cls.HIGH_SCHOOL_PRINCIPAL,
            "中等职业学校校长": cls.VOCATIONAL_PRINCIPAL,
            "九年一贯制学校校长": cls.NINE_YEAR_PRINCIPAL,
            "十二年一贯制学校校长": cls.TWELVE_YEAR_PRINCIPAL,
            "特殊教育学校校长": cls.SPECIAL_EDUCATION_PRINCIPAL,
            "幼儿园家长": cls.KINDERGARTEN_PARENT,
            "小学家长": cls.PRIMARY_SCHOOL_PARENT,
            "初中家长": cls.MIDDLE_SCHOOL_PARENT,
            "高中家长": cls.HIGH_SCHOOL_PARENT,
            "中等职业学校家长": cls.VOCATIONAL_PARENT,
            "技术人员": cls.TECHNICAL_STAFF,
            "运维人员": cls.OPERATION_STAFF,
            "完全中学专任教师": cls.FULL_SECONDARY_SCHOOL_TEACHER
        }

    @classmethod
    def from_chinese(cls, chinese_value: str):
        return cls.to_dict().get(chinese_value)



class OrgIdentityType(str, Enum):
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

    @classmethod
    def to_dict(cls):
        return {"学生": cls.STUDENT, "教职工": cls.STAFF, "管理者": cls.MANAGER, "家长": cls.PARENT,
                "第三方": cls.THIRD_PARTY}

    @classmethod
    def from_chinese(cls, chinese_value: str):
        return cls.to_dict().get(chinese_value)




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
