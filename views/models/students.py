from pydantic import BaseModel, Field
from datetime import date


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

    class Config:
        schema_extra = {
            "example": {
                "student_name": "John Doe",
                "enrollment_number": "20220001",
                "birthday": "2000-01-01 00:00:00",
                "gender": "Male",
                "id_type": "ID Card",
                "id_number": "12345678",
            }
        }


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

    class Config:
        schema_extra = {
            "example": {
                "student_name": "John Doe",
                "enrollment_number": "20220001",
                "gender": "Male",
                "id_type": "ID Card",
                "id_number": "12345678",
                "school": "清华",
                "enrollment_date": "2000-01-01 00:00:00",
                "county": "朝阳区",
                "status": "流出",
            }
        }


class StudentsKeyinfo(BaseModel):
    """
    学生姓名：student_name
    报名号：enrollment_number
    生日：birthday
    性别：gender
    证件类别：id_type
    证件号码：id_number
    民族：ethnicity
    照片：photo
    """
    student_name: str = Field(..., title="学生姓名", description="学生姓名")
    enrollment_number: str = Field(..., title="报名号", description="报名号")
    birthday: str = Field(..., title="生日", description="生日")
    gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")
    ethnicity: str = Field(..., title="民族", description="民族")
    photo: str = Field(..., title="照片", description="照片")

    class Config:
        schema_extra = {
            "example": {
                "student_name": "John Doe",
                "enrollment_number": "20220001",
                "birthday": "2000-01-01 00:00:00",
                "gender": "Male",
                "id_type": "ID Card",
                "id_number": "12345678",
                "ethnicity": "Han",
                "photo": "photo.jpg",
            }
        }



class StudentsBaseInfo(BaseModel):
    """
    姓名拼音：name_pinyin
    届别：session
    年级：grade
    班级：classroom
    班号：class_number
    学校：school
    登记日期：registration_date
    户口所在行政区：residence_district
    出生地行政区：birthplace_district
    籍贯行政区：native_place_district
    宗教信仰：religious_belief
    户口性质：residence_nature
    入学日期：enrollment_date
    联系电话：contact_number
    健康状况：health_condition
    政治面貌：political_status
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
    备注：remark
    """
    name_pinyin: str = Field(..., title="姓名拼音", description="姓名拼音")
    session: str = Field(..., title="届别", description="届别")
    grade: str = Field(..., title="年级", description="年级")
    classroom: str = Field(..., title="班级", description="班级")
    class_number: str = Field(..., title="班号", description="班号")
    school: str = Field(..., title="学校", description="学校")
    registration_date: str = Field(..., title="登记日期", description="登记日期")
    residence_district: str = Field(..., title="户口所在行政区", description="户口所在行政区")
    birthplace_district: str = Field(..., title="出生地行政区", description="出生地行政区")
    native_place_district: str = Field(..., title="籍贯行政区", description="籍贯行政区")
    religious_belief: str = Field(..., title="宗教信仰", description="宗教信仰")
    residence_nature: str = Field(..., title="户口性质", description="户口性质")
    enrollment_date: str = Field(..., title="入学日期", description="入学日期")
    contact_number: str = Field(..., title="联系电话", description="联系电话")
    health_condition: str = Field(..., title="健康状况", description="健康状况")
    political_status: str = Field(..., title="政治面貌", description="政治面貌")
    blood_type: str = Field(..., title="血型", description="血型")
    home_phone_number: str = Field(..., title="家庭电话", description="家庭电话")
    email_or_other_contact: str = Field(..., title="电子信箱/其他联系方式", description="电子信箱/其他联系方式")
    migrant_children: bool = Field(..., title="是否随迁子女", description="是否随迁子女")
    disabled_person: bool = Field(..., title="是否残疾人", description="是否残疾人")
    only_child: bool = Field(..., title="是否独生子女", description="是否独生子女")
    left_behind_children: bool = Field(..., title="是否留守儿童", description="是否留守儿童")
    floating_population: bool = Field(..., title="是否流动人口", description="是否流动人口")
    residence_address_detail: str = Field(..., title="户口所在地（详细）", description="户口所在地（详细）")
    communication_district: str = Field(..., title="通信地址行政区", description="通信地址行政区")
    postal_code: str = Field(..., title="邮政编码", description="邮政编码")
    communication_address: str = Field(..., title="通信地址", description="通信地址")
    photo_upload_time: str = Field(..., title="照片上传时间", description="照片上传时间")
    identity_card_validity_period: str = Field(..., title="身份证件有效期", description="身份证件有效期")
    remark: str = Field(..., title="备注", description="备注")

    class Config:
        schema_extra = {
            "example": {
                "name_pinyin": "john_doe",
                "session": "2022",
                "grade": "10",
                "classroom": "A",
                "class_number": "1",
                "school": "ABC School",
                "registration_date": "2024-04-16 00:00:00",
                "residence_district": "Beijing",
                "birthplace_district": "Shanghai",
                "native_place_district": "Shanxi",
                "religious_belief": "Christian",
                "residence_nature": "Urban",
                "enrollment_date": "2023-09-01 00:00:00",
                "contact_number": "12345678901",
                "health_condition": "Good",
                "political_status": "Party Member",
                "blood_type": "O",
                "home_phone_number": "1234567890",
                "email_or_other_contact": "johndoe@example.com",
                "migrant_children": "1",
                "disabled_person": "False",
                "only_child": "1",
                "left_behind_children": "False",
                "floating_population": "False",
                "residence_address_detail": "123 Main Street, Beijing",
                "communication_district": "Beijing",
                "postal_code": "100000",
                "communication_address": "123 Main Street, Beijing",
                "photo_upload_time": "2024-04-16 00:00:00",
                "identity_card_validity_period": "2024-04-16 to 2034-04-16",
                "remark": "This is a remark",
            }
        }


