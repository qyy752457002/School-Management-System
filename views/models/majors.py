from fastapi import Query
from pydantic import BaseModel, Field

class Majors(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),

    school_id: int = Field(0, title="学校ID", description="学校ID",examples=[''])
    major_name: str = Field(..., title="Grade_name",description="专业名称",examples=['农林牧鱼 '])
    major_id: str = Field(..., title="专业ID", description="专业ID",examples=['19'])
    major_type: str = Field(...,  description="专业类型",examples=['农林'])
    major_id_lv2: str = Field(..., title="专业ID", description="2级专业ID",examples=['23'])
    major_id_lv3: str = Field(..., title="专业ID", description="3级专业ID",examples=['125'])



