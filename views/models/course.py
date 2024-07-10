from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Course(BaseModel):
    id:int|str= Query(None, title="", description="id", example='1'),
    school_id: int|str = Field(0, title="学校ID", description="学校ID",examples=['1'])
    course_no: str = Field(..., title="", description="课程编码",examples=['19'])
    district: str|None = Field('', title="", description="",examples=['19'])
    city: str|None = Field('', title="", description="",examples=['19'])
    grade_id: int |str= Field(0, title="年级ID", description="年级ID",examples=['1'])
    course_name: str = Field(..., title="Grade_name",description="课程名称",examples=['语文'])
    school_type: str|None = Field('', title="",description="",examples=[''])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id',]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                # data[_change] = str(data[_change])
                pass
            else:
                pass
        return data

