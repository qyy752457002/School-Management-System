from pydantic import BaseModel, Field
from datetime import date

class WorkFlowNodeDependStrategyModel(BaseModel):
    """
    依赖code：depend_code
    参数名：parameter_name
    参数值：parameter_value
    操作：operation
    """
    work_flow_node_depend_strategy_id: int = Field(None, title="work_flow_node_depend_strategyID", description="work_flow_node_depend_strategyID")
    depend_code: str = Field(..., title="依赖code", description="依赖code")
    parameter_name: str = Field(..., title="参数名", description="参数名")
    parameter_value: str = Field(..., title="参数值", description="参数值")
    operation: str = Field(..., title="操作", description="操作")
    
    



    
    


