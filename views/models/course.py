from pydantic import BaseModel, Field

class Course(BaseModel):
    school_id: str = Field(..., title="学校ID", description="学校ID",examples=[''])
    course_no: str = Field(..., title="", description="课程编码",examples=['19'])
    grade_id: str = Field(None, title="年级ID", description="年级ID",examples=['一年级'])

    course_name: str = Field(..., title="Grade_name",description="课程名称",examples=['语文'])




