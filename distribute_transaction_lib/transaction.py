from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


# 视图模型
# 事务状态
class TransactionState(str, Enum):
    pending = 'pending'
    running = 'running'
    completed = 'completed'
    succeeded = 'succeeded'
    failed = 'failed'
    aborted = 'aborted'
    cancelled = 'cancelled'
    timeout = 'timeout'

# 事务 模型
class Transaction(BaseModel):
    transaction_id: str
    transaction_type: str
    payload: dict
    state: TransactionState = TransactionState.pending
    operator: str = None
    created_at: datetime = None
    progress: float = 0.0
    process_desc: str = ""
    completed_time: datetime = None
    result_extra: dict = dict()


# 各单位部署系统的 模型
class UnitSystem(BaseModel):
    school_id: int
    institution_id: int
    unit_url: str
    created_at: datetime = None
    remark: str = ""

# 事务节点  模型
class TransactionNode(BaseModel):
    transaction_code: str
    prepare_url: str
    base_url: str= Field(None, title="", description="",examples=['1'])
    precommit_url: str
    commit_url : str
