from fastapi import Query
from pydantic import BaseModel, Field


class School(BaseModel):
    id:int= Query(None, title="", description="学校id", example='1')
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])

    school_name: str = Field(..., title="学校名称", description="学校名称",examples=['XX小学'])
    school_no: str = Field(..., title="学校编号", description="学校编号",examples=['SC2032633'])
    school_operation_license_number: str = Field(..., title=" Description", description="办学许可证号",examples=['EDU2024012569'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    borough: str = Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    school_type: str = Field(..., title="", description=" 学校类型",examples=['中小学'])
    school_operation_type: str = Field(..., title="", description="办学类型",examples=['学前教育'])
    school_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    school_operation_type_lv2: str = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type_lv3: str = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Field(..., title="", description=" 学校办别",examples=['民办'])
    school_level: str = Field(..., title="", description=" 学校星级",examples=['5'])
    status: str = Field(..., title="", description=" 状态",examples=['正常'])
    school_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    kg_level: str = Field(..., title="", description="星级",examples=['5'])

    school_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    school_en_name: str = Field(..., title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    create_school_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    social_credit_code: str = Field(None, title="", description="统一社会信用代码",examples=['XH423423876867'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field(..., title="", description="举办者名称",examples=['上海教育局'])
    founder_code: str = Field(..., title="", description="举办者识别码",examples=['SC562369322SG'])
    urban_rural_nature: str = Field(..., title="", description="城乡性质",examples=['城镇'])
    school_org_form: str = Field(..., title="", description="办学组织形式",examples=['教学点'])
    school_closure_date: str = Field(..., title="", description="学校关闭日期",examples=[''])
    department_unit_number: str = Field(..., title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field(..., title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    sy_zones_pro: str = Field(..., title="", description="属地管理教育行政部门所在地（省级）",examples=['沈阳'])
    primary_school_system: str = Field(..., title="", description="小学学制",examples=['6'])
    primary_school_entry_age: str = Field(..., title="", description="小学入学年龄",examples=['6'])
    junior_middle_school_system: str = Field(..., title="", description="初中学制",examples=['3'])
    junior_middle_school_entry_age: str = Field(..., title="", description="初中入学年龄",examples=['12'])
    senior_middle_school_system: str = Field(..., title="", description="高中学制",examples=['3'])

    class Config:
        schema_extra = {
            "example": {
                "school_name": "xx学校",
                "school_no": "EDU202403256",
                "school_operation_license_number": "A school management system",
                "block": "Lfun technical",
                "borough": "cloud@lfun.cn",
                "school_type": "Copyright © 2024 Lfun technical",
                "school_operation_type":"Copyright © 2024 Lfun technical",
                "school_operation_type_lv2": "Copyright © 2024 Lfun technical",
                "school_operation_type_lv3": "Copyright © 2024 Lfun technical",
                "school_org_type": "Copyright © 2024 Lfun technical",
                "school_level": "Copyright © 2024 Lfun technical",
                "school_nature": "Copyright © 2024Lfun technical",
                "status": "Copyright © 2024 Lfun technical",
                "school_code": "Copyright © 2024 Lfun technical",
                "kg_level": "Copyright © 2024 Lfun technical",
                "created_uid": "Copyright © 2024 Lfun technical",
                "updated_uid": "Copyright © 2024 Lfun technical",
                "created_at": "Copyright © 2024 Lfun technical",
                "updated_at": "Copyright © 2024 Lfun technical",
                "deleted": "Copyright © 2024 Lfun technical",
                "school_short_name": "Copyright © 2024 Lfun technical",
                "school_en_name": "Copyright © 2024 Lfun technical",
                "create_school_date": "Copyright © 2024 Lfun technical",
                "social_credit_code": "Copyright © 2024 Lfun technical",
                "founder_type": "Copyright © 2024 Lfun technical",
                "founder_name": "Copyright © 2024 Lfun technical",
                "founder_code": "Copyright © 2024 Lfun technical",
                "urban_rural_nature": "Copyright © 2024 Lfun technical",
                "school_org_form": "Copyright © 2024 Lfun technical",
                "school_closure_date": "Copyright © 2024 Lfun technical",
                "department_unit_number": "Copyright © 2024 Lfun technical",
                "sy_zones": "Copyright © 2024 Lfun technical",
                "historical_evolution": "Copyright © 2024 Lfun technical",
                "sy_zones_pro": "Copyright © 2024 Lfun technical",
                "primary_school_system": "Copyright © 2024 Lfun technical",
                "primary_school_entry_age": "Copyright © 2024 Lfun technical",
                "junior_middle_school_system": "Copyright © 2024 Lfun technical",
                "junior_middle_school_entry_age": "Copyright © 2024 Lfun technical",
                "senior_middle_school_system": "Copyright © 2024 Lfun technical"

            }
        }


# 学校的 基本信息模型   视图的额模型是按需提供的
class SchoolBaseInfo(BaseModel):
    id:int= Query(..., title="", description="学校id", example='1')
    school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    school_short_name: str = Field('', title="", description="园所简称",examples=['MXXX'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_school_date: str = Field('', title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field('', title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field('', title="", description="举办者名称",examples=['上海教育局'])
    urban_rural_nature: str = Field('', title="", description="城乡性质",examples=['城镇'])
    school_operation_type: str = Field('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_org_form: str = Field('', title="", description="办学组织形式",examples=['教学点'])
    school_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    school_operation_type_lv2: str = Field('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type_lv3: str = Field('', title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field('', title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field('', title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field('', title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description=" 状态",examples=['正常'])


class SchoolKeyInfo(BaseModel):
    id:int= Query(None, title="", description="学校id", example='1')

    school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    planning_school_id: int = Field(None, title="", description="规划校id",examples=['1'])
    borough:str=Query('', title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    block: str = Query('', title=" Author", description="地域管辖区",examples=['铁西区'])
    school_name: str = Query('', title="学校名称", description="园所名称",examples=['XX小学'])
    school_type: str = Query('', title="", description=" 学校类型",examples=['中小学'])
    school_operation_type: str = Query('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_operation_type_lv2: str = Query('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type_lv3: str = Query('', title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    school_level: str = Query('', title="", description=" 学校星级",examples=['5'])

class SchoolKeyAddInfo(BaseModel):
    id:int= Query(None, title="", description="学校id", example='1')

    school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    planning_school_id: int = Field(0, title="", description="规划校id",examples=['1'])

    school_no:str= Query(..., title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    school_type: str = Query('', title="", description=" 学校类型",examples=['中小学'])
    school_operation_type: str = Query('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_operation_type_lv2: str = Query('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type_lv3: str = Query('', title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    school_level: str = Query(..., title="", description=" 学校星级",examples=['5'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])


