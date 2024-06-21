from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

from enum import Enum


class TeacherChangeModule(str, Enum):
    """
    新入职：new_entry
    基本信息变更：basic_info_change
    关键信息变更：key_info_change
    调动：transfer
    变动：transaction
    借动：borrow
    离退休：retirement
    """
    NEW_ENTRY = "new_entry"
    BASIC_INFO_CHANGE = "basic_info_change"
    KEY_INFO_CHANGE = "key_info_change"
    TRANSFER = "transfer"
    TRANSACTION = "transaction"
    BORROW = "borrow"
    RETIREMENT = "retirement"

    @classmethod
    def to_list(cls):
        return [cls.NEW_ENTRY, cls.BASIC_INFO_CHANGE, cls.KEY_INFO_CHANGE, cls.TRANSFER, cls.TRANSACTION, cls.BORROW,
                cls.RETIREMENT]


class TeacherChangeLogModel(BaseModel):
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

    teacher_id: str = Field(..., title="教师ID", description="教师ID")
    change_module: TeacherChangeModule = Field(..., title="变更模块", description="变更模块")
    change_detail: str = Field(..., title="变更详情", description="变更详情")
    log_status: Optional[str] = Field(..., title="日志状态", description="日志状态")
    process_instance_id: int = Field(..., title="流程ID", description="流程ID")
    # apply_name: Optional[str] = Field(..., title="申请人", description="申请人")
    # approval_name: str = Field(..., title="审核人", description="审核人")
    # apply_time: Optional[datetime] = Field(None, title="申请时间", description="申请时间")
    # approval_time: Optional[datetime] = Field(None, title="审核时间", description="审核时间")


class TeacherChangeLogReModel(TeacherChangeLogModel):
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


class TeacherChangeDetailModel(BaseModel):
    teacher_change_id: int = Field(..., title="teacher_change_id", description="teacher_change_id")
    teacher_id: str = Field(..., title="教师ID", description="教师ID")
    change_module: TeacherChangeModule = Field(..., title="变更模块", description="变更模块")
    changed_field: str = Field(..., title="变更字段", description="变更字段")
    before_change: str = Field(..., title="变更前", description="变更前")
    after_change: str = Field(..., title="变更后", description="变更后")


class TeacherChangeDetailReModel(TeacherChangeDetailModel):
    teacher_change_detail_id: int = Field(..., title="teacher_change_detail_id", description="teacher_change_detail_id")
