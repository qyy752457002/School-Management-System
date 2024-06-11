from pydantic import BaseModel, Field
from datetime import date


class TeacherBorrowModel(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    借动类型：borrow_type
    借动原因：borrow_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field(..., title="现行政属地", description="现行政属地")
    borrow_type: str = Field(..., title="借动类型", description="借动类型")
    borrow_reason: str = Field(..., title="借动原因", description="借动原因")
    remark: str = Field(..., title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: date = Field(..., title="操作时间", description="操作时间")


class TeacherBorrowUpdateModel(BaseModel):
    """
    teacher_borrow：teacher_borrow_id
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    借动类型：borrow_type
    借动原因：borrow_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    teacher_borrow_id: int = Field(..., title="teacher_borrow_id", description="teacher_borrow_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field(..., title="现行政属地", description="现行政属地")
    borrow_type: str = Field(..., title="借动类型", description="借动类型")
    borrow_reason: str = Field(..., title="借动原因", description="借动原因")
    remark: str = Field(..., title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: date = Field(..., title="操作时间", description="操作时间")
