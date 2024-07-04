from fastapi import Query
from pydantic import BaseModel, Field


class PlanningSchoolCommunications(BaseModel):
    id:int|None= Field(None, title="", description="", example='1'),
    planning_school_id: int|str |None= Field(None, title="", description="规划校id",examples=['1'])
    postal_code: str|None = Field(None, title="邮政编码", description="邮政编码",examples=['472566'])
    fax_number: str|None = Field(None, title="传真电话", description="传真电话",examples=['020265656'])
    email: str|None = Field(None, title="单位电子信箱", description="单位电子信箱",examples=['ddd@qq.cc'])
    contact_number: str|None = Field(None, title="联系电话", description="联系电话",examples=['126303366'])
    area_code: str |None= Field(None, title="电话区号", description="电话区号",examples=['0365'])
    long: str|None = Field(None, title="所在经度", description="所在经度",examples=['223.66'])
    lat: str|None = Field(None, title="所在纬度", description="所在纬度",examples=['23.65'])
    leg_repr_name: str|None = Field(None, title="法定代表人姓名", description="法定代表人姓名",examples=['XX'])
    party_leader_name: str|None = Field(None, title="党组织负责人姓名", description="党组织负责人姓名",examples=['YY'])
    party_leader_position: str |None= Field(None, title="党组织负责人职务", description="党组织负责人职务",examples=['SSSS'])
    adm_leader_name: str|None = Field(None, title="行政负责人姓名", description="行政负责人姓名",examples=['KKKK'])
    adm_leader_position: str|None = Field(None, title="行政负责人职务", description="行政负责人职务",examples=['DDDD'])
    loc_area: str|None = Field(None, title="园所所在地区", description="园所所在地区",examples=['XXXXFSDFSD'])
    loc_area_pro: str|None = Field(None, title="园所所在地(省级)", description="园所所在地(省级)",examples=['FSDFSD'])
    detailed_address: str|None = Field(None, title="园所详细地址", description="园所详细地址",examples=['FSDFSD'])
    related_license_upload: str |None= Field(None, title="相关证照上传", description="相关证照上传",examples=[''])
    school_web_url: str|None = Field(None, title="校园网域名", description="校园网域名",examples=['WW.SS.CC'])

