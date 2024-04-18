from pydantic import BaseModel, Field

class GraduationYear(BaseModel):
    graduation_year: str = Field(..., title="", description="届别",examples=['2003'])
    description: str = Field(None,  description="简介",examples=['fsdfdsfsdxxx'])
    status:str= Field(None,  description="状态",examples=['已开启'])


