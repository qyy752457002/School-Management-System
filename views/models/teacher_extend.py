from pydantic import BaseModel, Field
from datetime import date

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
    major_learned: str = Field(..., title="所学妆业", description="所学妆业")
    is_major_normal: str = Field(..., title="是否师范类专业", description="是否师范类专业")
    admission_date: date = Field(None, title="入学时间", description="入学时间")
    graduation_date: date = Field(None, title="毕业时间", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: str = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习方式", description="学习方式")
    type_of_institution: str = Field("", title="在学单位类别", description="在学单位类别")


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
    admission_date: date = Field(None, title="入学时间", description="入学时间")
    graduation_date: date = Field(None, title="毕业时间", description="毕业时间")
    degree_level: str = Field(..., title="学位层次", description="学位层次")
    country_or_region_of_degree_obtained: str = Field(..., title="获取学位过家地区", description="获取学位过家地区")
    institution_of_degree_obtained: str = Field(..., title="获得学位院校机构", description="获得学位院校机构")
    degree_award_date: str = Field(..., title="学位授予时间", description="学位授予时间")
    study_mode: str = Field(..., title="学习方式", description="学习方式")
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
    employment_institution_name: str = Field(..., title="任职单位名称", description="任职单位名称")
    start_date: date = Field(None, title="开始时间", description="开始时间")
    end_date: date = Field(None, title="结束时间", description="结束时间")
    on_duty_position: str = Field("", title="在职岗位", description="在职岗位")
    institution_nature_category: str = Field("", title="单位性质类别", description="单位性质类别")


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
    teacher_work_experience_id: int = Field(..., title="teacher_work_experience_id",
                                            description="teacher_work_experience_id")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    employment_institution_name: str = Field(..., title="任职单位名称", description="任职单位名称")
    start_date: date = Field(None, title="开始时间", description="开始时间")
    end_date: date = Field(None, title="结束时间", description="结束时间")
    on_duty_position: str = Field(..., title="在职岗位", description="在职岗位")
    institution_nature_category: str = Field("", title="单位性质类别", description="单位性质类别")


class TeacherJobAppointmentsModel(BaseModel):
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
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    position_category: str = Field(..., title="岗位类别", description="岗位类别")
    position_level: str = Field(..., title="岗位等级", description="岗位等级")
    school_level_position: str = Field(..., title="校级职务", description="校级职务")
    is_concurrent_other_positions: bool = Field(False, title="是否兼任其他岗位", description="是否兼任其他岗位")
    concurrent_position_category: str = Field(..., title="兼任岗位类别", description="兼任岗位类别")
    concurrent_position_level: str = Field(..., title="兼任岗位登记", description="兼任岗位登记")
    employment_institution_name: str = Field(..., title="任职单位名称", description="任职单位名称")
    appointment_start_date: date = Field(..., title="聘任开始时间", description="聘任开始时间")
    start_date: date = Field(..., title="任职开始年月", description="任职开始年月")


class TeacherJobAppointmentsUpdateModel(BaseModel):
    """
    teacher_job_appointments：teacher_job_appointments_id
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
    concurrent_position_category: str = Field(..., title="兼任岗位类别", description="兼任岗位类别")
    concurrent_position_level: str = Field(..., title="兼任岗位登记", description="兼任岗位登记")
    employment_institution_name: str = Field(..., title="任职单位名称", description="任职单位名称")
    appointment_start_date: date = Field(..., title="聘任开始时间", description="聘任开始时间")
    start_date: date = Field(..., title="任职开始年月", description="任职开始年月")


class TeacherProfessionalTitlesModel(BaseModel):
    """
    教师ID：teacher_id
    现专业技术职务：current_professional_title
    聘任单位名称：employing_institution_name
    聘任开始时间：employment_start_date
    聘任结束时间：employment_end_date
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    current_professional_title: str = Field(..., title="现专业技术职务", description="现专业技术职务")
    employing_institution_name: str = Field("", title="聘任单位名称", description="聘任单位名称")
    employment_start_date: date = Field(..., title="聘任开始时间", description="聘任开始时间")
    employment_end_date: date = Field(None, title="聘任结束时间", description="聘任结束时间")


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
    current_professional_title: str = Field(..., title="现专业技术职务", description="现专业技术职务")
    employing_institution_name: str = Field("", title="聘任单位名称", description="聘任单位名称")
    employment_start_date: date = Field(..., title="聘任开始时间", description="聘任开始时间")
    employment_end_date: date = Field(None, title="聘任结束时间", description="聘任结束时间")


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
    teacher_qualification_type: str = Field(..., title="教师资格证种类", description="教师资格证种类")
    qualification_number: str = Field(..., title="资格证号码", description="资格证号码")
    teaching_subject: str = Field(..., title="任教学科", description="任教学科")
    certificate_issue_date: date = Field(..., title="证书颁发时间", description="证书颁发时间")
    issuing_authority: str = Field("", title="颁发机构", description="颁发机构")
    first_registration_date: date = Field(None, title="首次注册日期", description="首次注册日期")
    regular_registration_date: date = Field(None, title="定期注册日期", description="定期注册日期")
    regular_registration_conclusion: str = Field("", title="定期注册结论", description="定期注册结论")


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
    teacher_qualification_type: str = Field(..., title="教师资格证种类", description="教师资格证种类")
    qualification_number: str = Field(..., title="资格证号码", description="资格证号码")
    teaching_subject: str = Field(..., title="任教学科", description="任教学科")
    certificate_issue_date: date = Field(..., title="证书颁发时间", description="证书颁发时间")
    issuing_authority: str = Field("", title="颁发机构", description="颁发机构")
    first_registration_date: date = Field(None, title="首次注册日期", description="首次注册日期")
    regular_registration_date: date = Field(None, title="定期注册日期", description="定期注册日期")
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
    other_skill_level: str = Field("", title="其他技能程度", description="其他技能程度")
    certificate_type: str = Field("", title="证书类型", description="证书类型")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称")
    issue_year_month: date = Field(None, title="发证年月", description="发证年月")
    issuing_authority: str = Field("", title="发证单位", description="发证单位")
    certificate_number: str = Field("", title="证书编号", description="证书编号")


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
    other_skill_level: str = Field("", title="其他技能程度", description="其他技能程度")
    certificate_type: str = Field("", title="证书类型", description="证书类型")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称")
    issue_year_month: date = Field(None, title="发证年月", description="发证年月")
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
    ethics_assessment_date: date = Field(..., title="师德考核时间", description="师德考核时间")
    ethics_assessment_conclusion: str = Field(..., title="师德考核结论", description="师德考核结论")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")
    honor_level: str = Field(..., title="荣誉级别", description="荣誉级别")
    honor_title: str = Field("", title="荣誉称号", description="荣誉称号")
    honor_date: date = Field(..., title="荣誉日期", description="荣誉日期")
    awarding_institution_name: str = Field("", title="荣誉授予单位名称", description="荣誉授予单位名称")
    honor_record_description: str = Field("", title="荣誉记录描述", description="荣誉记录描述")
    disciplinary_category: str = Field(..., title="处分类别", description="处分类别")
    disciplinary_reason: str = Field(..., title="处分原因", description="处分原因")
    disciplinary_date: date = Field(..., title="处分日期", description="处分日期")
    disciplinary_institution_name: str = Field("", title="处分单位名称", description="处分单位名称")
    disciplinary_record_description: str = Field("", title="处分记录描述", description="处分记录描述")
    disciplinary_occurrence_date: date = Field(..., title="处分发生日期", description="处分发生日期")
    disciplinary_revocation_date: date = Field(..., title="处分撤销日期", description="处分撤销日期")
    disciplinary_revocation_reason: str = Field("", title="处分撤销原因", description="处分撤销原因")


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
    ethics_assessment_date: date = Field(..., title="师德考核时间", description="师德考核时间")
    ethics_assessment_conclusion: str = Field(..., title="师德考核结论", description="师德考核结论")
    assessment_institution_name: str = Field("", title="考核单位名称", description="考核单位名称")
    honor_level: str = Field(..., title="荣誉级别", description="荣誉级别")
    honor_title: str = Field("", title="荣誉称号", description="荣誉称号")
    honor_date: date = Field(..., title="荣誉日期", description="荣誉日期")
    awarding_institution_name: str = Field("", title="荣誉授予单位名称", description="荣誉授予单位名称")
    honor_record_description: str = Field("", title="荣誉记录描述", description="荣誉记录描述")
    disciplinary_category: str = Field(..., title="处分类别", description="处分类别")
    disciplinary_reason: str = Field(..., title="处分原因", description="处分原因")
    disciplinary_date: date = Field(..., title="处分日期", description="处分日期")
    disciplinary_institution_name: str = Field("", title="处分单位名称", description="处分单位名称")
    disciplinary_record_description: str = Field("", title="处分记录描述", description="处分记录描述")
    disciplinary_occurrence_date: date = Field(..., title="处分发生日期", description="处分发生日期")
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
