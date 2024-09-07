from typing import List

from fastapi.params import Query
from pydantic import BaseModel, Field, model_validator

from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.school_communications import SchoolCommunications
from views.models.system import InstitutionType


class Institutions(BaseModel):
    #   title 等 必须和表头一样
    id:int|str= Query(None, title="", description="", example='1')

    institution_name: str = Field(..., title='单位名称', description="单位名称",examples=['文化部'])
    institution_en_name: str = Field(...,title='单位名称英文',   description=" 单位名称英文",examples=['CEDUCUL'])
    institution_category: str = Field(..., title='单位分类',  description=" 单位分类",examples=['事业单位'])
    institution_type: str = Field(...,   title='单位类型',  description="单位类型 ",examples=[''])
    fax_number: str = Field(...,   title='传真电话',  description=" 传真电话",examples=['020-256526256'])
    email: str = Field(...,   title='单位电子信箱',  description=" 单位电子信箱",examples=['fsdfds@odk.cc'])
    contact_number: str = Field(...,   title='联系电话',  description=" 联系电话",examples=['0232156562'])
    area_code: str = Field(...,   title='电话区号',  description=" 电话区号",examples=['020'])
    institution_code: str|None = Field(...,   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    create_date: str = Field(...,   title='成立年月',  description=" 成立年月",examples=['2020-10-23'])
    leg_repr_name: str = Field(...,   title='法定代表人姓名',  description=" 法定代表人姓名",examples=['XXX'])
    party_leader_name: str = Field(...,   title='党组织负责人姓名',  description=" 党组织负责人姓名",examples=['YYY'])
    party_leader_position: str = Field(...,   title='党组织负责人职务',  description=" 党组织负责人职务",examples=['FSDFSD'])
    adm_leader_name: str = Field(...,   title='行政负责人姓名',  description=" 行政负责人姓名",examples=['GGGG'])
    adm_leader_position: str = Field(...,   title='行政负责人职务',  description=" 行政负责人职务",examples=['FSDFSD'])
    department_unit_number: str = Field(...,   title='属地管理行政部门单位号',  description=" 属地管理行政部门单位号",examples=['DFG454353454'])
    sy_zones: str = Field(...,   title='属地管理行政部门所在地地区',  description=" 属地管理行政部门所在地地区",examples=['铁西区'])
    social_credit_code: str|None = Field(...,   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['3'])
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
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", ]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data

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
    id:int|str= Query(None, title="", description="", example='1')

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
    social_credit_code: str |None = Field("",   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['4'])
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
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", ]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class InstitutionPageSearch(BaseModel):
    social_credit_code: str|None = Field( '',   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['5'])
    block: str = Query("", title=" ", description="地域管辖区", )
    school_code: str = Query("", title=" ", description="", )
    school_level: str = Query("", title=" ", description="", )
    planning_school_code: str = Query("", title="", description=" 园所标识码", )
    planning_school_level: str = Query("", title="", description=" 学校星级", )
    planning_school_name: str = Query("", title="学校名称", description="1-20字符", )
    planning_school_no: str = Query("", title="学校编号", description="学校编号/园所代码",
                                    max_length=50, )
    borough: str = Query("", title="  ", description=" 行政管辖区", )
    status: PlanningSchoolStatus|None = Query("", title="", description=" 状态", examples=['正常'])

    founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                          examples=['地方'])
    founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                        examples=['教育部门'])
    founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                        examples=['县级教育部门'])
    school_no: str|None = Query("", title=" ", description="", )
    school_name: str|None = Query("", title=" ", description="", )
    province: str |None= Query("", title=" ", description="", )
    city: str|None = Query("", title=" ", description="", )
    planning_school_id: int|None = Query(0, title=" ", description="", )
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    institution_category: InstitutionType = Query(None, title='单位分类',examples=['institution/administration'])

class InstitutionsImport(BaseModel):
    school_name: str = Field(...,alias='institution_name', title='单位名称',  examples=['文化部'])
    institution_category: InstitutionType|str = Field(InstitutionType.INSTITUTION, title='单位类型',  examples=['institution/administration'])
    borough: str = Field("",    title="行政管辖区", description=" ", ),
    block: str = Field("",   title="地域管辖区", description="", ),
    membership_no: str = Field( '',     title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    social_credit_code: str|None = Field( None,   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['6'])
    create_school_date: str = Field( '',   title='成立时间',  description=" 成立年月",examples=['2020-10-23'])

class InstitutionsAdd(BaseModel):
    #   title  实际根据title匹配
    institution_category: InstitutionType = Field(InstitutionType.INSTITUTION, title='单位分类',  examples=['institution/administration'])
    school_name: str = Field(...,alias='institution_name', title='单位名称',  examples=['文化部'])
    school_no: str|None = Field(..., alias='institution_code',  title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    membership_no: str = Field(...,     title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    block: str = Query("",   title=" ", description="地域管辖区", ),
    borough: str = Query("",    title="  ", description=" 行政管辖区", ),
    status: str = Field(PlanningSchoolStatus.DRAFT,  alias='',   title='状态',  description=" 状态",examples=[''])
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])


class InstitutionKeyInfo(BaseModel):
    # 如果 不一样 需要转换到orm模型的
    id:int|str= Query(None, title="", description="", example='1')
    school_name: str = Field(...,alias='institution_name', title='单位名称',  examples=['文化部'])
    school_no: str|None = Field(..., alias='institution_code',  title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    membership_no: str |None = Field(...,   title='隶属单位号',  description=" 隶属单位号",examples=['DFF1565165656'])
    block: str |None = Field("", title=" ", description="地域管辖区", )
    borough: str |None = Field("", title="  ", description=" 行政管辖区", )
    status: str |None = Field(PlanningSchoolStatus.DRAFT,   title='状态',  description=" 状态",examples=[''])
    social_credit_code: str|None = Field( None,   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['6'])
    planning_school_id: int|str|None = Field(None, title="", description="规划校id",examples=['1'])
    workflow_status: str |None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int|None= Field(0, title="", description="", example='1')
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", ]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data

class InstitutionsWorkflowInfo(BaseModel):
    id:int|str= Query(None, title="", description="", example='1')

    workflow_status: str |None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int|None= Field(0, title="", description="", example='1')

    status: str = Field( '',  alias='',   title='状态',  description=" 状态",examples=[''])
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])


# 基础信息和分页的结果再用
class InstitutionBaseInfo(BaseModel):
    #   法1 新增时别名方式   获取模型 时 要映射为ins开头的字段  todo 法2  视图映射转换方式 需要支持互转  可改  外部键不变   且 m2v时需要映射
    id:int|str= Query( 0, title="", description="学校id", example='1')
    school_name: str |None = Field("",alias="institution_name", title='单位名称', description="单位名称",examples=['文化部'])
    school_org_type: str |None = Field("", alias='institution_type',  title='单位类型',  description="单位类型 ",examples=[''])

    school_en_name: str |None = Field("",alias='institution_en_name',title='单位名称英文',   description=" 单位名称英文",examples=['CEDUCUL'])
    institution_category: str |None = Field("", title='单位分类',  description=" 单位分类",examples=['institution'])
    sy_zones: str |None = Field("",   title='属地管理行政部门所在地地区',  description=" 属地管理行政部门所在地地区",examples=['铁西区'])

    school_no: str |None = Field("",alias="institution_code",   title='机构代码',  description=" 机构代码",examples=['DKE1865656'])
    social_credit_code: str|None = Field("",   title='统一社会信用代码',  description=" 统一社会信用代码",examples=['7'])

    create_school_date: str |None = Field("", alias='create_date',  title='成立年月',  description=" 成立年月",examples=['2020-10-23'])

    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])

    is_entity: bool |None = Field(None,   title='是否实体',  description=" 是否实体",examples=[''])

    urban_rural_nature: str |None = Field("",   title='城乡性质',  description=" 城乡性质",examples=['城镇'])
    location_economic_attribute: str |None = Field("",   title='所在地经济属性',  description=" 所在地经济属性",examples=['镇'])
    workflow_status: str|None = Field("",   title='',  description=" ",examples=[''])
    process_instance_id:int= Query(0, title="", description="", example='1')
    status: str |None = Field( '',   title='状态',  description=" 状态",examples=[''])
    urban_ethnic_nature: str |None = Field("",   title='所在地民族属性',  description="",examples=[''])
    leg_repr_name: str |None= Field(None, title="", description="法定代表人姓名",examples=['XX'])

    admin: str |None = Field("",   title='管理员',  description=" ",examples=[''])
    admin_phone: str |None = Field("",   title='管理员手机',  description=" ",examples=[''])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", ]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data

class InstitutionCommunications(SchoolCommunications):

    school_web_url: str = Field(None,alias='website_url', title="网址", description="网址",examples=['WW.SS.CC'])
