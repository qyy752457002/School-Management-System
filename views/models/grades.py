from pydantic import BaseModel, Field

class Grades(BaseModel):
    school_id: int = Field(..., title="学校ID", description="学校ID",examples=[''])
    grade_no: str = Field(..., title="年级编号", description="年级编号",examples=['一年级'])
    grade_name: str = Field(..., title="Grade_name",description="Grade_name",examples=['一年级'])
    grade_alias: str = Field(...,  description="Grade_alias",examples=['一年级'])
    description: str = Field(None,  description="简介",examples=['fsdfdsfsdxxx'])


    class Config:
        schema_extra = {
            "example": {
                "school_id": "SC2032633",
                "grade_no": "EDU202403256",
                "grade_name": "A school management system",
                "grade_alias": "Lfun technical",
            }
        }
