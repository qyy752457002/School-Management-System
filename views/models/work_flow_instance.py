from pydantic import BaseModel, Field,model_validator
from datetime import date, datetime
from enum import Enum
from typing import Optional

class WorkFlowInstanceStatus(str, Enum):
    """
    进行中：pending
    已同意：approved
    已拒绝：rejected
    """
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    @classmethod
    def to_list(cls):
        return [cls.PENDING, cls.APPROVED, cls.REJECTED]

class WorkFlowInstanceCreateModel(BaseModel):
    """
    流程定义id：process_code
    申请人id：applicant_id
    开始时间：start_time
    结束时间：end_time
    流程状态：process_status
    说明：description
    """

    process_code: str = Field(..., title="流程定义id", description="流程定义id")
    applicant_name: str = Field(..., title="申请人姓名", description="申请人姓名")
    start_time: datetime = Field(datetime.now(), title="开始时间", description="开始时间")
    end_time: Optional[datetime] = Field(None, title="结束时间", description="结束时间")
    process_status: WorkFlowInstanceStatus = Field("pending", title="流程状态", description="流程状态")
    description: str = Field("", title="说明", description="说明")


    @model_validator(mode='after')
    def set_end_time(self):
        if self.process_status == "approved" or self.process_status == "rejected":
            self.end_time = datetime.now()
        return self



class WorkFlowInstanceModel(WorkFlowInstanceCreateModel):
    process_instance_id: str = Field(..., title="流程实例id", description="流程实例id")

# 工作流节点相关模型

class WorkFlowNodeInstanceStatus(str, Enum):
    """
    待进行：pending
    已完成：completed
    """
    PENDING = "pending"
    COMPLETED = "completed"

    @classmethod
    def to_list(cls):
        return [cls.PENDING, cls.COMPLETED]


class NodeAction(str, Enum):
    """
    拒绝：rejected
    同意：approved
    撤回：revoke
    无：none
    """
    REJECTED = "rejected"
    APPROVED = "approved"
    REVOKE = "revoke"
    CREATE= "create"
    NONE = "none"

    @classmethod
    def to_list(cls):
        return [cls.REJECTED, cls.APPROVED, cls.REVOKE, cls.CREATE, cls.NONE]


class WorkFlowNodeCreatInstanceModel(BaseModel):
    """
    节点实例id：node_instance_id
    流程实例id：process_instance_id
    节点定义的id：node_definition_id
    节点状态：node_status
    操作人角色：operator_role
    操作人id：operator_id
    操作时间：operation_time
    动作：action
    说明：description
    """
    process_instance_id: str = Field(..., title="流程实例id", description="流程实例id")
    node_code: str = Field(..., title="节点定义的id", description="节点定义的id")
    node_status: WorkFlowNodeInstanceStatus = Field("pending", title="节点状态", description="节点状态")
    operator_id: str = Field(..., title="操作人id", description="操作人id")
    operation_time: str = Field(..., title="操作时间", description="操作时间")
    action: NodeAction = Field("none", title="动作", description="动作")
    description: str = Field(..., title="说明", description="说明")


class WorkFlowNodeInstanceModel(WorkFlowNodeCreatInstanceModel):
    node_instance_id: str = Field(..., title="节点实例id", description="节点实例id")


    
    


