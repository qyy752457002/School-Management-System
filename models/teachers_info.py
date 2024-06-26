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
    unemploy_time: Mapped[date] = mapped_column(Date, nullable=True, comment="非在职时间")
    unemploy_action_time = mapped_column(DateTime,default=datetime.now, nullable=True, comment="离退休操作时间")
    unemploy_number: Mapped[str] = mapped_column(String(255), nullable=True, default="", comment="离退休证号")

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
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="submitting")
    org_id: Mapped[int] = mapped_column(INT, nullable=True, default=0, comment="机构ID")

