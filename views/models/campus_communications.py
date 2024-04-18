from fastapi import Query
from pydantic import BaseModel, Field


class CampusCommunications(BaseModel):
    """
    校区负责人姓名
campus_leader_name
校区负责人职位
campus_leader_position
    """
    id:int= Query(None, title="", description="", example='1'),
    campus_id: int = Field(..., title="", description="校区id",examples=['1'])

    postal_code: str = Field(..., title="", description="邮政编码",examples=['472566'])
    fax_number: str = Field(..., title="", description="传真电话",examples=['020265656'])

    email: str = Field(..., title="", description="单位电子信箱",examples=['ddd@qq.cc'])
    contact_number: str = Field(..., title="", description="联系电话",examples=['126303366'])
    area_code: str = Field(..., title="", description="电话区号",examples=['0365'])
    long: str = Field(..., title="", description="所在经度",examples=['223.66'])
    lat: str = Field(..., title="", description="所在纬度",examples=['23.65'])
    leg_repr_name: str = Field(..., title="", description="法定代表人姓名",examples=['XX'])
    party_leader_name: str = Field(..., title="", description="党组织负责人姓名",examples=['YY'])
    party_leader_position: str = Field(..., title="", description="党组织负责人职务",examples=['SSSS'])
    adm_leader_name: str = Field(..., title="", description="行政负责人姓名",examples=['KKKK'])
    adm_leader_position: str = Field(..., title="", description="行政负责人职务",examples=['DDDD'])
    loc_area: str = Field(..., title="", description="园所所在地区",examples=['XXXXFSDFSD'])

    loc_area_pro: str = Field(..., title="", description="园所所在地(省级)",examples=['FSDFSD'])
    detailed_address: str = Field(..., title="", description="园所详细地址",examples=['FSDFSD'])
    related_license_upload: str = Field(..., title="", description="相关证照上传",examples=[''])
    campus_web_url: str = Field(..., title="", description="校园网域名",examples=['WW.SS.CC'])
    campus_leader_name: str = Field(..., title="", description="校区负责人姓名",examples=['3'])

    campus_leader_position: str = Field(..., title="", description="校区负责人职位",examples=['3'])















