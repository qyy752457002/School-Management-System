from sqlalchemy import String, Date, INT, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date, datetime


class TeacherInfo(BaseDBModel):
    """
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
       部门：department
       用户名：username
        密码：hash_password
            hmotf: str = Field("", title="港澳台侨外", description="港澳台侨外", example="港澳台侨外")
    hukou_type: str = Field("", title="户口类别", description="户口类别", example="户口类别")
    main_teaching_level: str = Field("", title="主要任课学段", description="主要任课学段", example="主要任课学段")
    teacher_qualification_cert_num: str = Field("", title="教师资格证编号", description="教师资格证编号",
                                                example="教师资格证编号")
    teaching_discipline: str = Field("", title="任教学科", description="任教学科", example="任教学科")
    language: str = Field("", title="语种", description="语种", example="语种")
    language_proficiency_level: str = Field("", title="语言掌握程度", description="语言掌握程度",
                                            example="语言掌握程度")
    language_certificate_name: str = Field("", title="语言证书名称", description="语言证书名称", example="语言证书名称")
    contact_address: str = Field("", title="通讯地址省市县", description="通讯地址省市县", example="通讯地址省市县")
    contact_address_details: str = Field("", title="通讯地址详细信息", description="通讯地址详细信息",
                                         example="通讯地址详细信息")
    email: str = Field("", title="电子信箱", description="电子信箱", example="电子信箱")
    highest_education_level: str = Field("", title="最高学历层次", description="最高学历层次", example="最高学历层次")
    highest_degree_name: str = Field("", title="最高学位名称", description="最高学位名称", example="最高学位名称")
    is_major_graduate: bool = Field(..., title="是否为师范生", description="是否为师范生")
    other_contact_address_details: str = Field("", title="其他联系方式", description="其他联系方式")
       """
    __tablename__ = 'lfun_teachers_info'
    __table_args__ = {'comment': '教师基本信息表模型'}
    teacher_base_id: Mapped[int] = mapped_column(primary_key=True, comment="教师基本信息ID",
                                                 autoincrement=True)  # 与教师表关联，关系为一对一
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")  # 与教师表关联，关系为一对一
    ethnicity: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="民族")
    nationality: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="国家地区")
    political_status: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="政治面貌")
    native_place: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="籍贯")
    birth_place: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="出生地")
    former_name: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="曾用名")
    marital_status: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="婚姻状况")
    health_condition: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="健康状况")
    highest_education: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="最高学历")
    institution_of_highest_education: Mapped[str] = mapped_column(String(255), nullable=True, default="",
                                                                  comment="获得最高学历的院校或者机构")
    special_education_start_time: Mapped[date] = mapped_column(Date, nullable=True, comment="特教开时时间")
    start_working_date: Mapped[date] = mapped_column(Date, nullable=True, comment="参加工作年月")
    enter_school_time: Mapped[date] = mapped_column(Date, nullable=True, comment="进本校时间")
    source_of_staff: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="教职工来源")
    staff_category: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="教职工类别")
    in_post: Mapped[bool] = mapped_column(nullable=True, default=False, comment="是否在编")
    employment_form: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="用人形式")
    contract_signing_status: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="合同签订情况")
    current_post_type: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="现在岗位类型")
    current_post_level: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="现岗位等级")
    current_technical_position: Mapped[str] = mapped_column(String(255), nullable=True, default="",
                                                            comment="现专业技术职务")
    full_time_special_education_major_graduate: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                             comment="是否全日制特殊教育专业毕业")
    received_preschool_education_training: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                        comment="是否受过学前教育培训")
    full_time_normal_major_graduate: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                  comment="是否全日制师范类专业毕业")
    received_special_education_training: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                      comment="是否受过特教专业培训")
    has_special_education_certificate: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                    comment="是否有特教证书")
    information_technology_application_ability: Mapped[str] = mapped_column(nullable=True, default="",
                                                                             comment="信息技术应用能力")
    free_normal_college_student: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                              comment="是否免费师范生")
    participated_in_basic_service_project: Mapped[bool] = mapped_column(nullable=True,
                                                                        comment="是否参加基层服务项目")
    basic_service_start_date: Mapped[date] = mapped_column(Date, nullable=True, comment="基层服务起始日期")
    basic_service_end_date: Mapped[date] = mapped_column(Date, nullable=True, comment="基层服务结束日期")
    special_education_teacher: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                            comment="是否特教")
    dual_teacher: Mapped[bool] = mapped_column(nullable=True, default=False, comment="是否双师型")
    has_occupational_skill_level_certificate: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                           comment="是否具备职业技能等级证书")
    enterprise_work_experience: Mapped[str] = mapped_column(String(255), nullable=True, default="",
                                                            comment="企业工作时长")
    county_level_backbone: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                        comment="是否县级以上骨干")
    psychological_health_education_teacher: Mapped[bool] = mapped_column(nullable=True, default=False,
                                                                         comment="是否心理健康教育教师")
    recruitment_method: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="招聘方式")
    teacher_number: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="教职工号")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    department: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="部门")
    org_id: Mapped[int] = mapped_column(INT, nullable=True, default=0, comment="机构ID")

    hmotf: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="港澳台侨外")
    hukou_type: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="户口类别")
    main_teaching_level: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="主要任课学段")
    teacher_qualification_cert_num: Mapped[str] = mapped_column(String(255), nullable=True, default="",
                                                                comment="教师资格证编号")
    teaching_discipline: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="任教学科")
    language: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="语种")
    language_proficiency_level: Mapped[str] = mapped_column(String(255), nullable=True, default="",
                                                            comment="语言掌握程度")
    language_certificate_name: Mapped[str] = mapped_column(String(255), nullable=True, default="",comment="语言证书名称")
    contact_address: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="通讯地址省市县")
    contact_address_details: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="通讯地址详细信息")
    email: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="电子信箱")
    highest_education_level: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="最高学历层次")
    highest_degree_name: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="最高学位名称")
    is_major_graduate: Mapped[bool] = mapped_column(nullable=True, default=False, comment="是否为师范生")
    other_contact_address_details: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="其他联系方式")

