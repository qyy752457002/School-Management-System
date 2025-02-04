from datetime import date, datetime
from enum import Enum
from typing import Optional

from fastapi import Query
from mini_framework.storage.view_model import FileStorageModel
from pydantic import BaseModel, Field, model_validator

from business_exceptions.teacher import EthnicityNoneError, PoliticalStatusNoneError
from models.public_enum import Gender
from views.models.operation_record import ChangeModule


class TeacherMainStatus(str, Enum):
    """
    未入职：unemployed
    在职：employed
    离退休：retired
    """
    UNEMPLOYED = "unemployed"
    EMPLOYED = "employed"
    RETIRED = "retired"

    @classmethod
    def to_list(cls):
        return [cls.UNEMPLOYED, cls.EMPLOYED, cls.RETIRED]


class IdentityType(str, Enum):
    RESIDENT_ID_CARD = "resident_id_card"
    MILITARY_OFFICER_ID = "military_officer_id"
    SOLDIER_ID = "soldier_id"
    CIVILIAN_OFFICER_ID = "civilian_officer_id"
    MILITARY_RETIRE_ID = "military_retiree_id"
    HONG_KONG_PASSPORT_ID = "hong_kong_passport_id"
    MACAU_PASSPORT_ID = "macau_passport_id"
    TAIWAN_RESIDENT_TRAVEL_PERMIT = "taiwan_resident_travel_permit"
    OVERSEAS_PERMANENT_RESIDENCE_PERMIT = "overseas_permanent_residence_permit"
    PASSPORT = "passport"
    BIRTH_CERTIFICATE = "birth_certificate"
    HOUSEHOLD_REGISTER = "household_register"
    OTHER = "other"
    UNKNOWN = "unknown"

    @classmethod
    def to_dict(cls):
        return {
            "居民身份证": cls.RESIDENT_ID_CARD,
            "军官证": cls.MILITARY_OFFICER_ID,
            "士兵证": cls.SOLDIER_ID,
            "文职干部证": cls.CIVILIAN_OFFICER_ID,
            "部队离退休证": cls.MILITARY_RETIRE_ID,
            "香港特区护照/身份证明": cls.HONG_KONG_PASSPORT_ID,
            "澳门特区护照/身份证明": cls.MACAU_PASSPORT_ID,
            "台湾居民来往大陆通行证": cls.TAIWAN_RESIDENT_TRAVEL_PERMIT,
            "境外永久居住证": cls.OVERSEAS_PERMANENT_RESIDENCE_PERMIT,
            "护照": cls.PASSPORT,
            "出生证明": cls.BIRTH_CERTIFICATE,
            "户口薄": cls.HOUSEHOLD_REGISTER,
            "其他": cls.OTHER
        }

    @classmethod
    def to_org(cls):
        return {
            cls.RESIDENT_ID_CARD.value: "resident_identity_card",
            cls.HONG_KONG_PASSPORT_ID.value: "hong_kong_passport_id",
            cls.MACAU_PASSPORT_ID.value: "macao_passport_id",
            cls.TAIWAN_RESIDENT_TRAVEL_PERMIT.value: "taiwan_pass",
            cls.OVERSEAS_PERMANENT_RESIDENCE_PERMIT.value: "permanent_residence_permit",
            cls.PASSPORT.value: "passport",
            cls.BIRTH_CERTIFICATE.value: "birth_certificate",
            cls.HOUSEHOLD_REGISTER.value: "household_register",
            cls.OTHER.value: "other",
        }

    @classmethod
    def from_to_org(cls, local_value: str):
        result = cls.to_org().get(local_value)
        if result is None:
            # 使用 cls.OTHER.value 作为参数再次查找
            result = cls.to_org().get(cls.OTHER.value)
        return result

    # 中文到枚举值的映射
    @classmethod
    def from_chinese(cls, chinese_value: str):
        return cls.to_dict().get(chinese_value, cls.UNKNOWN)

    @classmethod
    def to_list(cls):
        return [cls.RESIDENT_ID_CARD, cls.MILITARY_OFFICER_ID, cls.SOLDIER_ID, cls.CIVILIAN_OFFICER_ID,
                cls.MILITARY_RETIRE_ID, cls.HONG_KONG_PASSPORT_ID, cls.MACAU_PASSPORT_ID,
                cls.TAIWAN_RESIDENT_TRAVEL_PERMIT, cls.OVERSEAS_PERMANENT_RESIDENCE_PERMIT, cls.PASSPORT,
                cls.BIRTH_CERTIFICATE, cls.HOUSEHOLD_REGISTER, cls.OTHER]


class Teachers(BaseModel):
    """
    教师ID:teacher_id
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_id: int | str = Field(None, title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int | str = Field(0, title="单位部门", description="单位部门")
    teacher_avatar: str | None = Field("", title="头像", description="头像")
    teacher_avatar_url: str | None = Field("", title="头像url", description="头像url")
    mobile: str | None = Field("", title="手机号", description="手机号")
    teacher_main_status: str = Field("", title="主状态", description="主状态")
    teacher_sub_status: str = Field("", title="子状态", description="子状态")
    teacher_code: str = Field(..., title="教师编码", description="教师编码")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_employer"]
        # 需要给身份证脱敏
        # if isinstance(data["teacher_id"], int):
        #     if data.get("teacher_id_number"):
        #         if len(data["teacher_id_number"]) == 18:
        #             data["teacher_id_number"] = data["teacher_id_number"][0:6] + "********" + data["teacher_id_number"][
        #                                                                                       -4:]
        #         # 其他类型的证件号码值只对最后四位脱敏
        #         elif len(data["teacher_id_number"]) > 0:
        #             data["teacher_id_number"] = data["teacher_id_number"][0:-4] + "****"
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class EducateUserModel(BaseModel):
    """
    往组织中心加用户
    """
    avatar: str | None = Field("", title="头像", description="头像")
    birthDate: date | None = Field(None, title="出生日期", description="出生日期")
    createdTime: str | None = Field("", title="创建时间", description="创建时间")
    currentUnit: str | None = Field("", title="所在单位", description="当前单位")
    departmentId: str | None = Field("", title="部门ID", description="部门ID")
    departmentNames: str | None = Field("", title="部门名称", description="部门名称")
    email: str | None = Field("", title="邮箱", description="邮箱")
    gender: str | None = Field("", title="性别", description="性别")
    idCardNumber: str | None = Field("", title="身份证号", description="身份证号")
    idCardType: str | None = Field("", title="证件类型", description="证件类型")
    identity: str | None = Field("", title="身份", description="身份")
    identityNames: str | None = Field("", title="身份名称", description="身份名称")
    identityType: str | None = Field("", title="身份类型", description="身份类型")
    identityTypeNames: str | None = Field("", title="身份类型名称", description="身份类型名称")
    mainUnitName: str | None = Field("", title="主单位名称", description="主单位名称")
    name: str | None = Field("", title="登录账号", description="登录账号")
    owner: str | None = Field("", title="所属组织", description="所属组织")
    phoneNumber: str | None = Field("", title="手机号", description="手机号")
    realName: str | None = Field("", title="真实姓名", description="真实姓名")
    sourceApp: str | None = Field("", title="来源应用", description="来源应用")
    updatedTime: str | None = Field("", title="更新时间", description="更新时间")
    userCode: str | None = Field("", title="用户编码", description="用户编码")
    userId: str | None = Field("", title="用户ID", description="用户ID")
    userStatus: str | None = Field("", title="用户状态", description="用户状态")
    user_account_status: str | None = Field("", title="", description="")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["currentUnit", "departmentId", "userId", ]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        if data.get("userCode") is None and 'idCardNumber' in data:
            data["userCode"] = data["idCardNumber"]
        data["phoneNumber"] = data["name"] if data.get("name") else ""
        return data


class TeachersSchool(BaseModel):
    """这个模型的作用是在老师关键信息变更审批时，除了把老师更新信息送到工作流（不是在本地查），还需要将当时的状态和就职单位所处地区名字送上工作流"""
    teacher_main_status: str = Field("", title="主状态", description="主状态")
    teacher_sub_status: str = Field("", title="子状态", description="子状态")
    school_name: str = Field("", title="学校名称", description="学校名称")
    borough: str = Field("", title="行政管辖区", description="行政管辖区")


class TeachersCreatModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: Optional[int | str] = Field(None, title="任职单位", description="单位部门", )
    teacher_avatar: str = Field("", title="头像", description="头像")
    mobile: str = Field("", title="手机号", description="手机号")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeachersUpdateModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_id: int | str = Field(None, title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: Optional[int | str] = Field(None, title="任职单位", description="单位部门", )
    teacher_avatar: str = Field("", title="头像", description="头像")
    mobile: str = Field("", title="手机号", description="手机号")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeachersSaveImportRegisterCreatModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: str = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: int = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: str = Field(..., title="任职单位", description="单位部门", )
    mobile: int = Field("", title="手机号", description="手机号")


class TeachersSaveImportRegisterCreatTestModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: str = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="证件类型", description="证件类型")
    teacher_id_number: int | str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: str = Field(..., title="单位", description="单位部门", )
    mobile: int = Field("", title="手机号", description="手机号")
    identity: str = Field("", title="身份", description="身份")
    identity_type: str = Field("", title="身份类型", description="身份类型")


class TeachersSaveImportRegisterCreatTestTestModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: str = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: int | str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: str = Field(..., title="所在单位", description="单位部门", )
    mobile: int = Field("", title="手机号码", description="手机号")
    org_id: str | int = Field("", title="所在部门", description="组织ID")
    identity_type: str = Field("", title="身份类型", description="身份类型")
    identity: str = Field("", title="身份", description="身份")


class TeacherImportSaveResulRestModel(TeachersSaveImportRegisterCreatTestTestModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeachersSaveImportCreatTestModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: IdentityType = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int = Field(..., title="任职单位", description="单位部门", )
    mobile: str = Field("", title="手机号", description="手机号")
    org_id: str | int = Field("", title="组织ID", description="组织ID")

    # identity_type: str = Field("", title="身份类型", description="身份类型")
    # identity: str = Field("", title="身份", description="身份")

    @model_validator(mode='before')
    @classmethod
    def check_id_type(self, data: dict):
        data["teacher_id_type"] = IdentityType.from_chinese(data["teacher_id_type"])
        data["teacher_gender"] = Gender.from_chinese(data["teacher_gender"])
        _change_list = ["teacher_id_number", "mobile"]
        for _change in _change_list:
            if _change in data:
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeachersSaveImportCreatModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    单位部门：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: IdentityType = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int = Field(..., title="任职单位", description="单位部门", )
    mobile: str = Field("", title="手机号", description="手机号")

    @model_validator(mode='before')
    @classmethod
    def check_id_type(self, data: dict):
        data["teacher_id_type"] = IdentityType.from_chinese(data["teacher_id_type"])
        data["teacher_gender"] = Gender.from_chinese(data["teacher_gender"])
        _change_list = ["teacher_id_number", "mobile"]
        for _change in _change_list:
            if _change in data:
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherImportSaveResultModel(TeachersSaveImportCreatModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherRe(BaseModel):
    """
    这个模型先在本地查然后是交给工作流的,相当于表单附赠信息
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_avatar: str = Field("", title="头像", description="头像")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int | str = Field(0, title="任职单位", description="单位部门", )
    mobile: str = Field("", title="手机号", description="手机号")
    teacher_main_status: str = Field("", title="主状态", description="主状态")
    teacher_sub_status: str = Field("", title="子状态", description="子状态")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherAdd(BaseModel):
    """
    这个是借动和调动时,从系统外进系统内时,建立新老师的时候用的
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int | str = Field(0, title="任职单位", description="单位部门", )
    mobile: str = Field("", title="手机号", description="手机号")
    teacher_main_status: str = Field("employed", title="主状态", description="主状态")
    teacher_sub_status: str = Field("active", title="子状态", description="子状态")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherInfoCreateModel(BaseModel):  # 基本信息
    """
    姓名：name
    教师ID：teacher_id
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """

    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书"
                                                    )
    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field("", title="所在部门", description="部门", example="部门")
    org_id: Optional[int | str] = Field(None, title="组织ID", description="组织ID")

    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherInfoCreateResultModel(TeacherInfoCreateModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class CombinedModel(BaseModel):
    """
    这个模型是导入老师，注册excel时用的。
    """
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: str = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field(..., title="身份证件类型", description="证件类型")
    teacher_id_number: int = Field(..., title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: str | int = Field(..., title="任职单位", description="单位部门", )
    mobile: int = Field(..., title="手机号", description="手机号")

    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str | None = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str | None = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str | None = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str | None = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str | None = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str | None = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str | None = Field("", title="获得最高学历的院校或机构",
                                                         description="获得最高学历的院校或者机构",
                                                         example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: str = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str | None = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str | None = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str | None = Field("", title="现任专业技术职务", description="现妆业技术职务",
                                                   example="教师")
    full_time_special_education_major_graduate: str = Field(..., title="是否全日制特殊教育专业毕业",
                                                            description="是否全日制特殊教育专业毕业", )
    received_preschool_education_training: str = Field(..., title="是否受过学前教育培训",
                                                       description="是否受过学前教育培训")
    full_time_normal_major_graduate: str = Field(..., title="是否全日制师范类专业毕业",
                                                 description="是否全日制师范类专业毕业")
    received_special_education_training: str = Field(..., title="是否受过特教专业培养培训",
                                                     description="是否受过特教专业培训")
    has_special_education_certificate: str = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书")

    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: str = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")

    participated_in_basic_service_project: str = Field(..., title="是否参加基层服务项目",
                                                       description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: str = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: str = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: str = Field(..., title="是否具备职业技能等级证书",
                                                          description="是否具备职业技能等级证书", )
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: str = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: str = Field(..., title="是否心理健康教育教师",
                                                        description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str | None = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field(..., title="所在部门", description="部门", example="部门")
    org_id: str = Field(..., title="组织ID", description="组织ID")

    hmotf: str | None = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str | None = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str | None = Field("", title="主要任课学段", description="主要任课学段",
                                            example="主要任课学段")
    teacher_qualification_cert_num: str | None = Field("", title="教师资格证号码", description="教师资格证编号",
                                                       example="教师资格证编号")
    teaching_discipline: str | None = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str | None = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str | None = Field("", title="掌握程度", description="语言掌握程度",
                                                   example="语言掌握程度")
    language_certificate_name: str | None = Field("", title="语言证书名称", description="语言证书名称",
                                                  example="语言证书名称")
    contact_address: str | None = Field("", title="通讯地址省市县", description="通讯地址省市县",
                                        example="通讯地址省市县")
    contact_address_details: str | None = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                                example="通讯地址详细信息")
    email: str | None = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str | None = Field("", title="最高学历层次", description="最高学历层次",
                                                example="最高学历层次")
    highest_degree_name: str | None = Field("", title="最高学位名称", description="最高学位名称",
                                            example="最高学位名称")
    is_major_graduate: str | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str | None = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_org_id(self, data: dict):
        if "ori_id" not in data:
            if "department" in data:
                data["org_id"] = data["department"]
        if isinstance(data["teacher_number"], int):
            data["teacher_number"] = str(data["teacher_number"])
        return data


class TeacherImportResultModel(CombinedModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherFileStorageModel(FileStorageModel):
    pass


class TeacherInfo(BaseModel):  # 基本信息
    """
    姓名：name
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(-1, title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date | None = Field(..., title="特教开始时间", description="特教开始时间",
                                                      example="2021-10-10")
    start_working_date: date | None = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date | None = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书"
                                                    )
    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field("", title="所在部门", description="部门", example="部门")
    org_id: Optional[int | str] = Field(None, title="组织ID", description="组织ID")

    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_base_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data

    @model_validator(mode='after')
    def check_special_ethnicity_teacher(self):
        if self.nationality == "CN":
            if self.ethnicity is None:
                raise EthnicityNoneError()
            if self.political_status is None:
                raise PoliticalStatusNoneError()
        return self


# class TeacherInfoSaveModel(BaseModel):  # 基本信息
#     """
#     姓名：name
#     教师ID：teacher_id
#     国家地区：nationality
#     民族：ethnicity
#     政治面貌：political_status
#     籍贯：native_place
#     出生地：birth_place
#     曾用名：former_name
#     婚姻状况：marital_status
#     健康状况：health_condition
#     最高学历：highest_education
#     获得最高学历的院校或者机构：institution_of_highest_education
#     特教开时时间：special_education_start_time
#     参加工作年月：start_working_date
#     进本校时间：enter_school_time
#     教职工来源：source_of_staff
#     教职工类别：staff_category
#     是否在编：in_post
#     用人形式：employment_form
#     合同签订情况：contract_signing_status
#     现任岗位类型：current_post_type
#     现岗位等级：current_post_level
#     现妆业技术职务：current_technical_position
#     是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
#     是否受过学前教育培训：received_preschool_education_training
#     是否全日制师范类专业毕业：full_time_normal_major_graduate
#     是否受过特教专业培训：received_special_education_training
#     是否有特教证书：has_special_education_certificate
#     信息技术应用能力：information_technology_application_ability
#     是否免费师范生：free_normal_college_student
#     是否参加基层服务项目：participated_in_basic_service_project
#     基层服务起始日期：basic_service_start_date
#     基层服务结束日期：basic_service_end_date
#     是否特教：special_education_teacher
#     是否双师型：dual_teacher
#     是否具备职业技能等级证书：has_occupational_skill_level_certificate
#     企业工作时长：enterprise_work_experience
#     是否县级以上骨干：county_level_backbone
#     是否心理健康教育教师：psychological_health_education_teacher
#     招聘方式：recruitment_method
#     教职工号：teacher_number
#     """
#     teacher_base_id: Optional[int] = Field(..., title="教师ID", description="教师ID")
#     teacher_id: int = Field(..., title="教师ID", description="教师ID")
#     ethnicity: str = Field("", title="民族", description="民族", example="汉族")
#     nationality: str = Field("", title="国家/地区", description="国家地区", example="中国")
#     political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
#     native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
#     birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
#     former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
#     marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
#     health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
#     highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
#     institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
#                                                   description="获得最高学历的院校或者机构", example="沈阳师范大学")
#     special_education_start_time: Optional[date] = Field(None, title="特教开始时间",
#                                                          description="特教开始时间",
#                                                          example="2021-10-10")
#     start_working_date: Optional[date] = Field(None, title="参加工作年月", description="参加工作年月",
#                                                example="2010-01-01")
#     enter_school_time: Optional[date] = Field(None, title="进本校年月", description="进本校时间",
#                                               example="2010-01-01")
#     source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
#     staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
#     in_post: Optional[YesOrNo] = Field(None, title="是否在编", description="是否在编")
#     employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
#     contract_signing_status: str = Field("", title="签订合同情况", description="合同签订情况", example="已签")
#     current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
#     current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
#     current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
#     full_time_special_education_major_graduate: Optional[YesOrNo] = Field(None, title="是否全日制特殊教育专业毕业",
#                                                                           description="是否全日制特殊教育专业毕业")
#     received_preschool_education_training: Optional[YesOrNo] = Field(None, title="是否受过学前教育培训",
#                                                                      description="是否受过学前教育培训")
#     full_time_normal_major_graduate: Optional[YesOrNo] = Field(None, title="是否全日制师范类专业毕业",
#                                                                description="是否全日制师范类专业毕业")
#     received_special_education_training: Optional[YesOrNo] = Field(None, title="是否受过特教专业培养培训",
#                                                                    description="是否受过特教专业培训")
#     has_special_education_certificate: Optional[YesOrNo] = Field(None, title="是否有特殊教育从业证书",
#                                                                  description="是否有特教证书",
#                                                                  example="yes")
#     information_technology_application_ability: str = Field("", title="信息技术应用能力",
#                                                             description="信息技术应用能力", example="优秀")
#
#     free_normal_college_student: Optional[YesOrNo] = Field(None, title="是否属于免费（公费）师范生", description="是否免费师范生")
#     participated_in_basic_service_project: Optional[YesOrNo] = Field(None, title="是否参加基层服务项目",
#                                                                      description="是否参加基层服务项目")
#     basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
#                                                      description="基层服务起始日期",
#                                                      example="2010-01-01")
#     basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
#                                                    description="基层服务结束日期",
#                                                    example="2010-01-01")
#     special_education_teacher: Optional[YesOrNo] = Field(None, title="是否特级教师", description="是否特教")
#     dual_teacher: Optional[YesOrNo] = Field(None, title="是否双师型", description="是否双师型")
#     has_occupational_skill_level_certificate: Optional[YesOrNo] = Field(None, title="是否具备职业技能等级证书",
#                                                                         description="是否具备职业技能等级证书")
#     enterprise_work_experience: str = Field("", title="企业工作（实践）时长", description="企业工作时长", example="3年")
#     county_level_backbone: Optional[YesOrNo] = Field(None, title="是否县级及以上骨干教师", description="是否县级以上骨干")
#     psychological_health_education_teacher: Optional[YesOrNo] = Field(None, title="是否心理健康教育教师",
#                                                                       description="是否心理健康教育教师")
#     recruitment_method: str = Field("", title="招聘方式", description="招聘方式", example="招聘")
#     teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")


class TeacherInfoSaveModel(BaseModel):  # 基本信息
    """
    姓名：name
    教师ID：teacher_id
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(-1, title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: str = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field("", title="国家/地区", description="国家地区", example="中国")
    political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: Optional[date] = Field(None, title="特教开始时间",
                                                         description="特教开始时间",
                                                         example="2021-10-10")
    start_working_date: Optional[date] = Field(None, title="参加工作年月", description="参加工作年月",
                                               example="2010-01-01")
    enter_school_time: Optional[date] = Field(None, title="进本校年月", description="进本校时间",
                                              example="2010-01-01")
    source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: Optional[bool] = Field(None, title="是否在编", description="是否在编")
    employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field("", title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(False, title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(False, title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(False, title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(False, title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    information_technology_application_ability: str = Field("", title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    has_special_education_certificate: bool = Field(False, title="是否有特殊教育从业证书",
                                                    description="是否有特教证书",
                                                    example="yes")
    free_normal_college_student: bool = Field(False, title="是否属于免费（公费）师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(False, title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(False, title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(False, title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field("", title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(False, title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(False, title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field("", title="所在部门", description="部门", example="部门")
    org_id: Optional[int | str] = Field(None, title="组织ID", description="组织ID")

    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_base_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class NewTeacherInfoSaveModel(BaseModel):  # 基本信息
    """
    保存再查看的模型,有些是不需要经过验证
    姓名：name
    教师ID：teacher_id
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: str = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field("", title="国家/地区", description="国家地区", example="中国")
    political_status: str | None = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str | None = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str | None = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str | None = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str | None = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str | None = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str | None = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str | None = Field("", title="获得最高学历的院校或机构",
                                                         description="获得最高学历的院校或者机构",
                                                         example="沈阳师范大学")
    special_education_start_time: Optional[date] | None = Field(default=None, title="特教开始时间",
                                                                description="特教开始时间",
                                                                example="2021-10-10")
    start_working_date: Optional[date] | None = Field(default=None, title="参加工作年月", description="参加工作年月",
                                                      example="2010-01-01")
    enter_school_time: Optional[date] | None = Field(default=None, title="进本校年月", description="进本校时间",
                                                     example="2010-01-01")
    source_of_staff: str | None = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str | None = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: bool | None = Field(False, title="是否在编", description="是否在编")
    employment_form: str | None = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str | None = Field("", title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str | None = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str | None = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str | None = Field("", title="现任专业技术职务", description="现妆业技术职务",
                                                   example="教师")
    full_time_special_education_major_graduate: bool | None = Field(False, title="是否全日制特殊教育专业毕业",
                                                                    description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool | None = Field(False, title="是否受过学前教育培训",
                                                               description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool | None = Field(False, title="是否全日制师范类专业毕业",
                                                         description="是否全日制师范类专业毕业")
    received_special_education_training: bool | None = Field(False, title="是否受过特教专业培养培训",
                                                             description="是否受过特教专业培训")
    has_special_education_certificate: bool | None = Field(False, title="是否有特殊教育从业证书",
                                                           description="是否有特教证书")
    information_technology_application_ability: str | None = Field("", title="信息技术应用能力",
                                                                   description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool | None = Field(False, title="是否属于免费（公费）师范生",
                                                     description="是否免费师范生")
    participated_in_basic_service_project: bool | None = Field(False, title="是否参加基层服务项目",
                                                               description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] | None = Field(default=None, title="参加基层服务项目起始年月",
                                                            description="基层服务起始日期",
                                                            example="2010-01-01")
    basic_service_end_date: Optional[date] | None = Field(default=None, title="参加基层服务项目结束年月",
                                                          description="基层服务结束日期",
                                                          example="2010-01-01")
    special_education_teacher: bool | None = Field(False, title="是否特级教师", description="是否特教")
    dual_teacher: bool | None = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool | None = Field(False, title="是否具备职业技能等级证书",
                                                                  description="是否具备职业技能等级证书")
    enterprise_work_experience: str | None = Field("", title="企业工作（实践）时长", description="企业工作时长",
                                                   example="3年")
    county_level_backbone: bool | None = Field(False, title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool | None = Field(False, title="是否心理健康教育教师",
                                                                description="是否心理健康教育教师")
    recruitment_method: str | None = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str | None = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str | None = Field("", title="所在部门", description="部门", example="部门")
    org_id: Optional[int | str] | None = Field(None, title="组织ID", description="组织ID")

    hmotf: str | None = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str | None = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str | None = Field("", title="主要任课学段", description="主要任课学段",
                                            example="主要任课学段")
    teacher_qualification_cert_num: str | None = Field("", title="教师资格证号码", description="教师资格证编号",
                                                       example="教师资格证编号")
    teaching_discipline: str | None = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str | None = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str | None = Field("", title="掌握程度", description="语言掌握程度",
                                                   example="语言掌握程度")
    language_certificate_name: str | None = Field("", title="语言证书名称", description="语言证书名称",
                                                  example="语言证书名称")
    contact_address: str | None = Field("", title="通讯地址省市县", description="通讯地址省市县",
                                        example="通讯地址省市县")
    contact_address_details: str | None = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                                example="通讯地址详细信息")
    email: str | None = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str | None = Field("", title="最高学历层次", description="最高学历层次",
                                                example="最高学历层次")
    highest_degree_name: str | None = Field("", title="最高学位名称", description="最高学位名称",
                                            example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str | None = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_base_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class CurrentTeacherInfoSaveModel(BaseModel):  # 基本信息
    """
    姓名：name
    教师ID：teacher_id
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: str | None = Field("", title="民族", description="民族", example="汉族")
    nationality: str | None = Field("", title="国家/地区", description="国家地区", example="中国")
    political_status: str | None = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str | None = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str | None = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str | None = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str | None = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str | None = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str | None = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str | None = Field("", title="获得最高学历的院校或机构",
                                                         description="获得最高学历的院校或者机构",
                                                         example="沈阳师范大学")
    special_education_start_time: Optional[date] | None = Field(default=None, title="特教开始时间",
                                                                description="特教开始时间",
                                                                example="2021-10-10")
    start_working_date: Optional[date] | None = Field(default=None, title="参加工作年月", description="参加工作年月",
                                                      example="2010-01-01")
    enter_school_time: Optional[date] | None = Field(default=None, title="进本校年月", description="进本校时间",
                                                     example="2010-01-01")
    source_of_staff: str | None = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str | None = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: Optional[bool] | None = Field(None, title="是否在编", description="是否在编")
    employment_form: str | None = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str | None = Field("", title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str | None = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str | None = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str | None = Field("", title="现任专业技术职务", description="现妆业技术职务",
                                                   example="教师")
    full_time_special_education_major_graduate: bool | None = Field(False, title="是否全日制特殊教育专业毕业",
                                                                    description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool | None = Field(False, title="是否受过学前教育培训",
                                                               description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool | None = Field(False, title="是否全日制师范类专业毕业",
                                                         description="是否全日制师范类专业毕业")
    received_special_education_training: bool | None = Field(False, title="是否受过特教专业培养培训",
                                                             description="是否受过特教专业培训")
    has_special_education_certificate: bool | None = Field(False, title="是否有特殊教育从业证书",
                                                           description="是否有特教证书")
    information_technology_application_ability: str | None = Field("", title="信息技术应用能力",
                                                                   description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool | None = Field(False, title="是否属于免费（公费）师范生",
                                                     description="是否免费师范生")
    participated_in_basic_service_project: bool | None = Field(False, title="是否参加基层服务项目",
                                                               description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] | None = Field(default=None, title="参加基层服务项目起始年月",
                                                            description="基层服务起始日期",
                                                            example="2010-01-01")
    basic_service_end_date: Optional[date] | None = Field(default=None, title="参加基层服务项目结束年月",
                                                          description="基层服务结束日期",
                                                          example="2010-01-01")
    special_education_teacher: bool | None = Field(False, title="是否特级教师", description="是否特教")
    dual_teacher: bool | None = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool | None = Field(False, title="是否具备职业技能等级证书",
                                                                  description="是否具备职业技能等级证书")
    enterprise_work_experience: str | None = Field("", title="企业工作（实践）时长", description="企业工作时长",
                                                   example="3年")
    county_level_backbone: bool | None = Field(False, title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool | None = Field(False, title="是否心理健康教育教师",
                                                                description="是否心理健康教育教师")
    recruitment_method: str | None = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str | None = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str | None = Field("", title="所在部门", description="部门", example="部门")
    org_id: Optional[int | str] | None = Field(None, title="组织ID", description="组织ID")

    hmotf: str | None = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str | None = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str | None = Field("", title="主要任课学段", description="主要任课学段",
                                            example="主要任课学段")
    teacher_qualification_cert_num: str | None = Field("", title="教师资格证号码", description="教师资格证编号",
                                                       example="教师资格证编号")
    teaching_discipline: str | None = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str | None = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str | None = Field("", title="掌握程度", description="语言掌握程度",
                                                   example="语言掌握程度")
    language_certificate_name: str | None = Field("", title="语言证书名称", description="语言证书名称",
                                                  example="语言证书名称")
    contact_address: str | None = Field("", title="通讯地址省市县", description="通讯地址省市县",
                                        example="通讯地址省市县")
    contact_address_details: str | None = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                                example="通讯地址详细信息")
    email: str | None = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str | None = Field("", title="最高学历层次", description="最高学历层次",
                                                example="最高学历层次")
    highest_degree_name: str | None = Field("", title="最高学位名称", description="最高学位名称",
                                            example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str | None = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_base_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherInfoSubmit(BaseModel):  # 基本信息
    """
    姓名：name
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(-1, title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业", )
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书")

    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")

    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书", )
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field(..., title="所在部门", description="部门", example="部门")
    org_id: int | str = Field(..., title="组织ID", description="组织ID")

    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_base_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data

    @model_validator(mode='after')
    def check_special_ethnicity_teacher(self):
        if self.nationality == "CN":
            if self.ethnicity is None:
                raise EthnicityNoneError()
            if self.political_status is None:
                raise PoliticalStatusNoneError()
        return self


class TeacherInfoImportSubmit(BaseModel):
    # 基本信息
    """
    这个模型是导入的时候用的，需要验证，因为雪花id所以另起一个模型。
    姓名：name
    国家地区：nationality
    民族：ethnicity
    政治面貌：political_status
    籍贯：native_place
    出生地：birth_place
    曾用名：former_name
    婚姻状况：marital_status
    健康状况：health_condition
    最高学历：highest_education
    获得最高学历的院校或者机构：institution_of_highest_education
    特教开时时间：special_education_start_time
    参加工作年月：start_working_date
    进本校时间：enter_school_time
    教职工来源：source_of_staff
    教职工类别：staff_category
    是否在编：in_post
    用人形式：employment_form
    合同签订情况：contract_signing_status
    现任岗位类型：current_post_type
    现岗位等级：current_post_level
    现妆业技术职务：current_technical_position
    是否全日制特殊教育专业毕业：full_time_special_education_major_graduate
    是否受过学前教育培训：received_preschool_education_training
    是否全日制师范类专业毕业：full_time_normal_major_graduate
    是否受过特教专业培训：received_special_education_training
    是否有特教证书：has_special_education_certificate
    信息技术应用能力：information_technology_application_ability
    是否免费师范生：free_normal_college_student
    是否参加基层服务项目：participated_in_basic_service_project
    基层服务起始日期：basic_service_start_date
    基层服务结束日期：basic_service_end_date
    是否特教：special_education_teacher
    是否双师型：dual_teacher
    是否具备职业技能等级证书：has_occupational_skill_level_certificate
    企业工作时长：enterprise_work_experience
    是否县级以上骨干：county_level_backbone
    是否心理健康教育教师：psychological_health_education_teacher
    招聘方式：recruitment_method
    教职工号：teacher_number
    """
    teacher_base_id: int | str = Field(-1, title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业", )
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书")

    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")

    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书", )
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field(..., title="所在部门", description="部门", example="部门")
    org_id: int | str = Field(..., title="组织ID", description="组织ID")

    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")

    @model_validator(mode='after')
    def check_special_ethnicity_teacher(self):
        if self.nationality == "CN":
            if self.ethnicity is None:
                raise EthnicityNoneError()
            if self.political_status is None:
                raise PoliticalStatusNoneError()
        return self


# 查询新入职员工模型3.1
class NewTeacher(BaseModel):
    # teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_code: Optional[str] = Query("", title="教师编号", description="教师编号", example="123456789012345678")
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名", example="张三")
    teacher_gender: Optional[Gender] = Query("", title="性别", description="性别", example="男")
    nationality: Optional[str] = Query("", title="国家/地区", description="国家地区", example="中国")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    mobile: Optional[str] = Query("", title="手机号", description="手机号")
    political_status: Optional[str] = Query("", title="政治面貌", description="政治面貌", example="群众")
    source_of_staff: Optional[str] = Query("", title="教职工来源", description="教职工来源", example="招聘")
    teacher_id_number: Optional[str] = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="证件类型", example="身份证")
    teacher_main_status: Optional[str] = Query(None, title="主要状态", description="主要状态", example="unemployed")
    teacher_sub_status: Optional[str] = Query(None, title="子状态", description="子状态", example="unemployed")
    highest_education: Optional[str] = Query("", title="最高学历", description="最高学历", example="本科")
    teacher_date_of_birth: Optional[date] = Field(None, title="出生日期", description="出生日期")
    teacher_qualification_cert_num: Optional[str] = Query("", title="教师资格证号码", description="教师资格证编号",
                                                          example="教师资格证编号")
    county_level_backbone: Optional[bool] = Query(None, title="是否县级及以上骨干教师", description="是否县级以上骨干")
    employment_form: Optional[str] = Query("", title="用人形式", description="用人形式", example="合同")
    start_working_date_s: Optional[date] = Query(None, title="参加工作开始年月", description="参加工作开始年月",
                                                 example="2010-01-01")
    start_working_date_e: Optional[date] = Query(None, title="参加工作结束年月", description="参加工作结束年月",
                                                 example="2010-01-01")
    enter_school_time_s: Optional[date] = Query(None, title="进本校开始时间", description="进本校开始时间",
                                                example="2010-01-01")
    enter_school_time_e: Optional[date] = Query(None, title="进本校结束时间", description="进本校结束时间",
                                                example="2010-01-01")
    staff_category: Optional[str] = Query("", title="教职工类别", description="教职工类别", example="教师")
    current_post_type: Optional[str] = Query("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: Optional[str] = Query("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: Optional[str] = Query("", title="现任专业技术职务", description="现妆业技术职务",
                                                      example="教师")

    # @model_validator(mode='before')
    # @classmethod
    # def check_id_before(self, data: dict):
    #     _change_list = ["teacher_employer"]
    #     for _change in _change_list:
    #         if _change in data and isinstance(data[_change], str):
    #             data[_change] = int(data[_change])
    #         elif _change in data and isinstance(data[_change], int):
    #             data[_change] = str(data[_change])
    #         else:
    #             pass
    #     return data


class NewTeacherRe(BaseModel):
    teacher_base_id: Optional[int | str] = Field(0, title="教师ID", description="教师ID")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Field("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Field("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: str = Field("", title="性别", description="性别", example="男")
    teacher_employer: int | str = Field(None, title="任职单位", description="单位部门", example="xx学校")
    highest_education: Optional[str] = Field("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] = Field("", title="政治面貌", description="政治面貌", example="群众")
    employment_form: Optional[str] = Field("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] = Field(None, title="进本校年月", description="进本校时间", example="2010-01-01")
    teacher_main_status: Optional[str] = Field("", title="主要状态", description="主要状态", example="unemployed")
    teacher_sub_status: Optional[str] = Field("", title="次要状态", description="次要状态", example="unemployed")
    in_post: Optional[bool] = Field(None, title="是否在编", description="是否在编", example="yes")
    school_name: str = Field("", title="", description="", example="")
    approval_status: str = Field("submitting", title="审核状态", description="审核状态", example="submitting")
    # process_instance_id: int | str = Field(..., title="流程实例ID", description="流程实例ID",
    #                                        example="123456789012345678")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_base_id", "teacher_id", "process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class NewTeacherApprovalCreate(BaseModel):
    # 老师关键信息
    # teacher_base_id: Optional[int] = Field(None, title="教师ID", description="教师ID")
    # teacher_id: int = Field(..., title="教师ID", description="教师ID")
    # teacher_name: Optional[str] = Field("", title="姓名", description="姓名", example="张三")
    # teacher_id_number: Optional[str] = Field("", title="身份证号", description="身份证号", example="123456789012345678")
    # teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    # teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别", example="男")
    # teacher_employer: Optional[int] = Field(None, title="单位部门", description="单位部门", example="xx学校")
    # highest_education: Optional[str] = Field("", title="最高学历", description="最高学历", example="本科")
    # political_status: Optional[str] = Field("", title="政治面貌", description="政治面貌", example="群众")
    # in_post: Optional[bool] = Field(None, title="是否在编", description="是否在编", example="yes")
    # school_name: Optional[str] = Field("", title="", description="", example="")
    # employment_form: Optional[str] = Field("", title="用人形式", description="用人形式", example="合同")
    # enter_school_time: Optional[date] = Field(None, title="进本校年月", description="进本校时间", example="2010-01-01")
    # teacher_main_status: Optional[str] = Field(None, title="主要状态", description="主要状态", example="unemployed")
    # teacher_sub_status: Optional[str] = Field(None, title="次要状态", description="次要状态", example="unsubmitted")
    # is_approval: Optional[bool] = Field(None, title="是否在审批中", description="是否在审批中")
    # teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号", example="123456789012345678")

    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int = Field(0, title="任职单位", description="单位部门", gt=0)
    teacher_avatar: str = Field("", title="头像", description="头像")
    mobile: str = Field("", title="手机号", description="手机号")
    identity: str = Field("", title="身份", description="身份")
    identity_type: str = Field("", title="身份类型", description="身份类型")
    teacher_main_status: Optional[str] = Field("", title="主要状态", description="主要状态", example="unemployed")
    teacher_sub_status: Optional[str] = Field("", title="次要状态", description="次要状态", example="unemployed")
    school_name: str = Field("", title="", description="", example="")

    # 教师基本信息
    teacher_base_id: Optional[int] = Field(None, title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家/地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校年月", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="签订合同情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现任岗位类型", description="现任岗位类型", example="教师")
    current_post_level: str = Field("", title="现任岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现任专业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业", )
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培养培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特殊教育从业证书", description="是否有特教证书")

    free_normal_college_student: bool = Field(..., title="是否属于免费（公费）师范生", description="是否免费师范生")

    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="参加基层服务项目起始年月",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="参加基层服务项目结束年月",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特级教师", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书", )
    enterprise_work_experience: str = Field(..., title="企业工作（实践）时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级及以上骨干教师", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")
    department: str = Field(..., title="所在部门", description="部门", example="部门")
    org_id: int | str = Field(..., title="组织ID", description="组织ID")
    hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口性质", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证号码", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool | None = Field(False, title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")
    borough: str = Field("", title="行政管辖区", description="行政管辖区", example="行政管辖区")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_base_id", "teacher_id", "org_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class CurrentTeacherQuery(BaseModel):
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    单位部门：employer
    # 最高学历：highest_education
    政治面貌：political_status
    是否在编：in_post
    用人形式：employment_form
    进本校时间：enter_school_time
    审核状态：approval_status
    """
    # teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: Optional[Gender] = Query("", title="性别", description="性别", example="男")
    teacher_employer: Optional[int | str] = Query(None, title="任职单位", description="单位部门", example="xx学校")
    highest_education: str = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: str = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    employment_form: str = Query("", title="用人形式", description="用人形式", example="合同")
    enter_school_time_s: Optional[date] = Query(None, title="进本校开始时间", description="进本校开始时间",
                                                example="2010-01-01")
    enter_school_time_e: Optional[date] = Query(None, title="进本校结束时间", description="进本校结束时间",
                                                example="2010-01-01")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class CurrentTeacherQueryRe(BaseModel):
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    单位部门：employer
    # 最高学历：highest_education
    政治面貌：political_status
    是否在编：in_post
    用人形式：employment_form
    进本校时间：enter_school_time
    审核状态：approval_status
    """
    teacher_base_id: Optional[int | str] | None = Field(None, title="教师基本信息id", description="教师ID")
    teacher_id: int | str | None = Field(..., title="教师ID", description="教师ID")
    teacher_name: str | None = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str | None = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: str | None = Query("", title="性别", description="性别", example="男")
    teacher_employer: int | str | None = Query(1, title="任职单位", description="单位部门", example="xx学校")
    highest_education: Optional[str] | None = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] | None = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] | None = Query(None, title="是否在编", description="是否在编", example="yes")
    employment_form: Optional[str] | None = Query("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] | None = Query(None, title="进本校年月", description="进本校时间",
                                                     example="2010-01-01")
    school_name: Optional[str] | None = Query("", title="", description="", example="")
    is_approval: Optional[bool] | None = Field(None, title="是否在审批中", description="是否在审批中")
    teacher_main_status: Optional[str] | None = Field("", title="主要状态", description="主要状态",
                                                      example="unemployed")
    teacher_sub_status: Optional[str] | None = Field("", title="次要状态", description="次要状态", example="unemployed")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_base_id", "teacher_id"]
        # if data.get("teacher_id_number"):
        #     if len(data["teacher_id_number"]) == 18:
        #         data["teacher_id_number"] = data["teacher_id_number"][0:6] + "********" + data["teacher_id_number"][
        #                                                                                   -4:]
        #     # 其他类型的证件号码值只对最后四位脱敏
        #     elif len(data["teacher_id_number"]) > 0:
        #         data["teacher_id_number"] = data["teacher_id_number"][0:-4] + "****"
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass

        return data


class TeacherApprovalQuery(BaseModel):
    """
    新教职工审核查询模型
    教师姓名：teacher_name
    所属机构：teacher_employer
    教师性别：teacher_gender
    申请人：applicant_name
    审核人：approval_name
    身份证号：teacher_id_number
    """
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名", example="张三")
    teacher_employer: Optional[int | str] = Query(None, title="任职单位", description="单位部门", example="xx学校")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别", example="男")
    applicant_name: Optional[str] = Query("", title="申请人", description="申请人", example="张三")
    approval_name: Optional[str] = Query("", title="审核人", description="审核人", example="张三")
    teacher_id_number: Optional[str] = Query("", title="身份证号", description="身份证号", example="123456789012345678")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class TeacherApprovalQueryRe(BaseModel):
    """
    新教职工入职审批模块查看的四个模型
    教师姓名：teacher_name
    所属学校名称：school_name
    教师性别：teacher_gender
    身份证号：teacher_id_number
    用人形式：employment_form
    教师id：teacher_id
    申请人：applicant_name
    审批人：approval_name
    申请时间：apply_time
    """
    teacher_name: str = Field("", title="姓名", description="姓名", example="张三")
    teacher_gender: Gender = Field("male", title="性别", description="性别", example="男")
    school_name: Optional[str] = Query("", title="单位部门名称", description="单位部门名称", example="xx小学")
    teacher_id_number: Optional[str] = Field("", title="身份证号", description="身份证号", example="123456789012345678")
    employment_form: Optional[str] = Field("", title="用人形式", description="用人形式", example="合同")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    applicant_name: Optional[str] = Field("", title="申请人", description="申请人", example="张三")
    approval_name: Optional[str] = Field("", title="审核人", description="审核人", example="张三")
    start_time: Optional[datetime] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")
    approval_status: str = Field("pending", title="审批状态", description="审批状态")
    process_instance_id: int | str = Field(0, title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_id", "process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


# task相关模型
class NewTeacherTask(BaseModel):
    """{'file_name':filename,'bucket':bucket,'scene':scene},"""
    file_name: str = Field('', title="", description="", examples=[' '])
    bucket: str = Field('', title="", description="", examples=[' '])
    scene: str = Field("teacher_import", title="场景", description="", examples=[' '])


class TeacherChangeLogQueryModel(BaseModel):
    """
    id:
    change
    """
    id: Optional[int] = Query(None, title="id", description="id", example=1)
    teacher_id: int | str = Query(..., title="teacher_id", description="teacher_id", example=1)
    change_module: Optional[ChangeModule] = Query(None, description=" 变更模块", examples=[''])
