from datetime import date

from pydantic import BaseModel, Field, model_validator, ValidationError, field_validator
from fastapi import Query
from typing import Optional
from models.teachers import TeacherApprovalAtatus
from models.public_enum import  Gender
from business_exceptions.teacher import EthnicityNoneError, PoliticalStatusNoneError


class Teachers(BaseModel):
    """
    教师ID:teacher_id
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    任职单位：teacher_employer
    头像：teacher_avatar
    """
    teacher_id: int = Field(None, title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="教师名称", description="教师名称")
    teacher_gender: Gender = Field(..., title="教师性别", description="教师性别")
    teacher_id_type: str = Field("", title="证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int = Field(0, title="任职单位", description="任职单位")
    teacher_avatar: str = Field("", title="头像", description="头像")


class TeachersCreatModel(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    任职单位：teacher_employer
    头像：teacher_avatar
    """
    teacher_name: str = Field(..., title="教师名称", description="教师名称")
    teacher_gender: Gender = Field(..., title="教师性别", description="教师性别")
    teacher_id_type: str = Field("", title="证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int = Field(0, title="任职单位", description="任职单位", gt=0)
    teacher_avatar: str = Field("", title="头像", description="头像")


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
    现在岗位类型：current_post_type
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

    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: str = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家地区", description="国家地区", example="中国")
    political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field('', title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field('', title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field('', title="进本校时间", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field('', title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field('', title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(False, title="是否在编", description="是否在编")
    employment_form: str = Field('', title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field('', title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(False, title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(False, title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(False, title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(False, title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(False, title="是否有特教证书", description="是否有特教证书",
                                                    example="yes")
    information_technology_application_ability: str = Field('', title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(False, title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(False, title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(False, title="是否特教", description="是否特教")
    dual_teacher: bool = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(False, title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field('', title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(False, title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(False, title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field('', title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")

    # @model_validator(mode="after")
    # def check_special_ethnicity_teacher(self):
    #     if self.nationality == "CN":
    #         if self.ethnicity is None:
    #             raise ValueError("民族不能为空")
    #         if self.political_status is None:
    #             raise ValueError("政治面貌不能为空")


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
    现在岗位类型：current_post_type
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
    teacher_base_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家地区", description="国家地区", example="中国")
    political_status: Optional[str] = Field(None, title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校时间", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特教证书", description="是否有特教证书"
                                                    )
    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特教", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field(..., title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")

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
#     现在岗位类型：current_post_type
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
#     nationality: str = Field("", title="国家地区", description="国家地区", example="中国")
#     political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
#     native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
#     birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
#     former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
#     marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
#     health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
#     highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
#     institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
#                                                   description="获得最高学历的院校或者机构", example="沈阳师范大学")
#     special_education_start_time: Optional[date] = Field(None, title="特教开始时间",
#                                                          description="特教开始时间",
#                                                          example="2021-10-10")
#     start_working_date: Optional[date] = Field(None, title="参加工作年月", description="参加工作年月",
#                                                example="2010-01-01")
#     enter_school_time: Optional[date] = Field(None, title="进本校时间", description="进本校时间",
#                                               example="2010-01-01")
#     source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
#     staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
#     in_post: Optional[YesOrNo] = Field(None, title="是否在编", description="是否在编")
#     employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
#     contract_signing_status: str = Field("", title="合同签订情况", description="合同签订情况", example="已签")
#     current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
#     current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
#     current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
#     full_time_special_education_major_graduate: Optional[YesOrNo] = Field(None, title="是否全日制特殊教育专业毕业",
#                                                                           description="是否全日制特殊教育专业毕业")
#     received_preschool_education_training: Optional[YesOrNo] = Field(None, title="是否受过学前教育培训",
#                                                                      description="是否受过学前教育培训")
#     full_time_normal_major_graduate: Optional[YesOrNo] = Field(None, title="是否全日制师范类专业毕业",
#                                                                description="是否全日制师范类专业毕业")
#     received_special_education_training: Optional[YesOrNo] = Field(None, title="是否受过特教专业培训",
#                                                                    description="是否受过特教专业培训")
#     has_special_education_certificate: Optional[YesOrNo] = Field(None, title="是否有特教证书",
#                                                                  description="是否有特教证书",
#                                                                  example="yes")
#     information_technology_application_ability: str = Field("", title="信息技术应用能力",
#                                                             description="信息技术应用能力", example="优秀")
#
#     free_normal_college_student: Optional[YesOrNo] = Field(None, title="是否免费师范生", description="是否免费师范生")
#     participated_in_basic_service_project: Optional[YesOrNo] = Field(None, title="是否参加基层服务项目",
#                                                                      description="是否参加基层服务项目")
#     basic_service_start_date: Optional[date] = Field(None, title="基层服务起始日期",
#                                                      description="基层服务起始日期",
#                                                      example="2010-01-01")
#     basic_service_end_date: Optional[date] = Field(None, title="基层服务结束日期",
#                                                    description="基层服务结束日期",
#                                                    example="2010-01-01")
#     special_education_teacher: Optional[YesOrNo] = Field(None, title="是否特教", description="是否特教")
#     dual_teacher: Optional[YesOrNo] = Field(None, title="是否双师型", description="是否双师型")
#     has_occupational_skill_level_certificate: Optional[YesOrNo] = Field(None, title="是否具备职业技能等级证书",
#                                                                         description="是否具备职业技能等级证书")
#     enterprise_work_experience: str = Field("", title="企业工作时长", description="企业工作时长", example="3年")
#     county_level_backbone: Optional[YesOrNo] = Field(None, title="是否县级以上骨干", description="是否县级以上骨干")
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
    现在岗位类型：current_post_type
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
    teacher_base_id: int = Field(-1, title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: str = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field("", title="国家地区", description="国家地区", example="中国")
    political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: Optional[date] = Field(None, title="特教开始时间",
                                                         description="特教开始时间",
                                                         example="2021-10-10")
    start_working_date: Optional[date] = Field(None, title="参加工作年月", description="参加工作年月",
                                               example="2010-01-01")
    enter_school_time: Optional[date] = Field(None, title="进本校时间", description="进本校时间",
                                              example="2010-01-01")
    source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: Optional[bool] = Field(None, title="是否在编", description="是否在编")
    employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field("", title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(False, title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(False, title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(False, title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(False, title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(False, title="是否有特教证书",
                                                    description="是否有特教证书",
                                                    example="yes")
    information_technology_application_ability: str = Field("", title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(False, title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(False, title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(False, title="是否特教", description="是否特教")
    dual_teacher: bool = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(False, title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field("", title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(False, title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(False, title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")


class NewTeacherInfoSaveModel(BaseModel):  # 基本信息
    """
    保存再查看的模型，有些是不需要经过验证
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
    现在岗位类型：current_post_type
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
    teacher_base_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: str = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field("", title="国家地区", description="国家地区", example="中国")
    political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: Optional[date] = Field(default=None, title="特教开始时间", description="特教开始时间",
                                                         example="2021-10-10")
    start_working_date: Optional[date] = Field(default=None, title="参加工作年月", description="参加工作年月",
                                               example="2010-01-01")
    enter_school_time: Optional[date] = Field(default=None, title="进本校时间", description="进本校时间",
                                              example="2010-01-01")
    source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(False, title="是否在编", description="是否在编")
    employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field("", title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(False, title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(False, title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(False, title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(False, title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(False, title="是否有特教证书", description="是否有特教证书")
    information_technology_application_ability: str = Field("", title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(False, title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(False, title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(default=None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(default=None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(False, title="是否特教", description="是否特教")
    dual_teacher: bool = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(False, title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field("", title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(False, title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(False, title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")


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
    现在岗位类型：current_post_type
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
    teacher_base_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: str | None = Field("", title="民族", description="民族", example="汉族")
    nationality: str = Field("", title="国家地区", description="国家地区", example="中国")
    political_status: str = Field("", title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: Optional[date] = Field(default=None, title="特教开始时间", description="特教开始时间",
                                                         example="2021-10-10")
    start_working_date: Optional[date] = Field(default=None, title="参加工作年月", description="参加工作年月",
                                               example="2010-01-01")
    enter_school_time: Optional[date] = Field(default=None, title="进本校时间", description="进本校时间",
                                              example="2010-01-01")
    source_of_staff: str = Field("", title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field("", title="教职工类别", description="教职工类别", example="教师")
    in_post: Optional[bool] = Field(None, title="是否在编", description="是否在编")
    employment_form: str = Field("", title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field("", title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(False, title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业")
    received_preschool_education_training: bool = Field(False, title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(False, title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(False, title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(False, title="是否有特教证书",
                                                    description="是否有特教证书")
    information_technology_application_ability: str = Field("", title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(False, title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(False, title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(default=None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(default=None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(False, title="是否特教", description="是否特教")
    dual_teacher: bool = Field(False, title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(False, title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书")
    enterprise_work_experience: str = Field("", title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(False, title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(False, title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field("", title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")


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
    现在岗位类型：current_post_type
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
    teacher_base_id: int = Field(0, title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethnicity: Optional[str] = Field(None, title="民族", description="民族", example="汉族")
    nationality: str = Field(..., title="国家地区", description="国家地区", example="中国")
    political_status:Optional[str] = Field(None,  title="政治面貌", description="政治面貌", example="党员")
    native_place: str = Field("", title="籍贯", description="籍贯", example="沈阳")
    birth_place: str = Field("", title="出生地", description="出生地", example="沈阳")
    former_name: str = Field("", title="曾用名", description="曾用名", example="张三")
    marital_status: str = Field("", title="婚姻状况", description="婚姻状况", example="已婚")
    health_condition: str = Field("", title="健康状况", description="健康状况", example="良好")
    highest_education: str = Field("", title="最高学历", description="最高学历", example="本科")
    institution_of_highest_education: str = Field("", title="获得最高学历的院校或者机构",
                                                  description="获得最高学历的院校或者机构", example="沈阳师范大学")
    special_education_start_time: date = Field(..., title="特教开始时间", description="特教开始时间",
                                               example="2021-10-10")
    start_working_date: date = Field(..., title="参加工作年月", description="参加工作年月", example="2010-01-01")
    enter_school_time: date = Field(..., title="进本校时间", description="进本校时间", example="2010-01-01")
    source_of_staff: str = Field(..., title="教职工来源", description="教职工来源", example="招聘")
    staff_category: str = Field(..., title="教职工类别", description="教职工类别", example="教师")
    in_post: bool = Field(..., title="是否在编", description="是否在编")
    employment_form: str = Field(..., title="用人形式", description="用人形式", example="合同")
    contract_signing_status: str = Field(..., title="合同签订情况", description="合同签订情况", example="已签")
    current_post_type: str = Field("", title="现在岗位类型", description="现在岗位类型", example="教师")
    current_post_level: str = Field("", title="现岗位等级", description="现岗位等级", example="一级")
    current_technical_position: str = Field("", title="现妆业技术职务", description="现妆业技术职务", example="教师")
    full_time_special_education_major_graduate: bool = Field(..., title="是否全日制特殊教育专业毕业",
                                                             description="是否全日制特殊教育专业毕业", )
    received_preschool_education_training: bool = Field(..., title="是否受过学前教育培训",
                                                        description="是否受过学前教育培训")
    full_time_normal_major_graduate: bool = Field(..., title="是否全日制师范类专业毕业",
                                                  description="是否全日制师范类专业毕业")
    received_special_education_training: bool = Field(..., title="是否受过特教专业培训",
                                                      description="是否受过特教专业培训")
    has_special_education_certificate: bool = Field(..., title="是否有特教证书", description="是否有特教证书")

    information_technology_application_ability: str = Field(..., title="信息技术应用能力",
                                                            description="信息技术应用能力", example="优秀")

    free_normal_college_student: bool = Field(..., title="是否免费师范生", description="是否免费师范生")
    participated_in_basic_service_project: bool = Field(..., title="是否参加基层服务项目",
                                                        description="是否参加基层服务项目")
    basic_service_start_date: Optional[date] = Field(None, title="基层服务起始日期",
                                                     description="基层服务起始日期",
                                                     example="2010-01-01")
    basic_service_end_date: Optional[date] = Field(None, title="基层服务结束日期",
                                                   description="基层服务结束日期",
                                                   example="2010-01-01")
    special_education_teacher: bool = Field(..., title="是否特教", description="是否特教")
    dual_teacher: bool = Field(..., title="是否双师型", description="是否双师型")
    has_occupational_skill_level_certificate: bool = Field(..., title="是否具备职业技能等级证书",
                                                           description="是否具备职业技能等级证书", )
    enterprise_work_experience: str = Field(..., title="企业工作时长", description="企业工作时长", example="3年")
    county_level_backbone: bool = Field(..., title="是否县级以上骨干", description="是否县级以上骨干")
    psychological_health_education_teacher: bool = Field(..., title="是否心理健康教育教师",
                                                         description="是否心理健康教育教师")
    recruitment_method: str = Field(..., title="招聘方式", description="招聘方式", example="招聘")
    teacher_number: str = Field("", title="教职工号", description="教职工号", example="123456789012345678")

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
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    任职单位：employer
    # 最高学历：highest_education
    政治面貌：political_status
    是否在编：in_post
    用人形式：employment_form
    进本校时间：enter_school_time
    审核状态：approval_status
    """
    # teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: Optional[str] = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别", example="男")
    teacher_employer: Optional[int] = Query(None, title="任职单位", description="任职单位", example="xx学校")
    highest_education: Optional[str] = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    employment_form: Optional[str] = Query("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] = Query(None, title="进本校时间", description="进本校时间", example="2010-01-01")
    teacher_approval_status: Optional[str] = Query("", title="审核状态", description="审核状态", example="待审核")


class NewTeacherRe(BaseModel):
    teacher_base_id: Optional[int] = Field(0, title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Field("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Field("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: str = Field("", title="性别", description="性别", example="男")
    teacher_employer: int = Field(None, title="任职单位", description="任职单位", example="xx学校")
    highest_education: Optional[str] = Field("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] = Field("", title="政治面貌", description="政治面貌", example="群众")
    employment_form: Optional[str] = Field("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] = Field(None, title="进本校时间", description="进本校时间", example="2010-01-01")
    teacher_approval_status: str = Field("", title="审核状态", description="审核状态", example="待审核")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    school_name: str = Field("", title="", description="", example="")


class CurrentTeacherQuery(BaseModel):
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    任职单位：employer
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
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别", example="男")
    teacher_employer: Optional[int] = Query(None, title="任职单位", description="任职单位", example="xx学校")
    highest_education: str = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: str = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    employment_form: str = Query("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] = Query(None, title="进本校时间", description="进本校时间", example="2010-01-01")


class CurrentTeacherQueryRe(BaseModel):
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    任职单位：employer
    # 最高学历：highest_education
    政治面貌：political_status
    是否在编：in_post
    用人形式：employment_form
    进本校时间：enter_school_time
    审核状态：approval_status
    """
    teacher_base_id: Optional[int] = Field(None, title="教师ID", description="教师ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: str = Query("", title="性别", description="性别", example="男")
    teacher_employer: int = Query("", title="任职单位", description="任职单位", example="xx学校")
    highest_education: Optional[str] = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    employment_form: Optional[str] = Query("", title="用人形式", description="用人形式", example="合同")
    enter_school_time: Optional[date] = Query(None, title="进本校时间", description="进本校时间", example="2010-01-01")
    school_name: Optional[str] = Query("", title="", description="", example="")
