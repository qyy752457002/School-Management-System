from pydantic import BaseModel, Field
from datetime import date

class TeacherChangeModel(BaseModel):
    """
    变更ID：change_id
    教师ID：teacher_id
    操作人ID：operator_id
    操作人姓名：operator_name
    变更模块：change_module
    变更时间：change_time
    变更字段：changed_field
    变更前：before_change
    变更后：after_change
    操作时间：operation_time
    """
    change_id: str = Field(..., title="变更ID", description="变更ID")
    teacher_id: str = Field(..., title="教师ID", description="教师ID")
    operator_id: str = Field(..., title="操作人ID", description="操作人ID")
    operator_name: str = Field(..., title="操作人姓名", description="操作人姓名")
    change_module: str = Field(..., title="变更模块", description="变更模块")
    change_time: str = Field(..., title="变更时间", description="变更时间")
    changed_field: str = Field(..., title="变更字段", description="变更字段")
    before_change: str = Field(..., title="变更前", description="变更前")
    after_change: str = Field(..., title="变更后", description="变更后")
    operation_time: str = Field(..., title="操作时间", description="操作时间")
    
    


class TeacherChangeUpdateModel(BaseModel):
    """
    teacher_change：teacher_change_id
    变更ID：change_id
    教师ID：teacher_id
    操作人ID：operator_id
    操作人姓名：operator_name
    变更模块：change_module
    变更时间：change_time
    变更字段：changed_field
    变更前：before_change
    变更后：after_change
    操作时间：operation_time
    """
    teacher_change_id: int = Field(..., title="teacher_change_id", description="teacher_change_id")
    change_id: str = Field(..., title="变更ID", description="变更ID")
    teacher_id: str = Field(..., title="教师ID", description="教师ID")
    operator_id: str = Field(..., title="操作人ID", description="操作人ID")
    operator_name: str = Field(..., title="操作人姓名", description="操作人姓名")
    change_module: str = Field(..., title="变更模块", description="变更模块")
    change_time: str = Field(..., title="变更时间", description="变更时间")
    changed_field: str = Field(..., title="变更字段", description="变更字段")
    before_change: str = Field(..., title="变更前", description="变更前")
    after_change: str = Field(..., title="变更后", description="变更后")
    operation_time: str = Field(..., title="操作时间", description="操作时间")
    
    


