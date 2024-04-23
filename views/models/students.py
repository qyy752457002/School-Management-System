from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field
from datetime import date



class StudentStatus(str, Enum):
    """
    学生装态
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
    性别：gender
    证件类别：id_type
    证件号码：id_number
    """
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field(None, title="报名号", description="报名号")
    birthday: str = Field(..., title="生日", description="生日")
    gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(None, title="证件类别", description="证件类别")
    id_number: str = Field(None, title="证件号码", description="证件号码")


class NewStudentsQuery(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    性别：gender
    证件类别：id_type
    证件号码：id_number
    学校：school
    登记时间：enrollment_date
    区县：county
    状态：status
    """
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field(..., title="报名号", description="报名号")
    gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")
    school: str = Field(..., title="学校", description="学校")
    enrollment_date: date = Field(..., title="登记时间", description="登记时间")
    county: str = Field(..., title="区县", description="区县")
    status: str = Field(..., title="状态", description="状态")


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
    enrollment_number: str = Field(..., title="报名号", description="报名号")
    birthday: str = Field(..., title="生日", description="生日")
    student_gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")
    photo: str = Field(..., title="照片", description="照片")


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
    student_id: int = Field(0, title="学生id", description="学生id")
    name_pinyin: str = Field(..., title="姓名拼音", description="姓名拼音")
    session: str = Field(..., title="届别", description="届别")
    grade: str = Field(..., title="年级", description="年级")
    classroom: str = Field(..., title="班级", description="班级")
    class_number: str = Field(..., title="班号", description="班号")
    school: str = Field(..., title="学校", description="学校")
    registration_date: str = Field(..., title="登记日期", description="登记日期")
    residence_address: str = Field(..., title="户籍地址", description="户籍地址")
    residence_district: str = Field(..., title="户口所在行政区", description="户口所在行政区")
    birthplace_district: str = Field(..., title="出生地行政区", description="出生地行政区")
    native_place_district: str = Field(..., title="籍贯行政区", description="籍贯行政区")
    religious_belief: str = Field(None, title="宗教信仰", description="宗教信仰")
    residence_nature: str = Field(..., title="户口性质", description="户口性质")
    enrollment_date: str = Field(..., title="入学日期", description="入学日期")
    contact_number: str = Field(..., title="联系电话", description="联系电话")
    health_condition: str = Field(..., title="健康状况", description="健康状况")
    political_status: str = Field(None, title="政治面貌", description="政治面貌")
    ethnicity: str = Field(None, title="民族", description="民族")
    blood_type: str = Field(None, title="血型", description="血型")
    home_phone_number: str = Field(..., title="家庭电话", description="家庭电话")
    email_or_other_contact: str = Field(..., title="电子信箱/其他联系方式", description="电子信箱/其他联系方式")
    migrant_children: str = Field(..., title="是否随迁子女", description="是否随迁子女")
    disabled_person: str = Field(None, title="是否残疾人", description="是否残疾人")
    only_child: str = Field(..., title="是否独生子女", description="是否独生子女")
    left_behind_children: str = Field(..., title="是否留守儿童", description="是否留守儿童")
    floating_population: str = Field(..., title="是否流动人口", description="是否流动人口")
    overseas_chinese: str = Field(..., title="是否港澳台侨胞", description="是否港澳台侨胞")
    residence_address_detail: str = Field(None, title="户口所在地（详细）", description="户口所在地（详细）")
    communication_district: str = Field(..., title="通信地址行政区", description="通信地址行政区")
    postal_code: str = Field(None, title="邮政编码", description="邮政编码")
    communication_address: str = Field(None, title="通信地址", description="通信地址")
    photo_upload_time: str = Field(..., title="照片上传时间", description="照片上传时间")
    identity_card_validity_period: str = Field(..., title="身份证件有效期", description="身份证件有效期")
    specialty: str = Field(None, title="特长", description="特长")
    permanent_address: str = Field(None, title="常住地址", description="常住地址")
    remark: str = Field(None, title="备注", description="备注", max_length=50)



#学生家庭成员信息模型
class StudentsFamilyInfo(BaseModel):
    """
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
    gender: str = Field(..., title="性别", description="性别")
    relationship: str = Field(..., title="关系", description="关系")
    is_guardian: bool = Field(..., title="是否监护人", description="是否监护人")
    identification_type: str = Field(..., title="证件类型", description="证件类型")
    identification_number: str = Field(..., title="证件号码", description="证件号码")
    birthday: str = Field(..., title="出生日期", description="出生日期")
    phone_number: str = Field(..., title="手机号码", description="手机号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    health_status: str = Field(..., title="健康状态", description="健康状态")
    nationality: str = Field(..., title="国籍", description="国籍")
    political_status: str = Field(..., title="政治面貌", description="政治面貌")
    contact_address: str = Field(..., title="联系地址", description="联系地址")
    workplace: str = Field(..., title="工作单位", description="工作单位")
    family_member_occupation: str = Field(..., title="家庭成员职业", description="家庭成员职业")

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
    name: str = Field(..., title="姓名", description="姓名")
    gender: str = Field(..., title="性别", description="性别")
    relationship: str = Field(..., title="关系", description="关系")
    is_guardian: bool = Field(..., title="是否监护人", description="是否监护人")
    identification_type: str = Field(..., title="证件类型", description="证件类型")
    identification_number: str = Field(..., title="证件号码", description="证件号码")
    birthday: str = Field(..., title="出生日期", description="出生日期")
    phone_number: str = Field(..., title="手机号码", description="手机号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    health_status: str = Field(..., title="健康状态", description="健康状态")
    nationality: str = Field(..., title="国籍", description="国籍")
    political_status: str = Field(..., title="政治面貌", description="政治面貌")
    contact_address: str = Field(..., title="联系地址", description="联系地址")
    workplace: str = Field(..., title="工作单位", description="工作单位")
    family_member_occupation: str = Field(..., title="家庭成员职业", description="家庭成员职业")




class StudentEduInfo(BaseModel):
    student_id: int = Query(...,   description="学生id",min_length=1,max_length=20,examples=["1"],example="1"),
    province_id: str = Query(...,   description="省份",min_length=1,max_length=20,examples=["13000"],example="13000"),
    city_id: str = Query(...,   description="市",min_length=1,max_length=20,examples=["142323"]),
    area_id: str = Query(...,   description="区",min_length=1,max_length=20,examples=["1522000"]),
    district_id: str = Query(...,   description="区县",min_length=1,max_length=20,examples=["1622222"]),
    transfer_in_type: str = Query("",   description="转入类型",min_length=1,max_length=20,examples=["指定日期转入"]),
    natural_edu_no: str = Query("",   description="国家学籍号码",min_length=1,max_length=20,examples=["DF23321312"]),
    school_id: int  = Query(..., title="", description="学校ID",examples=["102"])
    school_name: str = Query(..., title="", description="学校名称",examples=["XXxiaoxue"])
    session: str = Query(..., title="", description="届别",examples=["2003"])
    attached_class: str = Query("", title="", description="附设班",examples=["3班"])
    grade_id: str = Query(..., title="", description="年级ID",examples=["102"])
    grade_name: str = Query(..., title="", description="年级",examples=["2年级"])
    class_id: str = Query(..., title="", description="班级id",examples=["125"])
    classes: str = Query(..., title="", description="班级",examples=["二2班"])
    major_id: str = Query(..., title="", description="专业",examples=["农业"])
    transferin_time:str= Query("", description="转入时间" ,min_length=1,max_length=20,examples=["2020-10-10"]),
    transferin_reason:str= Query("", description="转入原因" ,min_length=1,max_length=20,examples=["家庭搬迁..."]),
    status:str= Query('', description="" ,min_length=1,max_length=20,examples=["..."]),
    doc_upload: str = Field('',   description=" 附件",examples=[''])





class GraduationStudents(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),

    student_id: str = Field('', title="学生id", description="学生id",examples=['0'])
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    gender: str = Field(..., title="性别", description="性别")
    school: str = Field(..., title="学校", description="学校")
    county: str = Field(..., title="", description="行政属地")
    edu_number: str = Field(..., title="", description="学籍号码")
    class_id: str = Field(..., title="", description="班级")

class NewStudentsFlowOut(BaseModel):
    student_id: int = Query(...,   description="学生id", examples=["1"]),
    flow_out_time: str = Query(...,   description="流出时间",min_length=1,max_length=20,examples=["2020-10-10"]),
    flow_out_reason: str = Query(None,   description="流出原因",min_length=1,max_length=20,examples=["家庭搬迁"]),

class StudentSession(BaseModel):
    session_id: str = Query(...,   description="届别id",min_length=1,max_length=20,examples=["1234567890"]),
    session_name: str = Query(...,   description="届别名称",min_length=1,max_length=20,examples=["2020级"]),
    session_alias: str = Query(...,   description="届别别名",min_length=1,max_length=20,examples=["2020届别"]),
    session_status: str = Query(...,   description="届别状态",min_length=1,max_length=20,examples=["开"])



class NewStudentTransferIn(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    """
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field(None, title="报名号", description="报名号")
    birthday: str = Field(..., title="生日", description="生日")
    gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(None, title="证件类别", description="证件类别")
    id_number: str = Field(None, title="证件号码", description="证件号码")
    ethnicity: str = Field(None, title="民族", description="民族")
    # natural_edu_no: str = Query(...,   description="国家学籍号码",min_length=1,max_length=20,examples=["DF23321312"]),
    edu_number: str = Field(..., title="", description="学籍号码",examples=["DF23321312"])
    residence_address_detail: str = Field(None, title="户口所在地（详细）", description="户口所在地（详细）")
    residence_district: str = Field(..., title="户口所在行政区", description="户口所在行政区")



