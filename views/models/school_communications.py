from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class SchoolCommunications(BaseModel):
    id:int= Query(None, title="", description="", example='1'),
    school_id: int = Field(0, title="", description="学校id",examples=['1'])

    postal_code: str = Field(None, title="", description="邮政编码",examples=['472566'])
    fax_number: str = Field(None, title="", description="传真电话",examples=['020265656'])

    email: str = Field(None, title="", description="单位电子信箱",examples=['ddd@qq.cc'])
    contact_number: str = Field(None, title="", description="联系电话",examples=['126303366'])
    area_code: str = Field(None, title="", description="电话区号",examples=['0365'])
    long: str = Field(None, title="", description="所在经度",examples=['223.66'])
    lat: str = Field(None, title="", description="所在纬度",examples=['23.65'])
    leg_repr_name: str = Field(None, title="", description="法定代表人姓名",examples=['XX'])
    party_leader_name: str = Field(None, title="", description="党组织负责人姓名",examples=['YY'])
    party_leader_position: str = Field(None, title="", description="党组织负责人职务",examples=['SSSS'])
    adm_leader_name: str = Field(None, title="", description="行政负责人姓名",examples=['KKKK'])
    adm_leader_position: str = Field(None, title="", description="行政负责人职务",examples=['DDDD'])
    loc_area: str = Field(None, title="", description="园所所在地区",examples=['XXXXFSDFSD'])

    loc_area_pro: str = Field(None, title="", description="园所所在地(省级)",examples=['FSDFSD'])
    detailed_address: str = Field(None, title="", description="园所详细地址",examples=['FSDFSD'])
    related_license_upload: str = Field(None, title="", description="相关证照上传",examples=[''])
    school_web_url: str = Field(None, title="", description="校园网域名",examples=['WW.SS.CC'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["school_id", 'id']
        for _change in _change_list:
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data














