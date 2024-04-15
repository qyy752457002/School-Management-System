from datetime import date

from pydantic import BaseModel, Field


class Teachers(BaseModel):
    """
    姓名：teacher_name
    性别：teacher_gender
    证件类型：teacher_id_type
    证件号：teacher_id_number
    出生日期：teacher_date_of_birth
    任职单位：teacher_employer
    头像：teacher_avatar
    审批状态：teacher_approval_status
    """
    teacher_name: str = Field(..., title="教师名称", description="教师名称")
    teacher_gender: str = Field(..., title="教师性别", description="教师性别")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: str = Field(..., title="任职单位", description="任职单位")
    teacher_avatar: str = Field(..., title="头像", description="头像")
    teacher_approval_status: str = Field(..., title="审批状态", description="审批状态")

    class Config:
        schema_extra = {
            "example": {
                "teacher_name": "张三",
                "teacher_gender": "男",
                "teacher_id_type": "身份证",
                "teacher_id_number": "123456789012345678",
                "teacher_date_of_birth": "1990-01-01",
                "teacher_employer": "xx学校",
                "teacher_avatar": "http://www.baidu.com",
                "teacher_approval_status": "通过"
            }
        }
