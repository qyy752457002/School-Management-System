from fastapi import Query
from pydantic import BaseModel, Field
from datetime import datetime

class CertificateBatchQuery(BaseModel):
    year: int = Query(None, title="", description="年份", example='2023')
    batch_name: str = Query("", title="", description="批次名称", example='2023界毕业批次')

class CertificateBatchField(BaseModel):
    id: int = Field(None, title="", description="ID", examples='1')
    batch_number: int = Field(None, title="", description="批次编码", examples='G373422141')
    batch_name: str = Field('', title="", description="批次名称", examples='2023界毕业批次')
    status: bool = Field(False, title="", description="状态", examples='False')
    created_at: datetime|None = Field('',  description="创建时间", examples='2016-09-22 08:50:08')
    certification: str = Field('', title="", description="制证模板", examples='2023界毕业模板')
    