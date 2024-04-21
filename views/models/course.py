from fastapi import Query
from pydantic import BaseModel, Field

class Course(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    course_no: str = Field(..., title="", description="课程编码",examples=['19'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])

    course_name: str = Field(..., title="Grade_name",description="课程名称",examples=['语文'])




