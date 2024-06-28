from pydantic import BaseModel, Field
from datetime import date

class WorkFlowNodeDefineModel(BaseModel):
    """
    流程code：process_code
    节点名称：node_name
    节点code：node_code
    """
    process_code: str = Field(..., title="流程code", description="流程code")
    node_name: str = Field(..., title="节点名称", description="节点名称")
    node_code: str = Field(..., title="节点code", description="节点code")


class WorkFlowNodeDefineReModel(BaseModel):
    """
    流程code：process_code
    节点名称：node_name
    节点code：node_code
    节点分配的机构：node_org
    """
    process_code: str = Field(..., title="流程code", description="流程code")
    node_name: str = Field(..., title="节点名称", description="节点名称")
    node_code: str = Field(..., title="节点code", description="节点code")
    node_org: str = Field(..., title="节点分配的机构", description="节点分配的机构")

    


