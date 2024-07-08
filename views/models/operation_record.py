from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class OperationTarget(str, Enum):
    """
    操作主体类型

    """
    PLANNING_SCHOOL = "planning_school"
    SCHOOL = "school"
    INSTITUTION = "institution"
    CAMPUS = "campus"

    TEACHER = "teacher"
    STUDENT = "student"

    @classmethod
    def to_list(cls):
        return [cls.PLANNING_SCHOOL, cls.SCHOOL, cls.CAMPUS, cls.TEACHER, cls.STUDENT, cls.INSTITUTION]


class OperationType(str, Enum):
    """
    操作类型-页面的操作 对象

    """
    CREATE = "创建"
    MODIFY = "修改"
    DELETE = "删除"

    @classmethod
    def to_list(cls):
        return [cls.CREATE, cls.DELETE, cls.MODIFY, ]


class ChangeModule(str, Enum):
    """
    操作模块
    创建学校：create_school
    关闭学校：close_school
    入职：new_entry
    基本信息变更：basic_info_change
    关键信息变更：key_info_change
    家庭成员信息变更：family_info_change
    调动：transfer
    变动：transaction
    借动：borrow
    离退休：retirement
    转学：student_transaction
    """
    CREATE_SCHOOL = "create_school"
    CLOSE_SCHOOL = "close_school"
    NEW_ENTRY = "new_entry"
    BASIC_INFO_CHANGE = "basic_info_change"
    KEY_INFO_CHANGE = "key_info_change"
    FAMILY_INFO_CHANGE = "family_info_change"
    TRANSFER = "transfer"
    TRANSACTION = "transaction"
    BORROW = "borrow"
    RETIREMENT = "retirement"
    STUDENT_TRANSACTION = "student_transaction"

    @classmethod
    def to_list(cls):
        return [cls.CREATE_SCHOOL, cls.NEW_ENTRY, cls.BASIC_INFO_CHANGE, cls.KEY_INFO_CHANGE,
                cls.TRANSFER, cls.TRANSACTION, cls.BORROW,
                cls.RETIREMENT]


class OperationRecord(BaseModel):
    action_target_id: int = Field(..., title="操作对象ID", description="操作对象ID", examples=[''])
    target: OperationTarget = Field(..., description=" 操作对象", examples=[''])
    action_type: str = Field(..., title="操作类型", description="操作类型", examples=[''])
    ip: str = Field('', title=" Description", description="操作IP", examples=[''])
    change_data: Optional[str] = Field("", title=" Author", description="变更前后数据", examples=[''])
    operation_time: datetime = Field(datetime.now(), description="操作时间", examples=[''])
    doc_upload: str = Field('', description=" 附件", examples=[''])
    change_module: ChangeModule = Field(..., description=" 变更模块", examples=[''])
    change_detail: str = Field(..., description=" 变更详情", examples=[''])
    status: str = Field('', description=" 状态", examples=[''])
    operator_name: str = Field('', description=" 操作账号", examples=[''])
    operator_id: int = Field(0, description=" 操作人", examples=[''])
    process_instance_id: Optional[int | str] = Field(None, description="流程ID", examples=[''])
