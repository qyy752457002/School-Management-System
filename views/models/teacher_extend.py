from pydantic import BaseModel, Field, model_validator, ValidationError, field_validator
from datetime import date
from fastapi import Query
from models.public_enum import YesOrNo
from typing import Optional, List, Any


class TeacherLearnExperienceModel(BaseModel):
    """
    教师ID：teacher_id
    获的学历：education_obtained
    获得学历国家/地区：country_or_region_of_education
    获得学历的院校机构：institution_of_education_obtained
    所学妆业：major_learned
    是否师范类专业：is_major_normal
    入学时间：admission_date
    毕业时间：graduation_date
    学位层次：degree_level
    学位名称：degree_name
    获取学位过家地区：country_or_region_of_degree_obtained
    获得学位院校机构：institution_of_degree_obtained
    学位授予时间：degree_award_date
    学习方式：study_mode
    在学单位类别：type_of_institution
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    education_obtained: str = Field(..., title="获的学历", description="获的学历")
    country_or_region_of_education: str = Field(..., title="获得学历国家/地区", description="获得学历国家/地区")
    institution_of_education_obtained: str = Field(..., title="获得学历的院校机构", description="获得学历的院校机构")
    major_learned: str = Field(..., title="所学妆业", description="所学专业")
    is_major_normal: str = Field(..., title="是否师范类专业", description="是否师范类专业")
    admission_date: Optional[date] = Field(None, title="入学年月", description="入学时间")
    graduation_date: Optional[date] = Field(None, title="结束学业年月", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    degree_name: str = Field(..., title="学位名称", description="学位名称")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: date = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习形式", description="学习方式")
    type_of_institution: str = Field("", title="在学单位类别", description="在学单位类别")


class TeacherLearnExperienceComModel(TeacherLearnExperienceModel):
    pass


class TeacherLearnExperienceResultModel(TeacherLearnExperienceModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherLearnExperienceUpdateModel(BaseModel):
    """
    教师ID：teacher_id
    获的学历：education_obtained
    获得学历国家/地区：country_or_region_of_education
    获得学历的院校机构：institution_of_education_obtained
    所学妆业：major_learned
    是否师范类专业：is_major_normal
    入学时间：admission_date
    毕业时间：graduation_date
    学位层次：degree_level
    获取学位过家地区：country_or_region_of_degree_obtained
    获得学位院校机构：institution_of_degree_obtained
    学位授予时间：degree_award_date
    学习方式：study_mode
    在学单位类别：type_of_institution
    """
    teacher_learn_experience_id: int = Field(..., title="教师学习经历ID", description="教师学习经历ID")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    education_obtained: str = Field(..., title="获的学历", description="获的学历")
    country_or_region_of_education: str = Field(..., title="获得学历国家/地区", description="获得学历国家/地区")
    institution_of_education_obtained: str = Field(..., title="获得学历的院校机构", description="获得学历的院校机构")
    major_learned: str = Field(..., title="所学妆业", description="所学妆业")
    is_major_normal: str = Field(..., title="是否师范类专业", description="是否师范类专业")
    admission_date: Optional[date] = Field(None, title="入学年月", description="入学时间")
    graduation_date: Optional[date] = Field(None, title="结束学业年月", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    degree_name: str = Field(..., title="学位名称", description="学位名称")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: date = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习形式", description="学习方式")
    type_of_institution: str = Field("", title="在学单位类别", description="在学单位类别")


class TeacherWorkExperienceModel(BaseModel):
    """
    教师ID：teacher_id
    任职单位名称：employment_institution_name
    开始时间：start_date
    结束时间：end_date
    在职岗位：on_duty_position
    单位性质类别：institution_nature_category
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    employment_institution_name: str = Field(..., title="工作单位", description="任职单位名称")
    start_date: date = Field(..., title="工作起始日期", description="开始时间")
    end_date: date = Field(..., title="工作结束日期", description="结束时间")
    on_duty_position: str = Field("", title="任职岗位", description="在职岗位")
    institution_nature_category: str = Field("", title="单位性质类别", description="单位性质类别")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        if isinstance(data["teacher_id"], str):
            data["teacher_id"] = int(data["teacher_id"])
        elif isinstance(data["teacher_id"], int):
            data["teacher_id"] = str(data["teacher_id"])
        else:
            pass
        return data



class TeacherWorkExperienceComModel(TeacherWorkExperienceModel):
    pass


class TeacherWorkExperienceResultModel(TeacherWorkExperienceModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherWorkExperienceUpdateModel(BaseModel):
    """
    teacher_work_experience：teacher_work_experience_id
    教师ID：teacher_id
    任职单位名称：employment_institution_name
    开始时间：start_date
    结束时间：end_date
    在职岗位：on_duty_position
    单位性质类别：institution_nature_category
    """
    teacher_work_experience_id: int | str = Field(..., title="teacher_work_experience_id",
                                                  description="teacher_work_experience_id")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    employment_institution_name: str = Field(..., title="工作单位", description="任职单位名称")
    start_date: date = Field(..., title="工作起始日期", description="开始时间")
    end_date: date = Field(..., title="工作结束日期", description="结束时间")
    on_duty_position: str = Field(..., title="任职岗位", description="在职岗位")
    institution_nature_category: str = Field("", title="单位性质类别", description="单位性质类别")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        if isinstance(data["teacher_id"], str):
            data["teacher_id"] = int(data["teacher_id"])
        elif isinstance(data["teacher_id"], int):
            data["teacher_id"] = str(data["teacher_id"])
        else:
            pass
        if isinstance(data["teacher_work_experience_id"], str):
            data["teacher_work_experience_id"] = int(data["teacher_work_experience_id"])
        elif isinstance(data["teacher_work_experience_id"], int):
            data["teacher_work_experience_id"] = str(data["teacher_work_experience_id"])
        else:
            pass
        return data


# class TeacherJobAppointmentsModel(BaseModel):
#     """
#     教师ID：teacher_id
#     岗位类别：position_category
#     岗位等级：position_level
#     校级职务：school_level_position
#     是否兼任其他岗位：is_concurrent_other_positions
#     兼任岗位类别：concurrent_position_category
#     兼任岗位登记：concurrent_position_registration
#     任职单位名称：employment_institution_name
#     聘任开始时间：appointment_start_date
#     结束时间：end_date
#     """
#     teacher_id: int = Field(..., title="教师ID", description="教师ID")
#     position_category: str = Field(..., title="岗位类别", description="岗位类别")
#     position_level: str = Field(..., title="岗位等级", description="岗位等级")
#     school_level_position: str = Field(..., title="校级职务", description="校级职务")
#     is_concurrent_other_positions: YesOrNo = Field("N", title="是否兼任其他岗位", description="是否兼任其他岗位")
#     concurrent_position_category: Optional[str] = Field(..., title="兼任岗位类别", description="兼任岗位类别")
#     concurrent_position_level: Optional[str] = Field(..., title="兼任岗位登记", description="兼任岗位登记")
#     employment_institution_name: str = Field(..., title="工作单位", description="任职单位名称")
#     appointment_start_date: date = Field(..., title="开始年月", description="聘任开始时间")
#     start_date: date = Field(..., title="任职开始年月", description="任职开始年月")

class TeacherJobAppointmentsModel(BaseModel):
    """
    教师ID：teacher_id
    岗位类别：position_category
    岗位等级：position_level
    校级职务：school_level_position
    是否兼任其他岗位：is_concurrent_other_positions
    兼任岗位类别：concurrent_position
    任职单位名称：employment_institution_name
    聘任开始时间：appointment_start_date
    结束时间：end_date
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    position_category: str = Field(..., title="岗位类别", description="岗位类别")
    position_level: str = Field(..., title="岗位等级", description="岗位等级")
    school_level_position: str = Field(..., title="校级职务", description="校级职务")
    is_concurrent_other_positions: bool = Field(False, title="是否兼任其他岗位", description="是否兼任其他岗位")
    concurrent_position: Optional[List[dict]] = Field(default=[{"category": "默认类别", "level": "默认等级"}],
                                                      title="兼任岗位", description="兼任岗位")
    appointment_start_date: date = Field(..., title="聘任开始年月", description="聘任开始时间")
    start_date: Optional[date] = Field(None, title="任职开始年月", description="任职开始年月")


class TeacherJobAppointmentsComModel(TeacherJobAppointmentsModel):
    pass


class TeacherJobAppointmentsResultModel(TeacherJobAppointmentsModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherJobAppointmentsUpdateModel(BaseModel):
    """
    教师ID：teacher_id
    岗位类别：position_category
    岗位等级：position_level
    校级职务：school_level_position
    是否兼任其他岗位：is_concurrent_other_positions
    兼任岗位类别：concurrent_position_category
    兼任岗位登记：concurrent_position_registration
    任职单位名称：employment_institution_name
    聘任开始时间：appointment_start_date
    结束时间：end_date
    """
    teacher_job_appointments_id: int = Field(..., title="teacher_job_appointments_id",
                                             description="teacher_job_appointments_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    position_category: str = Field(..., title="岗位类别", description="岗位类别")
    position_level: str = Field(..., title="岗位等级", description="岗位等级")
    school_level_position: str = Field(..., title="校级职务", description="校级职务")
    is_concurrent_other_positions: bool = Field(False, title="是否兼任其他岗位", description="是否兼任其他岗位")
    concurrent_position: Optional[List[dict]] = Field(default=[{"category": "默认类别", "level": "默认等级"}],
                                                      title="兼任岗位", description="兼任岗位")
    appointment_start_date: date = Field(..., title="聘任开始年月", description="聘任开始时间")
    start_date: Optional[date] = Field(None, description="任职开始年月")


# class TeacherJobAppointmentsUpdateModel(BaseModel):
#     """
#     teacher_job_appointments：teacher_job_appointments_id
#     教师ID：teacher_id
#     岗位类别：position_category
#     岗位等级：position_level
#     校级职务：school_level_position
#     是否兼任其他岗位：is_concurrent_other_positions
#     兼任岗位类别：concurrent_position_category
#     兼任岗位登记：concurrent_position_registration
#     任职单位名称：employment_institution_name
#     聘任开始时间：appointment_start_date
#     结束时间：end_date
#     """
#     teacher_job_appointments_id: int = Field(..., title="teacher_job_appointments_id",
#                                              description="teacher_job_appointments_id")
#     teacher_id: int = Field(..., title="教师ID", description="教师ID")
#     position_category: str = Field(..., title="岗位类别", description="岗位类别")
#     position_level: str = Field(..., title="岗位等级", description="岗位等级")
#     school_level_position: str = Field(..., title="校级职务", description="校级职务")
#     is_concurrent_other_positions: YesOrNo = Field("N", title="是否兼任其他岗位", description="是否兼任其他岗位")
#     concurrent_position_category: Optional[str] = Field(..., title="兼任岗位类别", description="兼任岗位类别")
#     concurrent_position_level: Optional[str] = Field(..., title="兼任岗位登记", description="兼任岗位登记")
#     employment_institution_name: str = Field(..., title="工作单位", description="任职单位名称")
#     appointment_start_date: date = Field(..., title="开始年月", description="聘任开始时间")
#     start_date: date = Field(..., title="任职开始年月", description="任职开始年月")


class TeacherProfessionalTitlesModel(BaseModel):
    """
    教师ID：teacher_id
    现专业技术职务：current_professional_title
    聘任单位名称：employing_institution_name
    聘任开始时间：employment_start_date
    聘任结束时间：employment_end_date
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    current_professional_title: str = Field(..., title="聘任专业技术职务", description="现专业技术职务")
    employing_institution_name: str = Field("", title="聘任单位名称", description="聘任单位名称")
    employment_start_date: date = Field(..., title="开始年月", description="聘任开始时间")
    employment_end_date: Optional[date] = Field(None, title="结束年月", description="聘任结束时间")


class TeacherProfessionalTitlesComModel(TeacherProfessionalTitlesModel):
    pass


class TeacherProfessionalTitlesResultModel(TeacherProfessionalTitlesModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherProfessionalTitlesUpdateModel(BaseModel):
    """
    teacher_professional_titles：teacher_professional_titles_id
    教师ID：teacher_id
    现专业技术职务：current_professional_title
    聘任单位名称：employing_institution_name
    聘任开始时间：employment_start_date
    聘任结束时间：employment_end_date
    """
    teacher_professional_titles_id: int = Field(..., title="teacher_professional_titles_id",
                                                description="teacher_professional_titles_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    current_professional_title: str = Field(..., title="聘任专业技术职务", description="现专业技术职务")
    employing_institution_name: str = Field("", title="聘任单位名称", description="聘任单位名称")
    employment_start_date: date = Field(..., title="开始年月", description="聘任开始时间")
    employment_end_date: Optional[date] = Field(None, title="结束年月", description="聘任结束时间")


class TeacherQualificationsModel(BaseModel):
    """
    教师ID：teacher_id
    教师资格证种类：teacher_qualification_type
    资格证号码：qualification_number
    任教学科：teaching_subject
    证书颁发时间：certificate_issue_date
    颁发机构：issuing_authority
    首次注册日期：first_registration_date
    定期注册日期：regular_registration_date
    定期注册结论：regular_registration_conclusion
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_qualification_type: str = Field(..., title="种类", description="教师资格证种类")
    qualification_number: str = Field(..., title="证书编号", description="资格证号码")
    teaching_subject: str = Field(..., title="任教学科", description="任教学科")
    certificate_issue_date: date = Field(..., title="颁发日期", description="证书颁发时间")
    issuing_authority: str = Field("", title="颁发机构", description="颁发机构")
    first_registration_date: Optional[date] = Field(None, title="首次注册日期", description="首次注册日期")
    regular_registration_date: Optional[date] = Field(None, title="定期注册日期", description="定期注册日期")
    regular_registration_conclusion: str = Field("", title="定期注册结论", description="定期注册结论")


class TeacherQualificationsComModel(TeacherQualificationsModel):
    pass


class TeacherQualificationsResultModel(TeacherQualificationsModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherQualificationsUpdateModel(BaseModel):
    """
    teacher_qualifications：teacher_qualifications_id
    教师ID：teacher_id
    教师资格证种类：teacher_qualification_type
    资格证号码：qualification_number
    任教学科：teaching_subject
    证书颁发时间：certificate_issue_date
    颁发机构：issuing_authority
    首次注册日期：first_registration_date
    定期注册日期：regular_registration_date
    定期注册结论：regular_registration_conclusion
    """
    teacher_qualifications_id: int = Field(..., title="teacher_qualifications_id",
                                           description="teacher_qualifications_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_qualification_type: str = Field(..., title="种类", description="教师资格证种类")
    qualification_number: str = Field(..., title="证书编号", description="资格证号码")
    teaching_subject: str = Field(..., title="任教学科", description="任教学科")
    certificate_issue_date: date = Field(..., title="颁发日期", description="证书颁发时间")
    issuing_authority: str = Field("", title="颁发机构", description="颁发机构")
    first_registration_date: Optional[date] = Field(None, title="首次注册日期", description="首次注册日期")
    regular_registration_date: Optional[date] = Field(None, title="定期注册日期", description="定期注册日期")
    regular_registration_conclusion: str = Field("", title="定期注册结论", description="定期注册结论")


class TeacherSkillCertificatesModel(BaseModel):
    """
    教师ID：teacher_id
    语种：language
    掌握程度：proficiency_level
    其他技能名称：other_skill_name
    其他技能程度：other_skill_level
    证书类型：certificate_type
    语言证书名称：language_certificate_name
    发证年月：issue_year_month
    发证单位：issuing_authority
    证书编号：certificate_number
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    language: str = Field(..., title="语种", description="语种")
    proficiency_level: str = Field(..., title="掌握程度", description="掌握程度")
    other_skill_name: str = Field("", title="其他技能名称", description="其他技能名称")
    other_skill_level: str = Field("", title="其他技能掌握程度", description="其他技能程度")
    certificate_type: str = Field("", title="证书类型", description="证书类型")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称")
    issue_year_month: Optional[date] = Field(None, title="发证年月", description="发证年月")
    issuing_authority: str = Field("", title="发证单位", description="发证单位")
    certificate_number: str = Field("", title="证书编号", description="证书编号")


class TeacherSkillCertificatesComModel(TeacherSkillCertificatesModel):
    pass


class TeacherSkillCertificatesResultModel(TeacherSkillCertificatesModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherSkillCertificatesUpdateModel(BaseModel):
    """
    teacher_skill_certificates：teacher_skill_certificates_id
    教师ID：teacher_id
    语种：language
    掌握程度：proficiency_level
    其他技能名称：other_skill_name
    其他技能程度：other_skill_level
    证书类型：certificate_type
    语言证书名称：language_certificate_name
    发证年月：issue_year_month
    发证单位：issuing_authority
    证书编号：certificate_number
    """
    teacher_skill_certificates_id: int = Field(..., title="teacher_skill_certificates_id",
                                               description="teacher_skill_certificates_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    language: str = Field(..., title="语种", description="语种")
    proficiency_level: str = Field(..., title="掌握程度", description="掌握程度")
    other_skill_name: str = Field("", title="其他技能名称", description="其他技能名称")
    other_skill_level: str = Field("", title="其他技能掌握程度", description="其他技能程度")
    certificate_type: str = Field("", title="证书类型", description="证书类型")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称")
    issue_year_month: Optional[date] = Field(None, title="发证年月", description="发证年月")
    issuing_authority: str = Field("", title="发证单位", description="发证单位")
    certificate_number: str = Field("", title="证书编号", description="证书编号")


class TeacherEthicRecordsModel(BaseModel):
    """
    教师ID：teacher_id
    师德考核时间：ethics_assessment_date
    师德考核结论：ethics_assessment_conclusion
    考核单位名称：assessment_institution_name
    荣誉级别：honor_level
    荣誉称号：honor_title
    荣誉日期：honor_date
    荣誉授予单位名称：awarding_institution_name
    荣誉记录描述：honor_record_description
    处分类别：disciplinary_category
    处分原因：disciplinary_reason
    处分日期：disciplinary_date
    处分单位名称：disciplinary_institution_name
    处分记录描述：disciplinary_record_description
    处分发生日期：disciplinary_occurrence_date
    处分撤销日期：disciplinary_revocation_date
    处分撤销原因：disciplinary_revocation_reason
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethics_assessment_date: date = Field(..., title="师德考核时间（年月）", description="师德考核时间")
    ethics_assessment_conclusion: str = Field(..., title="考核结论", description="师德考核结论")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")
    honor_level: str = Field("", title="荣誉级别", description="荣誉级别")
    honor_title: str = Field("", title="获得荣誉称号", description="荣誉称号")
    honor_date: Optional[date] = Field(None, title="荣誉发生日期", description="荣誉日期")
    awarding_institution_name: str = Field("", title="荣誉授予单位名称", description="荣誉授予单位名称")
    honor_record_description: str = Field("", title="荣誉记录描述", description="荣誉记录描述")
    disciplinary_category: str = Field(..., title="处分类别", description="处分类别")
    disciplinary_reason: str = Field(..., title="处分原因", description="处分原因")
    disciplinary_date: date = Field(..., title="处分日期", description="处分日期")
    disciplinary_institution_name: str = Field("", title="处分单位名称", description="处分单位名称")
    disciplinary_record_description: str = Field("", title="处分记录描述", description="处分记录描述")
    disciplinary_occurrence_date: date = Field(..., title="处分发生日期（年月日）", description="处分发生日期")
    disciplinary_revocation_date: date = Field(..., title="处分撤销日期", description="处分撤销日期")
    disciplinary_revocation_reason: str = Field("", title="处分撤销原因", description="处分撤销原因")


class TeacherEthicRecordsComModel(TeacherEthicRecordsModel):
    pass


class TeacherEthicRecordsResultModel(TeacherEthicRecordsModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TeacherEthicRecordsUpdateModel(BaseModel):
    """
    teacher_ethic_records：teacher_ethic_records_id
    教师ID：teacher_id
    师德考核时间：ethics_assessment_date
    师德考核结论：ethics_assessment_conclusion
    考核单位名称：assessment_institution_name
    荣誉级别：honor_level
    荣誉称号：honor_title
    荣誉日期：honor_date
    荣誉授予单位名称：awarding_institution_name
    荣誉记录描述：honor_record_description
    处分类别：disciplinary_category
    处分原因：disciplinary_reason
    处分日期：disciplinary_date
    处分单位名称：disciplinary_institution_name
    处分记录描述：disciplinary_record_description
    处分发生日期：disciplinary_occurrence_date
    处分撤销日期：disciplinary_revocation_date
    处分撤销原因：disciplinary_revocation_reason
    """
    teacher_ethic_records_id: int = Field(..., title="teacher_ethic_records_id", description="teacher_ethic_records_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    ethics_assessment_date: date = Field(..., title="师德考核时间（年月）", description="师德考核时间")
    ethics_assessment_conclusion: str = Field(..., title="考核结论", description="师德考核结论")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")
    honor_level: str = Field("", title="荣誉级别", description="荣誉级别")
    honor_title: str = Field("", title="荣誉称号", description="荣誉称号")
    honor_date: Optional[date] = Field(None, title="荣誉日期", description="荣誉日期")
    awarding_institution_name: str = Field("", title="荣誉授予单位名称", description="荣誉授予单位名称")
    honor_record_description: str = Field("", title="荣誉记录描述", description="荣誉记录描述")
    disciplinary_category: str = Field(..., title="处分类别", description="处分类别")
    disciplinary_reason: str = Field(..., title="处分原因", description="处分原因")
    disciplinary_date: date = Field(..., title="处分日期", description="处分日期")
    disciplinary_institution_name: str = Field("", title="处分单位名称", description="处分单位名称")
    disciplinary_record_description: str = Field("", title="处分记录描述", description="处分记录描述")
    disciplinary_occurrence_date: date = Field(..., title="处分发生日期（年月日）", description="处分发生日期")
    disciplinary_revocation_date: date = Field(..., title="处分撤销日期", description="处分撤销日期")
    disciplinary_revocation_reason: str = Field("", title="处分撤销原因", description="处分撤销原因")


class EducationalTeachingModel(BaseModel):
    """
    教师ID：teacher_id
    学年：academic_year
    学期：semester
    任教阶段：teaching_stage
    任课课程类别：course_category
    任课学科类别：subject_category
    任课课程：course_name
    平均每周教学课时：average_weekly_teaching_hours
    承担其他工作：other_responsibilities
    平均每周其他工作折合课时：average_weekly_other_duties_hours
    兼任工作：concurrent_job
    兼任工作名称：concurrent_job_name
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    academic_year: str = Field(..., title="学年", description="学年")
    semester: str = Field(..., title="学期", description="学期")
    teaching_stage: str = Field(..., title="任教阶段", description="任教阶段")
    course_category: str = Field(..., title="任课课程类别", description="任课课程类别")
    subject_category: str = Field(..., title="任课学科类别", description="任课学科类别")
    course_name: str = Field(..., title="任课课程", description="任课课程")
    average_weekly_teaching_hours: str = Field(..., title="平均每周教学课时", description="平均每周教学课时")
    other_responsibilities: str = Field("", title="承担其他工作", description="承担其他工作")
    average_weekly_other_duties_hours: str = Field(..., title="平均每周其他工作折合课时",
                                                   description="平均每周其他工作折合课时")
    concurrent_job: str = Field(..., title="兼任工作", description="兼任工作")
    concurrent_job_name: str = Field("", title="兼任工作名称", description="兼任工作名称")


class EducationalTeachingComModel(EducationalTeachingModel):
    pass


class EducationalTeachingResultModel(EducationalTeachingModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class EducationalTeachingUpdateModel(BaseModel):
    """
    educational_teaching：educational_teaching_id
    教师ID：teacher_id
    学年：academic_year
    学期：semester
    任教阶段：teaching_stage
    任课课程类别：course_category
    任课学科类别：subject_category
    任课课程：course_name
    平均每周教学课时：average_weekly_teaching_hours
    承担其他工作：other_responsibilities
    平均每周其他工作折合课时：average_weekly_other_duties_hours
    兼任工作：concurrent_job
    兼任工作名称：concurrent_job_name
    """
    educational_teaching_id: int = Field(..., title="educational_teaching_id", description="educational_teaching_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    academic_year: str = Field(..., title="学年", description="学年")
    semester: str = Field(..., title="学期", description="学期")
    teaching_stage: str = Field(..., title="任教阶段", description="任教阶段")
    course_category: str = Field(..., title="任课课程类别", description="任课课程类别")
    subject_category: str = Field(..., title="任课学科类别", description="任课学科类别")
    course_name: str = Field(..., title="任课课程", description="任课课程")
    average_weekly_teaching_hours: str = Field(..., title="平均每周教学课时", description="平均每周教学课时")
    other_responsibilities: str = Field("", title="承担其他工作", description="承担其他工作")
    average_weekly_other_duties_hours: str = Field(..., title="平均每周其他工作折合课时",
                                                   description="平均每周其他工作折合课时")
    concurrent_job: str = Field(..., title="兼任工作", description="兼任工作")
    concurrent_job_name: str = Field("", title="兼任工作名称", description="兼任工作名称")


class DomesticTrainingModel(BaseModel):
    """
    教师ID：teacher_id
    培训年度：training_year
    培训类型：training_type
    培训项目：training_project
    培训机构：training_institution
    培训方式：training_mode
    培训学时：training_hours
    培训学分：training_credits
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    training_year: str = Field(..., title="培训年度", description="培训年度")
    training_type: str = Field(..., title="培训类别", description="培训类型")
    training_project: str = Field(..., title="项目名称", description="培训项目")
    training_institution: str = Field("", title="机构名称", description="培训机构")
    training_mode: str = Field(..., title="培训方式", description="培训方式")
    training_hours: str = Field(..., title="获得学时", description="培训学时")
    training_credits: str = Field("", title="培训学分", description="培训学分")


class DomesticTrainingComModel(DomesticTrainingModel):
    pass


class DomesticTrainingResultModel(DomesticTrainingModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class DomesticTrainingUpdateModel(BaseModel):
    """
    domestic_training：domestic_training_id
    教师ID：teacher_id
    培训年度：training_year
    培训类型：training_type
    培训项目：training_project
    培训机构：training_institution
    培训方式：training_mode
    培训学时：training_hours
    培训学分：training_credits
    """
    domestic_training_id: int = Field(..., title="domestic_training_id", description="domestic_training_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    training_year: str = Field(..., title="培训年度", description="培训年度")
    training_type: str = Field(..., title="培训类别", description="培训类型")
    training_project: str = Field(..., title="项目名称", description="培训项目")
    training_institution: str = Field("", title="机构名称", description="培训机构")
    training_mode: str = Field(..., title="培训方式", description="培训方式")
    training_hours: str = Field(..., title="获得学时", description="培训学时")
    training_credits: str = Field("", title="培训学分", description="培训学分")


class OverseasStudyModel(BaseModel):
    """
    教师ID：teacher_id
    开始日期：start_date
    结束日期：end_date
    国家地区：country_region
    研修机构名称：training_institution_name
    项目名称：project_name
    项目组织单位名称：organizing_institution_name
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    start_date: date = Field(..., title="开始日期", description="开始日期")
    end_date: date = Field(..., title="结束日期", description="结束日期")
    country_region: str = Field(..., title="国家/地区", description="国家地区")
    training_institution_name: str = Field("", title="研修机构名称", description="研修机构名称")
    project_name: str = Field(..., title="项目名称", description="项目名称")
    organizing_institution_name: str = Field("", title="项目组织单位名称", description="项目组织单位名称")


class OverseasStudyComModel(OverseasStudyModel):
    pass


class OverseasStudyResultModel(OverseasStudyModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class OverseasStudyUpdateModel(BaseModel):
    """
    overseas_study：overseas_study_id
    教师ID：teacher_id
    开始日期：start_date
    结束日期：end_date
    国家地区：country_region
    研修机构名称：training_institution_name
    项目名称：project_name
    项目组织单位名称：organizing_institution_name
    """
    overseas_study_id: int = Field(..., title="overseas_study_id", description="overseas_study_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    start_date: date = Field(..., title="开始日期", description="开始日期")
    end_date: date = Field(..., title="结束日期", description="结束日期")
    country_region: str = Field(..., title="国家/地区", description="国家地区")
    training_institution_name: str = Field("", title="研修机构名称", description="研修机构名称")
    project_name: str = Field(..., title="项目名称", description="项目名称")
    organizing_institution_name: str = Field("", title="项目组织单位名称", description="项目组织单位名称")


class TalentProgramModel(BaseModel):
    """
    教师ID：teacher_id
    人才项目名称：talent_project_name
    入选年份：selected_year
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    talent_project_name: str = Field("", title="入选人才项目名称", description="人才项目名称")
    selected_year: str = Field("", title="年份", description="入选年份")


class TalentProgramComModel(TalentProgramModel):
    pass


class TalentProgramResultModel(TalentProgramModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class TalentProgramUpdateModel(BaseModel):
    """
    talent_program：talent_program_id
    教师ID：teacher_id
    人才项目名称：talent_project_name
    入选年份：selected_year
    """
    talent_program_id: int = Field(..., title="talent_program_id", description="talent_program_id")
    teacher_id: int = Field(None, title="教师ID", description="教师ID")
    talent_project_name: str = Field("", title="人才项目名称", description="人才项目名称")
    selected_year: str = Field("", title="入选年份", description="入选年份")


class AnnualReviewModel(BaseModel):
    """
    教师ID：teacher_id
    考核年度：assessment_year
    考核结果：assessment_result
    考核单位名称：assessment_institution_name
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    assessment_year: str = Field(..., title="考核年度", description="考核年度")
    assessment_result: str = Field(..., title="考核结果", description="考核结果")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")


class AnnualReviewComModel(AnnualReviewModel):
    pass


class AnnualReviewResultModel(AnnualReviewModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class AnnualReviewUpdateModel(BaseModel):
    """
    annual_review：annual_review_id
    教师ID：teacher_id
    考核年度：assessment_year
    考核结果：assessment_result
    考核单位名称：assessment_institution_name
    """
    annual_review_id: int = Field(..., title="annual_review_id", description="annual_review_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    assessment_year: str = Field(..., title="考核年度", description="考核年度")
    assessment_result: str = Field(..., title="考核结果", description="考核结果")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")


class ResearchAchievementsModel(BaseModel):
    """
    教师ID：teacher_id
    科研成果种类：research_achievement_type
    类型：type
    是否代表性成果或项目：representative_or_project
    名称：name
    学科领域：disciplinary_field
    本人角色：role
    日期：date
    批准号：approval_number
    经费额度：funding_amount
    开始年月：start_year_month
    结束日期：end_date
    本人排名：ranking
    委托单位：entrusting_unit
    来源：source
    出版社名称：publisher_name
    出版号：publication_number
    总字数：total_words
    本人撰写字数：self_written_words
    发表刊物名称：journal_name
    卷号：volume_number
    期号：issue_number
    论文收录情况：indexing_status
    起始页码：start_page
    结束页码：end_page
    本人排名：personal_rank
    等级：research_level
    其他等级：other_level
    授权国家：authorized_country
    授权单位：authorized_organization
    完成地点：completion_location
    本人工作描述：work_description
    专利号：patent_number
    委托方：entrusting_party
    证书号：certificate_number
    有效期：validity_period
    标准号：standard_number
    发布单位：publishing_organization
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    research_achievement_type: str = Field(..., title="科研成果类型", description="科研成果种类")
    type: str = Field("", title="类型", description="类型")
    representative_or_project: Optional[bool] = Field(None, title="是否代表性成果和项目",
                                                      description="是否代表性成果或项目")
    name: str = Field("", title="名称", description="名称")
    disciplinary_field: str = Field("", title="学科领域", description="学科领域")
    role: str = Field("", title="本人角色", description="本人角色")
    research_date: Optional[date] = Field(None, title="日期", description="日期")
    approval_number: str = Field("", title="批准号", description="批准号")
    funding_amount: str = Field("", title="经费额度", description="经费额度")
    start_year_month: Optional[date] = Field(None, title="开始年月", description="开始年月")
    end_date: Optional[date] = Field(None, title="结束日期", description="结束日期")
    ranking: str = Field("", title="本人排名", description="本人排名")
    entrusting_unit: str = Field("", title="委托单位", description="委托单位")
    source: str = Field("", title="来源", description="来源")
    publisher_name: str = Field("", title="出版社名称", description="出版社名称")
    publication_number: str = Field("", title="出版号", description="出版号")
    total_words: int = Field(0, title="总字数", description="总字数")
    self_written_words: int = Field(0, title="本人撰写字数", description="本人撰写字数")
    journal_name: str = Field("", title="发表刊物名称", description="发表刊物名称")
    volume_number: int = Field(0, title="卷号", description="卷号")
    issue_number: int = Field(0, title="期号", description="期号")
    indexing_status: str = Field("", title="论文收录情况", description="论文收录情况")
    start_page: int = Field(0, title="起始页码", description="起始页码")
    end_page: int = Field(0, title="结束页码", description="结束页码")
    personal_rank: str = Field("", title="本人排名", description="本人排名")
    research_level: str = Field("", title="等级", description="等级")
    other_level: str = Field("", title="其他等级", description="其他等级")
    authorized_country: str = Field("", title="授权国家", description="授权国家")
    authorized_organization: str = Field("", title="授权单位", description="授权单位")
    completion_location: str = Field("", title="完成地点", description="完成地点")
    work_description: str = Field("", title="本人工作描述", description="本人工作描述")
    patent_number: str = Field("", title="专利号", description="专利号")
    entrusting_party: str = Field("", title="委托方", description="委托方")
    certificate_number: str = Field("", title="证书号", description="证书号")
    validity_period: Optional[date] = Field(None, title="有效期", description="有效期")
    standard_number: str = Field("", title="标准号", description="标准号")
    publishing_organization: str = Field("", title="发布单位", description="发布单位")


class ResearchAchievementsComModel(ResearchAchievementsModel):
    pass


class ResearchAchievementsResultModel(ResearchAchievementsModel):
    failed_msg: str = Field(..., title="错误信息", description="错误信息", key="failed_msg")


class ResearchAchievementsUpdateModel(BaseModel):
    """
    research_achievements：research_achievements_id
    教师ID：teacher_id
    科研成果种类：research_achievement_type
    类型：type
    是否代表性成果或项目：representative_or_project
    名称：name
    学科领域：disciplinary_field
    本人角色：role
    日期：date
    批准号：approval_number
    经费额度：funding_amount
    开始年月：start_year_month
    结束日期：end_date
    本人排名：ranking
    委托单位：entrusting_unit
    来源：source
    出版社名称：publisher_name
    出版号：publication_number
    总字数：total_words
    本人撰写字数：self_written_words
    发表刊物名称：journal_name
    卷号：volume_number
    期号：issue_number
    论文收录情况：indexing_status
    起始页码：start_page
    结束页码：end_page
    本人排名：personal_rank
    等级：research_level
    其他等级：other_level
    授权国家：authorized_country
    授权单位：authorized_organization
    完成地点：completion_location
    本人工作描述：work_description
    专利号：patent_number
    委托方：entrusting_party
    证书号：certificate_number
    有效期：validity_period
    标准号：standard_number
    发布单位：publishing_organization
    """
    research_achievements_id: int = Field(..., title="research_achievements_id", description="research_achievements_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    research_achievement_type: str = Field(..., title="科研成果类型", description="科研成果种类")
    type: str = Field("", title="类型", description="类型")
    representative_or_project: Optional[bool] = Field(None, title="是否代表性成果和项目",
                                                      description="是否代表性成果或项目")
    name: str = Field("", title="名称", description="名称")
    disciplinary_field: str = Field("", title="学科领域", description="学科领域")
    role: str = Field("", title="本人角色", description="本人角色")
    research_date: Optional[date] = Field(None, title="日期", description="日期")
    approval_number: str = Field("", title="批准号", description="批准号")
    funding_amount: str = Field("", title="经费额度", description="经费额度")
    start_year_month: Optional[date] = Field(None, title="开始年月", description="开始年月")
    end_date: Optional[date] = Field(None, title="结束日期", description="结束日期")
    ranking: str = Field("", title="本人排名", description="本人排名")
    entrusting_unit: str = Field("", title="委托单位", description="委托单位")
    source: str = Field("", title="来源", description="来源")
    publisher_name: str = Field("", title="出版社名称", description="出版社名称")
    publication_number: str = Field("", title="出版号", description="出版号")
    total_words: Optional[int] = Field(None, title="总字数", description="总字数")
    self_written_words: Optional[int] = Field(None, title="本人撰写字数", description="本人撰写字数")
    journal_name: str = Field("", title="发表刊物名称", description="发表刊物名称")
    volume_number: Optional[int] = Field(None, title="卷号", description="卷号")
    issue_number: Optional[int] = Field(None, title="期号", description="期号")
    indexing_status: str = Field("", title="论文收录情况", description="论文收录情况")
    start_page: Optional[int] = Field(None, title="起始页码", description="起始页码")
    end_page: Optional[int] = Field(None, title="结束页码", description="结束页码")
    personal_rank: str = Field("", title="本人排名", description="本人排名")
    research_level: str = Field("", title="等级", description="等级")
    other_level: str = Field("", title="其他等级", description="其他等级")
    authorized_country: str = Field("", title="授权国家", description="授权国家")
    authorized_organization: str = Field("", title="授权单位", description="授权单位")
    completion_location: str = Field("", title="完成地点", description="完成地点")
    work_description: str = Field("", title="本人工作描述", description="本人工作描述")
    patent_number: str = Field("", title="专利号", description="专利号")
    entrusting_party: str = Field("", title="委托方", description="委托方")
    certificate_number: str = Field("", title="证书号", description="证书号")
    validity_period: Optional[date] = Field(None, title="有效期", description="有效期")
    standard_number: str = Field("", title="标准号", description="标准号")
    publishing_organization: str = Field("", title="发布单位", description="发布单位")


class ResearchAchievementsQueryModel(BaseModel):
    """
    教师ID：teacher_id
    科研项目联合查询模型
    科研成果种类：research_achievement_type
    类型：type
    是否代表性成果或项目：representative_or_project
    名称：name
    学科领域：disciplinary_field
    本人角色：role
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    research_achievement_type: str = Query("", title="姓名", description="姓名", example="张三")
    type: str = Query("", title="类型", description="类型", example="类型")
    representative_or_project: Optional[bool] = Query(False, title="是否代表性成果和项目",
                                                      description="是否代表性成果或项目")
    name: str = Query("", title="名称", description="名称", example="名称")
    disciplinary_field: str = Query("", title="学科领域", description="学科领域", example="学科领域")
    role: str = Query("", title="本人角色", description="本人角色", example="本人角色")


class ResearchAchievementsQueryReModel(BaseModel):
    """
    教师ID：teacher_id
    科研项目联合查询模型
    科研成果种类：research_achievement_type
    类型：type
    是否代表性成果或项目：representative_or_project
    名称：name
    学科领域：disciplinary_field
    本人角色：role
    """
    research_achievements_id: int = Field(..., title="research_achievements_id", description="research_achievements_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    research_achievement_type: str = Query("", title="姓名", description="姓名", example="张三")
    type: str = Query("", title="类型", description="类型", example="类型")
    representative_or_project: Optional[bool] = Query(False, title="是否代表性成果和项目",
                                                      description="是否代表性成果或项目")
    name: str = Query("", title="名称", description="名称", example="名称")
    disciplinary_field: str = Query("", title="学科领域", description="学科领域", example="学科领域")
    role: str = Query("", title="本人角色", description="本人角色", example="本人角色")
