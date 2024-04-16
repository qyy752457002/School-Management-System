from pydantic import BaseModel, Field


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


