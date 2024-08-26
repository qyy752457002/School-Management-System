from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class LeaderInfo(BaseModel):
    """
     领导

    """
    id:int|str= Query(None, title="", description="id", example='1'),

    school_id: int |str= Field(None, title="学校ID", description="学校ID",examples=['1'])
    institution_id: int|str = Field(None, title="", description="事业单位ID",examples=['1'])
    planning_school_id: int|str = Field(None, title="", description="规划校id",examples=['1'])
    leader_name: str = Field(..., title="", description="领导姓名",examples=['xxxx'])
    position: str = Field(..., title="", description="职务",examples=['xxxx'])
    status: str = Field(None, title="", description="状态",examples=['正常'])
    start_date: str = Field(..., title="", description="任职开始时间",examples=['2021-10-10 00:00:00'])
    end_date: str = Field(..., title="", description="任职结束时间",examples=['2021-10-10 00:00:00'])
    job_content: str = Field( '', title="", description="工作内容",examples=['xxxx'])
    job_responsibility: str = Field( '', title="", description="分管工作",examples=['xxxx'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'institution_id','planning_school_id']
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




