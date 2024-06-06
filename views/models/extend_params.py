from fastapi import Query
from pydantic import BaseModel, Field

class ExtendParams(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    system_type: str|None = Field('', title="", description="",examples=['19'])
    unit_type: str|None = Field('', title="", description="",examples=['19'])
    edu_type: str|None = Field('', title="", description="",examples=['19'])
    # 档学校时 有这个学校ID
    school_id: int = Field(None, title="", description="",examples=['19'])
    planning_school_id: int = Field(None, title="", description="",examples=['19'])
    # 当区 时有区ID  实际上是code
    county_id: int = Field(None, title="", description="",examples=['19'])
    county_name: int = Field(None, title="", description="",examples=['19'])
    # 市  有市ID
    city: str = Field(None, title="", description="",examples=['19'])




