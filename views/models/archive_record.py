from fastapi import Query
from pydantic import BaseModel, Field

class ArchiveRecord(BaseModel):
    """
    行政属地
    学校
    归档名称
    归档年份
    归档状态
    归档数量
    归档时间


    """
    id:int= Query(0, title="", description="id", example='1'),
    school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    archive_name: str = Field('', title="归档名称", description="归档名称",examples=['2019年'])
    archive_year: str = Field('', title="归档年份", description="归档年份",examples=['2019'])
    archive_status: str = Field('', title="归档状态", description="归档状态",examples=['已归档'])
    archive_count: int = Field(0, title="归档数量", description="归档数量",examples=['1'])
    archive_time: str = Field('', title="归档时间", description="归档时间",examples=['2021-10-10 00:00:00'])
    archive_remark: str = Field('', title="归档备注", description="归档备注",examples=['备注'])
    borough:str=Query('', title=" Author Email", description=" 行政管辖区",examples=['铁西区'])







