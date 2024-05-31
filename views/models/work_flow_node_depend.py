from pydantic import BaseModel, Field
from datetime import date

class WorkFlowNodeDependModel(BaseModel):
    """
    依赖code：depend_code
    来源节点：source_node
    下一个节点：next_node
    """
    depend_code: str = Field(..., title="依赖code", description="依赖code")
    source_node: str = Field(..., title="来源节点", description="来源节点")
    next_node: str = Field(..., title="下一个节点", description="下一个节点")
    

    
    


