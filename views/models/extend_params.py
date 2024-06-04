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
    school_id: str|None = Field('', title="", description="",examples=['19'])
    county_id: str|None = Field('', title="", description="",examples=['19'])




