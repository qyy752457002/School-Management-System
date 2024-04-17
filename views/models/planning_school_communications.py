from fastapi import Query
from pydantic import BaseModel, Field


class PlanningSchoolCommunications(BaseModel):
    id:int= Query(None, title="", description="", example='1'),
    planning_school_id: int = Field(..., title="", description="规划校id",examples=[''])

    postal_code: str = Field(..., title="", description="邮政编码",examples=[''])
    fax_number: str = Field(..., title="", description="传真电话",examples=['SC2032633'])

    email: str = Field(..., title="", description="单位电子信箱",examples=[''])
    contact_number: str = Field(..., title="", description="联系电话",examples=[''])
    area_code: str = Field(..., title="", description="电话区号",examples=[''])
    long: str = Field(..., title="", description="所在经度",examples=[''])
    lat: str = Field(..., title="", description="所在纬度",examples=[''])
    leg_repr_name: str = Field(..., title="", description="法定代表人姓名",examples=[''])
    party_leader_name: str = Field(..., title="", description="党组织负责人姓名",examples=[''])
    party_leader_position: str = Field(..., title="", description="党组织负责人职务",examples=[''])
    adm_leader_name: str = Field(..., title="", description="行政负责人姓名",examples=[''])
    adm_leader_position: str = Field(..., title="", description="行政负责人职务",examples=[''])
    loc_area: str = Field(..., title="", description="园所所在地区",examples=[''])

    loc_area_pro: str = Field(..., title="", description="园所所在地(省级)",examples=[''])
    detailed_address: str = Field(..., title="", description="园所详细地址",examples=[''])
    related_license_upload: str = Field(..., title="", description="相关证照上传",examples=[''])
    school_web_url: str = Field(..., title="", description="校园网域名",examples=[''])













