from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

class Grades(BaseModel):
    """
    school_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="教育阶段/学校类别 例如 小学 初中")
    grade_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="年级类型/班级类型 例如 一年级 二年级 三年级")

    """
    grade_name: str = Field(..., title="",description="年级名称",examples=['一年级'])
    grade_type: str = Field('',  description="年级类型/班级类型 例如 一年级 二年级 三年级",examples=['一年级'])
    school_type: str = Field('',  description="教育阶段/学校类别 例如 小学 初中",examples=['小学'])

    grade_alias: str = Field('',  description="年级别名",examples=['一年级'])
    school_id: int = Field(0, title="学校ID", description="学校ID",examples=[0])
    grade_no: str = Field("", title="年级编号", description="年级编号",examples=['一年级'])
    city: str|None = Field("", title="", description="",examples=[''])
    district: str|None = Field("", title="", description="",examples=[''])

    description: str = Field('',  description="简介",examples=['fsdfdsfsdxxx'])
    created_at: datetime = Field('',  description="简介",examples=['2020-01-01'])
    id:int= Query(0, title="", description="id", example='1'),

