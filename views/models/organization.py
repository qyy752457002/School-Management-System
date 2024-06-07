from fastapi import Query
from pydantic import BaseModel, Field


class Organization(BaseModel):
    """
     org_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="组织分类 行政类等")

    org_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="组织或者部门名称 例如行政部")
    parent_id: Mapped[int] = mapped_column( comment="父级ID",default=0,nullable=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID",default=0,nullable=True)
    member_cnt: Mapped[int] = mapped_column( comment="人数",default=0,nullable=True)
    """
    id:int= Query(None, title="", description="id", example='1')
    school_id: int = Field(None, title="", description="学校id",examples=['1'])

    org_type: str = Field(None, title="", description="组织分类 行政类等",examples=['行政类'])
    org_name: str = Field(None, title="", description="组织或者部门名称 例如行政部",examples=['行政部'])
    parent_id: int = Field(None, title="", description="父级ID",examples=['1'])
    member_cnt: int = Field(None, title="", description="人数",examples=['1'])



