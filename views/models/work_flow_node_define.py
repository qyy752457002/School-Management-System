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
    

    


