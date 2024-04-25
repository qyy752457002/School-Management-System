from enum import Enum

from pydantic import BaseModel, Field



class OperationTargetType(str, Enum):
    """
    操作主体类型

    """
    PLANNING_SCHOOL = "planning_school"
    SCHOOL  = "school"
    CAMPUS  = "campus"

    TEACHER  = "teacher"
    STUDENT  = "student"

    @classmethod
    def to_list(cls):
        return [cls.PLANNING_SCHOOL, cls.SCHOOL, cls.CAMPUS, cls.TEACHER, cls.STUDENT]

class OperationType(str, Enum):
    """
    操作类型-页面的操作 对象

    """
    CREATE = "创建"
    MODIFY  = "删除"
    DELETE  = "修改"
    @classmethod
    def to_list(cls):
        return [cls.CREATE, cls.DELETE, cls.MODIFY,  ]

class OperationModule(str, Enum):
    """
    操作模块

    """
    CREATE_SCHOOL = "开园"
    KEYINFO  = "关键信息"
    BASEINFO  = "基础信息"
    @classmethod
    def to_list(cls):
        return [cls.CREATE_SCHOOL, cls.KEYINFO, cls.BASEINFO,  ]

class OperationRecord(BaseModel):
    action_target_id: str = Field(..., title="操作对象ID", description="操作对象ID",examples=[''])
    action_type: str = Field(..., title="操作类型", description="操作类型",examples=[''])
    ip: str = Field(..., title=" Description",  description="操作IP",examples=[''])
    change_data: str = Field(..., title=" Author", description="变更前后数据",examples=[''])
    change_field: str = Field(...,   description=" 变更字段",examples=[''])
    change_item: str = Field(...,   description=" 变更项",examples=[''])
    timestamp: str = Field(...,   description="操作时间 ",examples=[''])
    action_reason: str = Field(...,   description=" 操作原因",examples=[''])
    doc_upload: str = Field(...,   description=" 附件",examples=[''])
    status: str = Field(...,   description=" 状态",examples=[''])
    account: str = Field(...,   description=" 操作账号",examples=[''])
    operator: str = Field(...,   description=" 操作人",examples=[''])
    module: str = Field(...,   description=" 操作模块",examples=[''])
    target: str = Field(...,   description=" 操作对象",examples=[''])


