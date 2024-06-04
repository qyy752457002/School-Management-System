from fastapi import Query
from pydantic import BaseModel, Field

class EducationYearModel(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    education_year: int = Field(0, title="", description="",examples=['1'])
    school_type: str = Field(..., title="", description="",examples=['19'])
    district: str = Field(..., title="", description="",examples=['19'])
    city: str = Field(..., title="", description="",examples=['19'])




