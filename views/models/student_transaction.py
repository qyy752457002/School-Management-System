from fastapi import Query
from pydantic import BaseModel, Field

class StudentTransaction(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    in_school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    # course_no: str = Field(..., title="", description="课程编码",examples=['19'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])

    status: str = Field('', title="",description="状态",examples=[''])




