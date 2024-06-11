from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field
from datetime import date
from models.public_enum import YesOrNo, Gender, IDtype
from models.student_transaction import AuditAction
from models.students import  Relationship, Registration,HealthStatus,StudentApprovalAtatus
from typing import Optional


class StudentStatus(str, Enum):
    """
    学生状态
    """
    NEW = "new"
    CURRENT = "current"
    GRADUATE = "graduate"

    @classmethod
    def to_list(cls):
        return [cls.NEW, cls.CURRENT, cls.GRADUATE]


class NewStudents(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：student_gender
    证件类别：id_type
    证件号码：id_number
    照片：photo
    届别：session_id
    """
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field("", title="报名号", description="报名号")
    birthday: date = Field(..., title="生日", description="生日")
    student_gender: Gender = Field(..., title="性别", description="性别")
    id_type: str = Field("", title="证件类别", description="证件类别")
    id_number: str = Field("", title="证件号码", description="证件号码")
    photo: str = Field("", title="照片", description="照片")
    student_id: int = Field(0, title="", description="id")
    school_id: int = Field(0, title="", description="学校id")
    session_id: int = Field(0, title="", description="届别id")



class NewStudentsQuery(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    性别：student_gender
    证件类别：id_type
    证件号码：id_number
    学校：school
    登记时间：enrollment_date
    区县：county
    状态：status
    """
    student_name: Optional[str] = Query(None, title="学生姓名", description="学生姓名")
    enrollment_number: Optional[str] = Query(None, title="报名号", description="报名号")
    student_gender: Optional[Gender] = Query(None, title="性别", description="性别")
    id_type: Optional[str] = Query(None, title="证件类别", description="证件类别")
    id_number: Optional[str] = Query(None, title="证件号码", description="证件号码")
    school: Optional[str] = Query(None, title="学校", description="学校")
    school_id: Optional[int ] = Query(0, title="", description="学校id")
    class_id: Optional[int ] = Query(0, title="", description="班级ID")

    enrollment_date: Optional[date] = Query(None, title="登记时间", description="登记时间")
    enrollment_date_range: Optional[str] = Query(None, title="登记时间", description="登记时间区间 逗号分隔")
    county: Optional[str] = Query(None, title="区县", description="区县")
    approval_status: Optional[str] = Query(None, title="状态", description="状态")
    emporary_borrowing_status: Optional[str] = Query(None, title="", description="临时借读")
    edu_number: Optional[str] = Query(None, title="", description="学籍号")


class NewStudentsQueryRe(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    性别：student_gender
    证件类别：id_type
    证件号码：id_number
    学校：school
    登记时间：enrollment_date
    区县：county
    状态：status
    """
    student_id: int = Field(..., title="学生id", description="学生id")
    student_name: str = Field(None, title="学生姓名", description="学生姓名")
    enrollment_number: str = Field(None, title="报名号", description="报名号")
    student_gender: Gender|str = Field(None, title="性别", description="性别")
    id_type: str = Field(None, title="证件类别", description="证件类别")
    id_number: str = Field(None, title="证件号码", description="证件号码")
    school: str = Field(None, title="学校", description="学校")
    county: str = Field(None, title="区县", description="区县")
    approval_status: StudentApprovalAtatus = Field(None, title="状态", description="状态")
    block: str = Field(None, title="", description="")
    borough: str = Field(None, title="", description="")
    loc_area: str = Field(None, title="", description="")
    loc_area_pro: str = Field(None, title="", description="")
    school_name: str = Field(None, title="", description="")
    birthday: date = Field( '', title="生日", description="生日")
    photo: str = Field('', title="照片", description="照片")
    session: str = Field(None, title="", description="")
    edu_number: str = Field(None, title="", description="")
    class_name: str = Field(None, title="", description="")
    enrollment_date: str|date = Field(None, title="", description="")
    grade_name: str = Field(None, title="", description="")




class StudentsKeyinfo(BaseModel):
    """
    学生id：student_id
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    照片：photo
    """
    student_id: int = Field(None, title="学生id", description="学生id")
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field('', title="报名号", description="报名号")
    birthday: date = Field(..., title="生日", description="生日")
    student_gender: Gender = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")
    photo: str = Field('', title="照片", description="照片")


class StudentsKeyinfoDetail(BaseModel):
    """
    学生id：student_id
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    照片：photo

    """
    student_id: int = Field(None, title="学生id", description="学生id")
    student_name: str = Field('', title="学生姓名", description="学生姓名")
    enrollment_number: str = Field('', title="报名号", description="报名号")
    birthday: date = Field('', title="生日", description="生日")
    student_gender: Gender = Field('', title="性别", description="性别")
    id_type: str = Field('', title="证件类别", description="证件类别")
    id_number: str = Field('', title="证件号码", description="证件号码")
    photo: str|None = Field('', title="照片", description="照片")
    province: str|None = Field('', title=" ", description="",examples=[''],min_length=0,max_length=30)
    city: str|None = Field('', title=" ", description="",examples=[''],min_length=0,max_length=30)
    school_name: str = Field('', title="学校名称", description="学校名称",examples=['XX小学'])
    session: str = Field("", title="届别", description="届别")
    grade_name: str = Field('', title="",description="年级名称",examples=['一年级'])
    class_name: str = Field('', title="Grade_name", description="班级名称", examples=['一年级'])
    major_name: str|None = Field('', title="Grade_name",description="专业名称",examples=['农林牧鱼 '])
    block: str = Field("", title="", description="", max_length=50)
    borough: str = Field("", title="", description="", max_length=50)
    loc_area: str = Field("", title="", description="", max_length=50)
    loc_area_pro: str = Field("", title="", description="", max_length=50)



class StudentsKeyinfoChange(BaseModel):
    """
    学生id：student_id
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    照片：photo
    """
    id: int = Field(None, title="id", description="id")
    student_id: int = Field(None, title="学生id", description="学生id")
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field('', title="报名号", description="报名号")
    birthday: date = Field(..., title="生日", description="生日")
    student_gender: Gender = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")
    photo: str = Field('', title="照片", description="照片")
    approval_status: Optional[str] = Query(None, title="状态", description="状态")


class StudentsKeyinfoChangeAudit(BaseModel):
    # id:int= Query(None, title="", description="id", example='1'),
    # in_school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    # grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])
    # status: str = Field('', title="",description="状态",examples=[''])
    apply_id: int = Query(..., description="申请id", example='2')
    audit_action: AuditAction = Query(..., description="审批的操作",
                                                 example='pass')
    remark: str = Query("", description="审批的备注", min_length=0, max_length=200,
                        example='同意 无误')

class StudentsBaseInfo(BaseModel):
    """
    学生id：student_id
    姓名拼音：name_pinyin
    届别：session
    年级：grade
    班级：classroom
    班号：class_number
    学校：school
    登记日期：registration_date
    户籍地址：residence_address
    户口所在行政区：residence_district
    出生地行政区：birthplace_district
    籍贯行政区：native_place_district
    宗教信仰：religious_belief
    户口性质：residence_nature
    入学日期：enrollment_date
    联系电话：contact_number
    健康状况：health_condition
    政治面貌：political_status
    民族：ethnicity
    血型：blood_type
    家庭电话：home_phone_number
    电子信箱/其他联系方式：email_or_other_contact
    是否随迁子女：migrant_children
    是否残疾人：disabled_person
    是否独生子女：only_child
    是否留守儿童：left_behind_children
    是否流动人口：floating_population
    户口所在地（详细）：residence_address_detail
    通信地址行政区：communication_district
    邮政编码：postal_code
    通信地址：communication_address
    照片上传时间：photo_upload_time
    身份证件有效期：identity_card_validity_period
    常住地址：permanent_address
    备注：remark
    """
    student_base_id: int = Field(0, title="学生信息id", description="学生信息id")
    student_id: int = Field(..., title="学生id", description="学生id")
    grade_id: int|None = Field(0, title="", description="")
    class_id: int|None = Field(0, title="", description="")
    school_id: int|None = Field(0, title="", description="")

    name_pinyin: str = Field("", title="姓名拼音", description="姓名拼音")
    session: str = Field("", title="届别", description="届别")
    grade: str = Field("", title="年级", description="年级")
    classroom: str = Field("", title="班级", description="班级")
    class_number: str = Field("", title="班号", description="班号")
    school: str = Field("", title="学校", description="学校")
    registration_date: date = Field(date(1970, 1, 1), title="登记日期", description="登记日期")
    residence_address: str = Field("", title="户籍地址", description="户籍地址")
    residence_district: str = Field("", title="户口所在行政区", description="户口所在行政区")
    birthplace_district: str = Field("", title="出生地行政区", description="出生地行政区")
    native_place_district: str = Field("", title="籍贯行政区", description="籍贯行政区")
    religious_belief: str = Field("", title="宗教信仰", description="宗教信仰")
    residence_nature: str = Field("", title="户口性质", description="户口性质")
    enrollment_date: date = Field(date(1970, 1, 1), title="入学日期", description="入学日期")
    contact_number: str = Field("", title="联系电话", description="联系电话")
    health_condition: str = Field("", title="健康状况", description="健康状况")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    ethnicity: str = Field("", title="民族", description="民族")
    blood_type: str = Field("", title="血型", description="血型")
    home_phone_number: str = Field("", title="家庭电话", description="家庭电话")
    email_or_other_contact: str = Field("", title="电子信箱/其他联系方式", description="电子信箱/其他联系方式")
    migrant_children: YesOrNo = Field("N", title="是否随迁子女", description="是否随迁子女")
    disabled_person: YesOrNo = Field("N", title="是否残疾人", description="是否残疾人")
    only_child: str = Field("N", title="是否独生子女", description="是否独生子女")
    left_behind_children: YesOrNo = Field("N", title="是否留守儿童", description="是否留守儿童")
    floating_population: YesOrNo = Field("N", title="是否流动人口", description="是否流动人口")
    overseas_chinese: YesOrNo = Field("N", title="是否港澳台侨胞", description="是否港澳台侨胞")
    residence_address_detail: str = Field("", title="户口所在地（详细）", description="户口所在地（详细）")
    communication_district: str = Field("", title="通信地址行政区", description="通信地址行政区")
    postal_code: str = Field("", title="邮政编码", description="邮政编码")
    communication_address: str = Field("", title="通信地址", description="通信地址")
    photo_upload_time: str = Field("", title="照片上传时间", description="照片上传时间")
    identity_card_validity_period: str = Field("", title="身份证件有效期", description="身份证件有效期")
    specialty: str = Field("", title="特长", description="特长")
    permanent_address: str = Field("", title="常住地址", description="常住地址")
    remark: str = Field("", title="备注", description="备注", max_length=50)
    block: str = Field("", title="", description="", max_length=50)
    borough: str = Field("", title="", description="", max_length=50)
    loc_area: str = Field("", title="", description="", max_length=50)
    edu_number: str = Field('', title="", description="学籍号码")

    loc_area_pro: str = Field("", title="", description="", max_length=50)



class NewBaseInfoCreate(BaseModel):
    student_id: int = Field(..., title="学生id", description="学生id")
    birthplace_district: str = Field('', title="出生地", description="出生地")
    native_place_district: str = Field('', title="籍贯", description="籍贯")
    ethnicity: str = Field("", title="民族", description="民族")
    blood_type: str = Field("", title="血型", description="血型")
    health_condition: str = Field('', title="健康状况", description="健康状况")
    disabled_person: YesOrNo = Field("N", title="是否残疾人", description="是否残疾人")
    religious_belief: str = Field("", title="宗教信仰", description="宗教信仰")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    residence_address: str = Field('', title="户籍地址", description="户籍地址")
    residence_district: str = Field("", title="户口所在行政区", description="户口所在行政区")
    residence_nature: str = Field('', title="户口性质", description="户口性质")
    communication_address: str = Field("", title="通信地址", description="通信地址")
    postal_code: str = Field("", title="邮政编码", description="邮政编码")
    contact_number: str = Field("", title="联系电话", description="联系电话")
    email_or_other_contact: str = Field("", title="电子信箱/其他联系方式", description="电子信箱/其他联系方式")
    overseas_chinese: YesOrNo = Field("N", title="是否港澳台侨胞", description="是否港澳台侨胞")
    left_behind_children: YesOrNo = Field("N", title="是否留守儿童", description="是否留守儿童")
    migrant_children: YesOrNo = Field("N", title="是否随迁子女", description="是否随迁子女")
    floating_population: YesOrNo = Field("N", title="是否流动人口", description="是否流动人口")
    only_child: YesOrNo = Field("N", title="是否独生子女", description="是否独生子女")
    residence_address_detail: str = Field("", title="户口所在地（详细）", description="户口所在地（详细）")
    identity_card_validity_period: str = Field("", title="身份证件有效期", description="身份证件有效期")
    specialty: str = Field("", title="特长", description="特长")
    permanent_address: str = Field("", title="常住地址", description="常住地址")
    school_id: int = Field(0, title="学校id", description="学校id")
    session_id: int = Field(0, title="", description="届别id")
    registration_date: date = Field(date(1970, 1, 1), title="登记日期", description="登记日期")



class NewBaseInfoUpdate(BaseModel):
    student_base_id: int = Field(..., title="学生信息id", description="学生信息id")
    student_id: int = Field(..., title="学生id", description="学生id")
    birthplace_district: str = Field(..., title="出生地", description="出生地")
    native_place_district: str = Field(..., title="籍贯", description="籍贯")
    ethnicity: str = Field("", title="民族", description="民族")
    blood_type: str = Field("", title="血型", description="血型")
    health_condition: str = Field(..., title="健康状况", description="健康状况")
    disabled_person: YesOrNo = Field("N", title="是否残疾人", description="是否残疾人")
    religious_belief: str = Field("", title="宗教信仰", description="宗教信仰")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    residence_address: str = Field(..., title="户籍地址", description="户籍地址")
    residence_district: str = Field("", title="户口所在行政区", description="户口所在行政区")
    residence_nature: str = Field(..., title="户口性质", description="户口性质")
    communication_address: str = Field("", title="通信地址", description="通信地址")
    postal_code: str = Field("", title="邮政编码", description="邮政编码")
    contact_number: str = Field("", title="联系电话", description="联系电话")
    email_or_other_contact: str = Field("", title="电子信箱/其他联系方式", description="电子信箱/其他联系方式")
    overseas_chinese: YesOrNo = Field("N", title="是否港澳台侨胞", description="是否港澳台侨胞")
    left_behind_children: YesOrNo = Field("N", title="是否留守儿童", description="是否留守儿童")
    migrant_children: YesOrNo = Field("N", title="是否随迁子女", description="是否随迁子女")
    floating_population: YesOrNo = Field("N", title="是否流动人口", description="是否流动人口")
    only_child: YesOrNo = Field("N", title="是否独生子女", description="是否独生子女")
    residence_address_detail: str = Field("", title="户口所在地（详细）", description="户口所在地（详细）")
    identity_card_validity_period: str = Field("", title="身份证件有效期", description="身份证件有效期")
    specialty: str = Field("", title="特长", description="特长")
    permanent_address: str = Field("", title="常住地址", description="常住地址")


# 学生家庭成员信息模型
class StudentsFamilyInfo(BaseModel):
    """
    家庭成员id：student_family_info_id
    学生id：student_id
    姓名：name
    性别：gender
    关系：relationship
    是否监护人：is_guardian
    证件类型：identification_type
    证件号码：identification_number
    出生日期：birthday
    手机号码：phone_number
    民族：ethnicity
    健康状态：health_status
    国籍：nationality
    政治面貌：political_status
    联系地址：contact_address
    工作单位：workplace
    家庭成员职业：family_member_occupation
    """
    student_family_info_id: int = Field(..., title="家庭成员id", description="家庭成员id")
    student_id: int = Field(..., title="学生id", description="学生id")
    name: str = Field(..., title="姓名", description="姓名")
    gender: Gender = Field(..., title="性别", description="性别")
    relationship: Relationship = Field(..., title="关系", description="关系")
    is_guardian: YesOrNo = Field(..., title="是否监护人", description="是否监护人")
    identification_type: str = Field(..., title="证件类型", description="证件类型")
    identification_number: str = Field(..., title="证件号码", description="证件号码")
    birthday: date = Field(..., title="出生日期", description="出生日期")
    phone_number: str = Field(..., title="手机号码", description="手机号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    health_status: HealthStatus = Field(..., title="健康状态", description="健康状态")
    nationality: str = Field(..., title="国籍", description="国籍")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    contact_address: str = Field(..., title="联系地址", description="联系地址")
    workplace: str = Field("", title="工作单位", description="工作单位")
    family_member_occupation: str = Field("", title="家庭成员职业", description="家庭成员职业")


class StudentsFamilyInfoCreate(BaseModel):
    """
    家庭成员id：student_family_info_id
    学生id：student_id
    姓名：name
    性别：gender
    关系：relationship
    是否监护人：is_guardian
    证件类型：identification_type
    证件号码：identification_number
    出生日期：birthday
    手机号码：phone_number
    民族：ethnicity
    健康状态：health_status
    国籍：nationality
    政治面貌：political_status
    联系地址：contact_address
    工作单位：workplace
    家庭成员职业：family_member_occupation
    """
    student_id: int = Field(..., title="学生id", description="学生id")
    name: str = Field(..., title="姓名", description="姓名")
    gender: Gender = Field(..., title="性别", description="性别")
    relationship: Relationship = Field(..., title="关系", description="关系")
    is_guardian: YesOrNo = Field(..., title="是否监护人", description="是否监护人")
    identification_type: str = Field(..., title="证件类型", description="证件类型")
    identification_number: str = Field(..., title="证件号码", description="证件号码")
    birthday: date = Field(..., title="出生日期", description="出生日期")
    phone_number: str = Field(..., title="手机号码", description="手机号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    health_status: HealthStatus = Field(..., title="健康状态", description="健康状态")
    nationality: str = Field(..., title="国籍", description="国籍")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    contact_address: str = Field(..., title="联系地址", description="联系地址")
    workplace: str = Field("", title="工作单位", description="工作单位")
    family_member_occupation: str = Field("", title="家庭成员职业", description="家庭成员职业")


class StudentsUpdateFamilyInfo(BaseModel):
    """
    姓名：name
    性别：gender
    关系：relationship
    是否监护人：is_guardian
    证件类型：identification_type
    证件号码：identification_number
    出生日期：birthday
    手机号码：phone_number
    民族：ethnicity
    健康状态：health_status
    国籍：nationality
    政治面貌：political_status
    联系地址：contact_address
    工作单位：workplace
    家庭成员职业：family_member_occupation
    """
    student_family_info_id: int = Field(..., title="家庭成员id", description="家庭成员id")
    student_id: int = Field(..., title="学生id", description="学生id")
    name: str = Field(..., title="姓名", description="姓名")
    gender: Gender = Field(..., title="性别", description="性别")
    relationship: Relationship = Field(..., title="关系", description="关系")
    is_guardian: YesOrNo = Field(..., title="是否监护人", description="是否监护人")
    identification_type: str = Field(..., title="证件类型", description="证件类型")
    identification_number: str = Field(..., title="证件号码", description="证件号码")
    birthday: date = Field(..., title="出生日期", description="出生日期")
    phone_number: str = Field(..., title="手机号码", description="手机号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    health_status: HealthStatus = Field(..., title="健康状态", description="健康状态")
    nationality: str = Field(..., title="国籍", description="国籍")
    political_status: str = Field("", title="政治面貌", description="政治面貌")
    contact_address: str = Field(..., title="联系地址", description="联系地址")
    workplace: str = Field("", title="工作单位", description="工作单位")
    family_member_occupation: str = Field("", title="家庭成员职业", description="家庭成员职业")






class GraduationStudents(BaseModel):
    """
    状态 毕业      行政属地
    graduation_type: Mapped[str] = mapped_column(String(10), nullable=True, default='', comment="毕业类型")
    borough: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政管辖区")


    """
    id: int = Query(0, title="", description="id", example='1'),

    student_id: int = Field(0, title="学生id", description="学生id", examples=['0'])
    graduation_type: str = Field('', title="状态", description="状态")
    student_name: str = Field('', title="学生姓名", description="学生姓名")
    student_gender: str = Field('', title="性别", description="性别")
    school_name: str = Field('', title="学校", description="学校")
    borough: str = Field('', title="", description="行政属地")
    edu_number: str = Field('', title="", description="学籍号码")
    class_id: int = Field(0, title="", description="班级")
    class_name: str = Field('', title="", description="班级名称")


#



class NewStudentsFlowOut(BaseModel):
    student_id: int = Query(..., description="学生id", examples=["1"]),
    flow_out_time: str = Query(..., description="流出时间", min_length=1, max_length=20, examples=["2020-10-10"]),
    flow_out_reason: str = Query('', description="流出原因", min_length=1, max_length=20, examples=["家庭搬迁"]),


class StudentSession(BaseModel):
    session_id: int = Query(0, description="届别id",   examples=["1234567890"]),
    session_name: str = Query(..., description="届别名称", min_length=1, max_length=20, examples=["2020级"]),
    session_alias: str = Query(..., description="届别别名", min_length=1, max_length=20, examples=["2020届别"]),
    session_status: str = Query(..., description="届别状态", min_length=1, max_length=20, examples=["开"])


class NewStudentTransferIn(BaseModel):
    """
    student_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生姓名")
    student_gender: Mapped[str] = mapped_column(String(64), nullable=False, comment="学生性别")
    enrollment_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="报名号")
    birthday: Mapped[str] = mapped_column(String(30), nullable=False, comment="生日",default='')
    gender: Mapped[str] = mapped_column(String(64), nullable=True, comment="性别")
    id_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件类别")
    id_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="证件号码")
    photo: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片") #图像处理再定
    # deleted: Mapped[int] = mapped_column(nullable=True, comment="删除态", default=0)
    approval_status: Mapped[str] = mapped_column(String(64), nullable=False, comment="状态",default="分班")
    """

    student_name: str = Field('', title="学生姓名", description="学生姓名")
    enrollment_number: str = Field('', title="报名号", description="报名号")
    birthday: date  = Field('', title="生日", description="生日")
    student_gender: str = Field('', title="性别", description="性别")
    id_type: str = Field('', title="证件类别", description="证件类别")
    id_number: str = Field("", title="证件号码", description="证件号码")
    ethnicity: str = Field("", title="民族", description="民族")
    # natural_edu_no: str = Query('',   description="国家学籍号码",min_length=1,max_length=20,examples=["DF23321312"]),
    edu_number: str = Field('', title="", description="学籍号码", examples=["DF23321312"])
    residence_address_detail: str = Field("", title="户口所在地（详细）", description="户口所在地（详细）")
    residence_district: str = Field('', title="户口所在行政区", description="户口所在行政区")
    student_id: int = Query(0, title="", description="id", example='1'),

class StudentGraduation(BaseModel):
    student_id: int = Query(0, title="", description="学生id", example= 1),
    graduation_type: str = Query('', description="毕业类型",   max_length=20, examples=[""]),
    graduation_remarks: str = Query('', description="毕业备注",   max_length=200, examples=[""]),
    credential_notes: str = Query('', description="制证备注",  max_length=200, examples=[""])
    graduation_photo: str = Query('', description="毕业照",   max_length=200, examples=[""])
class NewStudentTask(BaseModel):
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])