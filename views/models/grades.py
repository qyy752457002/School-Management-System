from pydantic import BaseModel, Field

class Grades(BaseModel):
    school_id: str = Field(..., title="学校ID", description="1-20字符")
    grade_no: str = Field(..., title="年级编号", description="1-20字符")
    grade_name: str = Field(..., title="Grade_name",description="Grade_name")
    grade_alias: str = Field(..., title="Grade_alias",description="Grade_alias")

    class Config:
        schema_extra = {
            "example": {
                "school_id": "SC2032633",
                "grade_no": "EDU202403256",
                "grade_name": "A school management system",
                "grade_alias": "Lfun technical",
            }
        }
