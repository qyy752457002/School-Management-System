from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field


class StudentTransactionStatus(str, Enum):
    """
    状态   待审批  已通过 已拒绝
    """
    # ALL = "All"

    NEEDAUDIT = "needaudit"

    PASS = "pass"
    REFUSE = "refuse"

    @classmethod
    def to_list(cls):
        return [cls.NEEDAUDIT, cls.PASS, cls.REFUSE]

class StudentTransaction(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    in_school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])
    status: str = Field('', title="",description="状态",examples=[''])




class StudentTransactionFlow(BaseModel):
    """
    student_id: Mapped[int] = mapped_column(nullable=True , comment="学生ID",default=0)
    apply_id: Mapped[int] = mapped_column(nullable=True , comment="申请ID",default=0)

    stage: Mapped[str] = mapped_column(String(255),  nullable=True, comment="阶段",default='')
    description: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程描述",default='')
    remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程备注",default='')
    """
    id:int= Query(None, title="", description="id", example='1'),
    apply_id: int = Field(0, title="", description="转学申请ID",examples=['1'])
    status: str = Field('', title="",description="状态",examples=[''])
    stage: str = Field('', title="",description="阶段",examples=[''])

    description: str = Field('', title="",description="描述",examples=[''])
    remark: str = Field('', title="",description="备注",examples=[''])
    student_id: int = Field(0, title="", description="学生ID",examples=['1'])




