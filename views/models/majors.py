from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Majors(BaseModel):
    id:int|str= Query(None, title="", description="id", example='1'),

    school_id: int |str= Field(0, title="学校ID", description="学校ID",examples=[''])
    major_name: str = Field('', title="Grade_name",description="专业名称",examples=['农林牧鱼 '])
    major_no: str|None = Field('', title="", description="专业码",examples=['19'])
    major_type: str |None= Field('',  description="专业类型",examples=['农林'])
    major_id_lv2: str|None = Field('', title="专业ID", description="2级专业ID",examples=['23'])
    major_id_lv3: str|None = Field('', title="专业ID", description="3级专业ID",examples=['125'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",]
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



