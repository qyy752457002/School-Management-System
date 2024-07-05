from typing import List

from fastapi.params import Query
from pydantic import BaseModel, Field

from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.system import InstitutionType


class Institutions(BaseModel):
    #   title 等 必须和表头一样
    id:int= Query(None, title="", description="", example='1')

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
    social_credit_code: str|None = Field(...,   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656'])
    postal_code: str = Field(...,   title='邮政编码',  description=" 邮政编码",examples=['4587236'])
    detailed_address: str = Field(...,   title='详细地址',  description=" 详细地址",examples=['FSDFSDFSDF234E23'])
    related_license_upload: str = Field(...,   title='相关证照上传',  description=" 相关证照上传",examples=[''])
    long: str = Field(...,   title='所在经度',  description=" 所在经度",examples=['201.22'])
    lat: str = Field(...,   title='所在纬度',  description=" 所在纬度",examples=['65.33'])
    urban_rural_nature: str |None = Field("",   title='城乡性质',  description=" 城乡性质",examples=['城镇'])
    location_economic_attribute: str |None = Field("",   title='所在地经济属性',  description=" 所在地经济属性",examples=['镇'])
    urban_ethnic_nature: str |None = Field("",   title='所在地民族属性',  description="",examples=[''])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])
    is_entity: bool |None = Field(None,   title='是否实体',  description=" 是否实体",examples=[''])

    website_url: str = Field(...,   title='网址',  description=" 网址",examples=['WWW.BDIUFD.COM'])
    status: str = Field(...,   title='状态',  description=" 状态",examples=[''])
    membership_no: str = Field(...,   title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    membership_category: str = Field(...,   title='隶属单位类型',  description=" 隶属单位类型",examples=['行政'])
    workflow_status: str|None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int= Query(0, title="", description="", example='1')

class InstitutionTask(BaseModel):
    """{'file_name':filename,'bucket':bucket,'scene':scene},"""
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])


class InstitutionsValid(BaseModel):
    #   title  实际根据title匹配
    institution_name: str = Field(..., title='单位名称',  examples=['文化部'])
    institution_en_name: str = Field(..., title='a',   examples=['CEDUCUL'])

class InstitutionOptional(BaseModel):
    #   title 等 必须和表头一样 todo 为了保持原样输出 必须 进行转换 2个视图模型的映射
    id:int= Query(None, title="", description="", example='1')

    institution_name: str|None = Field("", title='单位名称', description="单位名称",examples=['文化部'])
    institution_en_name: str |None= Field("",title='单位名称英文',   description=" 单位名称英文",examples=['CEDUCUL'])
    institution_category: str|None = Field("", title='单位分类',  description=" 单位分类",examples=['事业单位'])
    institution_type: str|None = Field("",   title='单位类型',  description="单位类型 ",examples=[''])
    fax_number: str |None= Field("",   title='传真电话',  description=" 传真电话",examples=['020-256526256'])
    email: str |None = Field("",   title='单位电子信箱',  description=" 单位电子信箱",examples=['fsdfds@odk.cc'])
    contact_number: str |None = Field("",   title='联系电话',  description=" 联系电话",examples=['0232156562'])
    area_code: str |None = Field("",   title='电话区号',  description=" 电话区号",examples=['020'])
    institution_code: str |None = Field("",   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    create_date: str |None = Field("",   title='成立年月',  description=" 成立年月",examples=['2020-10-23'])
    leg_repr_name: str |None = Field("",   title='法定代表人姓名',  description=" 法定代表人姓名",examples=['XXX'])
    party_leader_name: str |None = Field("",   title='党组织负责人姓名',  description=" 党组织负责人姓名",examples=['YYY'])
    party_leader_position: str |None = Field("",   title='党组织负责人职务',  description=" 党组织负责人职务",examples=['FSDFSD'])
    adm_leader_name: str |None = Field("",   title='行政负责人姓名',  description=" 行政负责人姓名",examples=['GGGG'])
    adm_leader_position: str |None = Field("",   title='行政负责人职务',  description=" 行政负责人职务",examples=['FSDFSD'])
    department_unit_number: str |None = Field("",   title='属地管理行政部门单位号',  description=" 属地管理行政部门单位号",examples=['DFG454353454'])
    sy_zones: str |None = Field("",   title='属地管理行政部门所在地地区',  description=" 属地管理行政部门所在地地区",examples=['铁西区'])
    social_credit_code: str |None = Field("",   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656'])
    postal_code: str |None = Field("",   title='邮政编码',  description=" 邮政编码",examples=['4587236'])
    detailed_address: str |None = Field("",   title='详细地址',  description=" 详细地址",examples=['FSDFSDFSDF234E23'])
    related_license_upload: str |None = Field("",   title='相关证照上传',  description=" 相关证照上传",examples=[''])
    long: str |None = Field("",   title='所在经度',  description=" 所在经度",examples=['201.22'])
    lat: str |None = Field("",   title='所在纬度',  description=" 所在纬度",examples=['65.33'])
    urban_rural_nature: str |None = Field("",   title='城乡性质',  description=" 城乡性质",examples=['城镇'])
    location_economic_attribute: str |None = Field("",   title='所在地经济属性',  description=" 所在地经济属性",examples=['镇'])
    urban_ethnic_nature: str |None = Field("",   title='所在地民族属性',  description="",examples=[''])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])
    is_entity: bool |None = Field(None,   title='是否实体',  description=" 是否实体",examples=[''])

    website_url: str |None = Field("",   title='网址',  description=" 网址",examples=['WWW.BDIUFD.COM'])
    status: str |None = Field("",   title='状态',  description=" 状态",examples=[''])
    membership_no: str |None = Field("",   title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    membership_category: str |None = Field("",   title='隶属单位类型',  description=" 隶属单位类型",examples=['行政'])
    workflow_status: str |None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int|None= Query(0, title="", description="", example='1')
    block: str |None = Query("", title=" ", description="地域管辖区", ),
    borough: str |None = Query("", title="  ", description=" 行政管辖区", ),

class InstitutionKeyInfo(BaseModel):
    # 如果 不一样 需要转换到orm模型的
    id:int= Query(None, title="", description="", example='1')
    school_name: str = Field(...,alias='institution_name', title='单位名称',  examples=['文化部'])
    school_no: str = Field(..., alias='institution_code',  title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    # institution_name: str |None = Field(..., title='单位名称',  examples=['文化部'])
    # institution_code: str |None = Field(...,   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    membership_no: str |None = Field(...,   title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    block: str |None = Query("", title=" ", description="地域管辖区", ),
    borough: str |None = Query("", title="  ", description=" 行政管辖区", ),
    status: str |None = Field(PlanningSchoolStatus.DRAFT,   title='状态',  description=" 状态",examples=[''])
    social_credit_code: str|None = Field( '',   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656']),

    # school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])
    # borough:str=Query('', title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    # block: str = Query('', title=" Author", description="地域管辖区",examples=['铁西区'])
    # school_name: str = Query('', title="学校名称", description="园所名称",examples=['XX小学'])
    # school_type: str = Query('', title="", description=" 学校类型",examples=['中小学'])
    school_edu_level: str|None = Query('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_category: str|None = Query('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Query('', title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    school_level: str|None = Query(None, title="", description=" 学校星级",examples=['5'])

class InstitutionPageSearch(BaseModel):
    social_credit_code: str|None = Field( '',   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656']),
    block: str = Query("", title=" ", description="地域管辖区", ),
    school_code: str = Query("", title=" ", description="", ),
    school_level: str = Query("", title=" ", description="", ),
    planning_school_code: str = Query("", title="", description=" 园所标识码", ),
    planning_school_level: str = Query("", title="", description=" 学校星级", ),
    planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),
    planning_school_no: str = Query("", title="学校编号", description="学校编号/园所代码",
                                    max_length=50, ),
    borough: str = Query("", title="  ", description=" 行政管辖区", ),
    status: PlanningSchoolStatus|None = Query("", title="", description=" 状态", examples=['正常']),

    founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                          examples=['地方']),
    founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                        examples=['教育部门']),
    founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                        examples=['县级教育部门']),
    school_no: str|None = Query("", title=" ", description="", ),
    school_name: str|None = Query("", title=" ", description="", ),
    province: str |None= Query("", title=" ", description="", ),
    city: str|None = Query("", title=" ", description="", ),
    planning_school_id: int|None = Query(0, title=" ", description="", ),
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办']),

class InstitutionsAdd(BaseModel):
    #   title  实际根据title匹配
    institution_category: InstitutionType = Field(InstitutionType.INSTITUTION, title='单位分类',  examples=['institution/administration'])
    school_name: str = Field(...,alias='institution_name', title='单位名称',  examples=['文化部'])
    school_no: str = Field(..., alias='institution_code',  title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    membership_no: str = Field(...,     title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    block: str = Query("",   title=" ", description="地域管辖区", ),
    borough: str = Query("",    title="  ", description=" 行政管辖区", ),
    status: str = Field(PlanningSchoolStatus.DRAFT,  alias='',   title='状态',  description=" 状态",examples=[''])
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])

    # school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    # planning_school_id: int = Field(0, title="", description="规划校id",examples=['1'])
    # school_no:str= Query(..., title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    # borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    # block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    # school_edu_level: str|None = Query('', title="", description="办学类型/学校性质",examples=['学前教育'])
    # school_category: str|None = Query('', title="", description=" 办学类型二级",examples=['小学'])
    # school_operation_type: str|None = Query('', title="", description=" 办学类型三级",examples=['附设小学班'])
    # school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    # school_level: str|None = Query(None, title="", description=" 学校星级",examples=['5'])
    # school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])



class InstitutionBaseInfo(BaseModel):
    #  todo 法1 新增时别名方式   获取模型 时 要映射为ins开头的字段  todo 法2  视图映射转换方式 需要支持互转  可改  外部键不变   且 m2v时需要映射
    id:int= Query( 0, title="", description="学校id", example='1')
    school_name: str |None = Field("",alias="institution_name", title='单位名称', description="单位名称",examples=['文化部'])
    institution_type: str |None = Field("",   title='单位类型',  description="单位类型 ",examples=[''])

    institution_en_name: str |None = Field("",title='单位名称英文',   description=" 单位名称英文",examples=['CEDUCUL'])
    institution_category: str |None = Field("", title='单位分类',  description=" 单位分类",examples=['事业单位'])
    sy_zones: str |None = Field("",   title='属地管理行政部门所在地地区',  description=" 属地管理行政部门所在地地区",examples=['铁西区'])
    school_no: str |None = Field("",alias="institution_code",   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    social_credit_code: str|None = Field("",   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['DK156512656'])
    create_date: str |None = Field("",   title='成立年月',  description=" 成立年月",examples=['2020-10-23'])
    leg_repr_name: str |None = Field("",   title='法定代表人姓名',  description=" 法定代表人姓名",examples=['XXX'])
    party_leader_name: str |None = Field("",   title='党组织负责人姓名',  description=" 党组织负责人姓名",examples=['YYY'])
    adm_leader_name: str |None = Field("",   title='行政负责人姓名',  description=" 行政负责人姓名",examples=['GGGG'])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])

    is_entity: bool |None = Field(None,   title='是否实体',  description=" 是否实体",examples=[''])
    detailed_address: str |None = Field("",   title='详细地址',  description=" 详细地址",examples=['FSDFSDFSDF234E23'])
    contact_number: str |None = Field("",   title='联系电话',  description=" 联系电话",examples=['0232156562'])
    postal_code: str |None = Field("",   title='邮政编码',  description=" 邮政编码",examples=['4587236'])
    website_url: str |None = Field("",   title='网址',  description=" 网址",examples=['WWW.BDIUFD.COM'])
    email: str |None = Field("",   title='单位电子信箱',  description=" 单位电子信箱",examples=['fsdfds@odk.cc'])

    fax_number: str |None = Field("",   title='传真电话',  description=" 传真电话",examples=['020-256526256'])
    long: str |None = Field("",   title='所在经度',  description=" 所在经度",examples=['201.22'])
    lat: str |None = Field("",   title='所在纬度',  description=" 所在纬度",examples=['65.33'])
    urban_rural_nature: str |None = Field("",   title='城乡性质',  description=" 城乡性质",examples=['城镇'])
    location_economic_attribute: str |None = Field("",   title='所在地经济属性',  description=" 所在地经济属性",examples=['镇'])
    related_license_upload: str |None = Field("",   title='相关证照上传',  description=" 相关证照上传",examples=[''])
    workflow_status: str|None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int= Query(0, title="", description="", example='1')
    status: str |None = Field( '',   title='状态',  description=" 状态",examples=[''])
    urban_ethnic_nature: str |None = Field("",   title='所在地民族属性',  description="",examples=[''])

    # 下面的待映射
    # school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    school_short_name: str = Field('', title="", description="园所简称",examples=['MXXX'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_school_date: str = Field('', title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field('', title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field('', title="", description="举办者名称",examples=['上海教育局'])
    # urban_rural_nature: str = Field('', title="", description="城乡性质",examples=['城镇'])
    school_edu_level: str|None = Field('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_org_form: str = Field('', title="", description="办学组织形式",examples=['教学点'])
    # school_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    school_category: str|None = Field('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Field('', title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field('', title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    # sy_zones: str = Field('', title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field('', title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    # status: str = Field(None, title="", description=" 状态",examples=[])
    school_en_name: str = Field('', title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    # social_credit_code: str = Field('', title="", description="统一社会信用代码",examples=['XH423423876867'])
    school_closure_date: str = Field('', title="", description="学校关闭日期",examples=[''])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    # location_economic_attribute: str |None= Field(None, title="所属地经济属性", description="", examples=[''])
    # urban_ethnic_nature: str |None= Field(None, title="所在地民族属性", description="", examples=[''])
    # leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])



