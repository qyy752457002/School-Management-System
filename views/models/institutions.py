from pydantic import BaseModel, Field


class Institutions(BaseModel):
    # todo title 等 必须和表头一样
    institution_name: str = Field(..., title='单位名称', description="单位名称",examples=['文化部'])
    institution_en_name: str = Field(...,title='单位名称英文',   description=" 单位名称英文",examples=['CEDUCUL'])
    institution_category: str = Field(..., title='单位分类',  description=" 单位分类",examples=['事业单位'])
    institution_type: str = Field(...,   title='单位类型',  description="单位类型 ",examples=[''])
    fax_number: str = Field(...,   title='传真电话',  description=" 传真电话",examples=['020-256526256'])
    email: str = Field(...,   title='单位电子信箱',  description=" 单位电子信箱",examples=['fsdfds@odk.cc'])
    contact_number: str = Field(...,   title='联系电话',  description=" 联系电话",examples=['0232156562'])
    area_code: str = Field(...,   title='电话区号',  description=" 电话区号",examples=['020'])
    institution_code: str = Field(...,   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    create_date: str = Field(...,   title='成立年月',  description=" 成立年月",examples=['2020-10-23'])
    leg_repr_name: str = Field(...,   title='法定代表人姓名',  description=" 法定代表人姓名",examples=['XXX'])
    party_leader_name: str = Field(...,   title='党组织负责人姓名',  description=" 党组织负责人姓名",examples=['YYY'])
    party_leader_position: str = Field(...,   title='党组织负责人职务',  description=" 党组织负责人职务",examples=['FSDFSD'])
    adm_leader_name: str = Field(...,   title='行政负责人姓名',  description=" 行政负责人姓名",examples=['GGGG'])
    adm_leader_position: str = Field(...,   title='行政负责人职务',  description=" 行政负责人职务",examples=['FSDFSD'])
    department_unit_number: str = Field(...,   title='属地管理行政部门单位号',  description=" 属地管理行政部门单位号",examples=['DFG454353454'])
    sy_zones: str = Field(...,   title='属地管理行政部门所在地地区',  description=" 属地管理行政部门所在地地区",examples=['铁西区'])
    social_credit_code: str = Field(...,   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656'])
    postal_code: str = Field(...,   title='邮政编码',  description=" 邮政编码",examples=['4587236'])
    detailed_address: str = Field(...,   title='详细地址',  description=" 详细地址",examples=['FSDFSDFSDF234E23'])
    related_license_upload: str = Field(...,   title='相关证照上传',  description=" 相关证照上传",examples=[''])
    long: str = Field(...,   title='所在经度',  description=" 所在经度",examples=['201.22'])
    lat: str = Field(...,   title='所在纬度',  description=" 所在纬度",examples=['65.33'])
    urban_rural_nature: str = Field(...,   title='城乡性质',  description=" 城乡性质",examples=['城镇'])
    location_economic_attribute: str = Field(...,   title='所在地经济属性',  description=" 所在地经济属性",examples=['镇'])
    leg_repr_certificatenumber: str = Field(...,   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])
    is_entity: str = Field(...,   title='是否实体',  description=" 是否实体",examples=['是'])
    website_url: str = Field(...,   title='网址',  description=" 网址",examples=['WWW.BDIUFD.COM'])
    status: str = Field(...,   title='状态',  description=" 状态",examples=[''])
    membership_no: str = Field(...,   title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    membership_category: str = Field(...,   title='隶属单位类型',  description=" 隶属单位类型",examples=['行政'])

class InstitutionTask(BaseModel):
    """{'file_name':filename,'bucket':bucket,'scene':scene},"""
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])


class InstitutionsValid(BaseModel):
    #   title  实际根据title匹配
    institution_name: str = Field(..., title='单位名称',  examples=['文化部'])
    institution_en_name: str = Field(..., title='a',   examples=['CEDUCUL'])









