from fastapi import Query
from pydantic import BaseModel, Field

class LeaderInfo(BaseModel):
    """
     领导
     planning_school_id: Mapped[int] = mapped_column(  nullable=True , comment="规划ID",default=0)
    leader_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="领导姓名",default='')
    position: Mapped[str] = mapped_column(String(255),  nullable=True, comment="职务",default='')
    status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="状态",default='')
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="任职开始时间")
    end_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="任职结束时间")
    job_content: Mapped[str] = mapped_column(String(255),  nullable=True, comment="工作内容",default='')
    job_responsibility: Mapped[str] = mapped_column(String(255),  nullable=True, comment="分管工作",default='')
    school_id: Mapped[int] = mapped_column(  nullable=True , comment="学校ID",default=0)
    institution_id: Mapped[int] = mapped_column(  nullable=True , comment="事业单位ID",default=0)
    """
    id:int= Query(None, title="", description="id", example='1'),

    school_id: int = Field(None, title="学校ID", description="学校ID",examples=['1'])
    institution_id: int = Field(None, title="", description="事业单位ID",examples=['1'])
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])
    leader_name: str = Field(..., title="", description="领导姓名",examples=['xxxx'])
    position: str = Field(..., title="", description="职务",examples=['xxxx'])
    status: str = Field(None, title="", description="状态",examples=['正常'])
    start_date: str = Field(..., title="", description="任职开始时间",examples=['2021-10-10 00:00:00'])
    end_date: str = Field(..., title="", description="任职结束时间",examples=['2021-10-10 00:00:00'])
    job_content: str = Field(..., title="", description="工作内容",examples=['xxxx'])
    job_responsibility: str = Field(..., title="", description="分管工作",examples=['xxxx'])




