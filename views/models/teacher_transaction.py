from pydantic import BaseModel, Field
from datetime import date, datetime


class TeacherTransactionModel(BaseModel):
    """
    异动类型：transfer_type
    异动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    transfer_type: str = Field(..., title="异动类型", description="异动类型")
    transfer_reason: str = Field(..., title="异动原因", description="异动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")


class TeacherTransactionUpdateModel(BaseModel):
    """
    teacher_transaction：teacher_transaction_id
    异动类型：transfer_type
    异动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    teacher_transaction_id: int = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transfer_type: str = Field(..., title="异动类型", description="异动类型")
    transfer_reason: str = Field(..., title="异动原因", description="异动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: date = Field(..., title="操作时间", description="操作时间")

class TeacherTransactionQuery(BaseModel):
    """
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    """
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")

class TeacherTransactionQueryRe(BaseModel):
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: str = Field(..., title="性别", description="性别")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_number: str = Field(..., title="教师编号", description="教师编号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")





class TransferDetailsModel(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field(..., title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: date = Field(..., title="操作时间", description="操作时间")


class TransferDetailsUpdateModel(BaseModel):
    """
    transfer_details：transfer_details_id
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    transfer_details_id: int = Field(..., title="transfer_details_id", description="transfer_details_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field(..., title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
