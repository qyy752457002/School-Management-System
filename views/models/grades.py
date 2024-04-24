from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

class Grades(BaseModel):
    grade_name: str = Field(..., title="",description="年级名称",examples=['一年级'])
    grade_alias: str = Field(...,  description="年级别名",examples=['一年级'])
    school_id: int = Field(0, title="学校ID", description="学校ID",examples=[0])
    grade_no: str = Field("", title="年级编号", description="年级编号",examples=['一年级'])

    description: str = Field('',  description="简介",examples=['fsdfdsfsdxxx'])
    created_at: datetime = Field('',  description="简介",examples=['2020-01-01'])
    id:int= Query(0, title="", description="id", example='1'),

