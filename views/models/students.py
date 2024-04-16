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
    enrollment_number: str = Field(..., title="报名号", description="报名号")
    birthday: str = Field(..., title="生日", description="生日")
    gender: str = Field(..., title="性别", description="性别")
    id_type: str = Field(..., title="证件类别", description="证件类别")
    id_number: str = Field(..., title="证件号码", description="证件号码")

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
