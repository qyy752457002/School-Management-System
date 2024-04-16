from pydantic import BaseModel, Field

class SubSystem(BaseModel):
    system_name: str = Field(..., title="",description="系统名称",examples=['学校版'])
    system_no: str = Field(..., title="系统编号", description="系统编号",examples=['02'])
    system_url: str = Field(..., title="", description="系统url",examples=['www.fsdfsd.cc'])
    system_icon: str = Field(..., title="", description="系统icon",examples=['www.dd.cc/343.jpg'])
    system_description: str = Field(..., title="", description="系统简述",examples=['学校版的教育登录'])


