from fastapi import Query
from pydantic import BaseModel, Field


class Campus(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    school_id: int = Field(None, title="", description="学校id",examples=['1'])

    campus_name: str = Field(..., title="", description="校区名称",examples=['XX小学xx校区'])
    campus_no: str = Field(..., title="校区编号", description="校区编号",examples=['SC2032633'])
    campus_operation_license_number: str = Field(..., title=" Description", description="办学许可证号",examples=['EDU2024012569'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    borough: str = Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    campus_type: str = Field(..., title="", description=" 校区类型",examples=['中小学'])
    campus_operation_type: str = Field(..., title="", description="办学类型/校区性质",examples=['学前教育'])
    campus_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    campus_operation_type_lv2: str = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    campus_operation_type_lv3: str = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    campus_org_type: str = Field(..., title="", description=" 校区办别",examples=['民办'])
    campus_level: str = Field(..., title="", description=" 校区星级",examples=['5'])
    status: str = Field(..., title="", description=" 状态",examples=['正常'])
    campus_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    kg_level: str = Field(..., title="", description="星级",examples=['5'])

    campus_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    campus_en_name: str = Field(..., title="", description="园所英文名称",examples=['MinxingPrimarycampus'])
    create_campus_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    social_credit_code: str = Field(None, title="", description="统一社会信用代码",examples=['XH423423876867'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field(..., title="", description="举办者名称",examples=['上海教育局'])
    founder_code: str = Field(..., title="", description="举办者识别码",examples=['SC562369322SG'])
    urban_rural_nature: str = Field(..., title="", description="城乡性质",examples=['城镇'])
    campus_org_form: str = Field(..., title="", description="办学组织形式",examples=['教学点'])
    campus_closure_date: str = Field(..., title="", description="校区关闭日期",examples=[''])
    department_unit_number: str = Field(..., title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field(..., title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    sy_zones_pro: str = Field(..., title="", description="属地管理教育行政部门所在地（省级）",examples=['沈阳'])
    primary_campus_system: str = Field(..., title="", description="小学学制",examples=['6'])
    primary_campus_entry_age: str = Field(..., title="", description="小学入学年龄",examples=['6'])
    junior_middle_campus_system: str = Field(..., title="", description="初中学制",examples=['3'])
    junior_middle_campus_entry_age: str = Field(..., title="", description="初中入学年龄",examples=['12'])
    senior_middle_campus_system: str = Field(..., title="", description="高中学制",examples=['3'])
    location_city: str = Field(..., title="", description="校区所在地(省市)",examples=['3'])
    location_district: str = Field(..., title="", description="校区所在地(区县)",examples=['3'])
    campus_leader_name: str = Field(..., title="", description="校区负责人姓名",examples=['3'])

    campus_leader_position: str = Field(..., title="", description="校区负责人职位",examples=['3'])

# 规划校的 基本信息模型   视图的额模型是按需提供的
class CampusBaseInfo(BaseModel):
    id:int= Query(..., title="", description="id", example='1'),
    campus_name: str = Field(..., title="校区名称", description="1-20字符",examples=['XX小学'])
    campus_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    campus_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_campus_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field(..., title="", description="举办者名称",examples=['上海教育局'])
    urban_rural_nature: str = Field(..., title="", description="城乡性质",examples=['城镇'])
    campus_operation_type: str = Field(..., title="", description="办学类型/校区性质",examples=['学前教育'])
    campus_org_form: str = Field(..., title="", description="办学组织形式",examples=['教学点'])
    campus_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    campus_operation_type_lv2: str = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    campus_operation_type_lv3: str = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field(..., title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field(..., title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description=" 状态",examples=['正常'])



class CampusKeyInfo(BaseModel):
    id:int= Query(..., title="", description="校区id", example='1'),
    school_id: int = Field(None, title="", description="规划校id",examples=['1'])
    campus_no:str= Query(None, title="校区编号", description="校区编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
    borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
    block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
    campus_name: str = Query(..., title="校区名称", description="园所名称",examples=['XX小学']),
    campus_type: str = Query(..., title="", description=" 校区类型",examples=['中小学']),
    campus_operation_type: str = Query(..., title="", description="办学类型/校区性质",examples=['学前教育']),
    campus_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
    campus_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
    campus_org_type: str = Query(..., title="", description=" 校区办别",examples=['民办']),
    campus_level: str = Query(..., title="", description=" 校区星级",examples=['5'])
class CampusKeyAddInfo(BaseModel):
    id:int= Query(None, title="", description="学校id", example='1'),
    campus_name: str = Query(..., title="校区名称", description="园所名称",examples=['XX小学']),
    campus_no:str= Query(None, title="校区编号", description="校区编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
    school_id: int = Field(None, title="", description="规划校id",examples=['1'])
    borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
    block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
    campus_type: str = Query(..., title="", description=" 校区类型",examples=['中小学']),
    campus_operation_type: str = Query(..., title="", description="办学类型/校区性质",examples=['学前教育']),
    campus_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
    campus_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
    campus_org_type: str = Query(..., title="", description=" 校区办别",examples=['民办']),
    campus_level: str = Query(..., title="", description=" 校区星级",examples=['5'])
    campus_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])



