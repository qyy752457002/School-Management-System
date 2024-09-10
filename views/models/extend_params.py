from typing import List

from mini_framework.multi_tenant.tenant import Tenant
from pydantic import BaseModel, Field

from views.models.system import UnitType, SystemType, EduType


class ExtendParams(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)

    system_type: SystemType | None = Field('', title="", description="老师 学生 单位", examples=['19'])
    unit_type: UnitType | None = Field('', title="", description="市 区 学校", examples=['19'])
    edu_type: EduType | None = Field('', title="学校阶段", description="幼儿园/小学/初中", examples=['19'])
    # 档学校时 有这个学校ID
    school_id: int = Field(None, title="", description="学校ID", examples=['19'])
    school_ids: List[int] =   Field(None, title="", description="学校ID", examples=['19'])
    planning_school_id: int = Field(None, title="", description="", examples=['19'])
    # 当区 时有区ID  实际上是code
    county_id: int | str = Field(None, title="", description="区编码", examples=['19'])
    county_name: int = Field(None, title="", description="区名称", examples=['19'])
    # 市  有市ID
    city: str = Field(None, title="", description="城市 市端这里是沈阳的编码", examples=[''])
    user_name: str = Field(None, title="", description="", examples=[''])
    tenant: Tenant = Field(None, title="", description="", examples=[''])
