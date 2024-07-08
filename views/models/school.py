from typing import List

from fastapi import Query
from pydantic import BaseModel, Field, model_validator

from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType


class School(BaseModel):
    id:int|str= Query(None, title="", description="学校id", example='1')
    planning_school_id: int |str= Field(None, title="", description="规划校id",examples=['1'])
    school_name: str = Field(..., title="学校名称", description="学校名称",examples=['XX小学'])
    school_no: str = Field(..., title="学校编号", description="学校编号",examples=['SC2032633'])
    school_operation_license_number: str = Field(..., title=" Description", description="办学许可证号",examples=['EDU2024012569'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    borough: str = Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    school_edu_level: str|None = Field(..., title="", description="办学类型",examples=['学前教育'])
    school_category: str|None = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Field(..., title="", description=" 学校办别",examples=['民办'])
    school_level: str |None= Field(None, title="", description=" 学校星级",examples=['5'])
    status: str = Field(..., title="", description=" 状态",examples=['正常'])
    school_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    kg_level: str|None = Field(None, title="", description="星级",examples=['5'])
    created_uid: int  = Field(..., title="", description="创建人",examples=['1'])
    school_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    school_en_name: str = Field(..., title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    create_school_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    social_credit_code: str = Field(None, title="", description="统一社会信用代码",examples=['XH423423876867'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_type_lv2: str = Field(..., title="", description="举办者类型二级",examples=['教育部门'])
    founder_type_lv3: str = Field(..., title="", description="举办者类型三级",examples=['县级教育部门'])
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
    workflow_status: str |None= Field(None, title="", description="", examples=[''])
    location_economic_attribute: str |None= Field(None, title="所属地经济属性", description="", examples=[''])
    urban_ethnic_nature: str |None= Field(None, title="所在地民族属性", description="", examples=[''])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "planning_school_id",]
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

# 学校的 基本信息模型   视图的额模型是按需提供的
class SchoolBaseInfoOptional(BaseModel):
    id:int|str= Query(0, title="", description="学校id", example='1')
    school_name: str = Field( '', title="学校名称", description="1-20字符",examples=['XX小学'])
    school_short_name: str = Field('', title="", description="园所简称",examples=['MXXX'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_school_date: str = Field('', title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field('', title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field('', title="", description="举办者名称",examples=['上海教育局'])
    urban_rural_nature: str = Field('', title="", description="城乡性质",examples=['城镇'])
    school_edu_level: str |None= Field('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_org_form: str = Field('', title="", description="办学组织形式",examples=['教学点'])
    school_category: str|None = Field('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Field('', title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field('', title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field('', title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field('', title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description=" 状态",examples=['正常'])
    school_en_name: str = Field('', title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    social_credit_code: str = Field('', title="", description="统一社会信用代码",examples=['XH423423876867'])
    school_closure_date: str = Field('', title="", description="学校关闭日期",examples=[''])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    process_instance_id:int= Query(0, title="", description="", example='1')
    workflow_status: str |None= Field(None, title="", description="", examples=[''])
    location_economic_attribute: str |None= Field(None, title="所属地经济属性", description="", examples=[''])
    urban_ethnic_nature: str |None= Field(None, title="所在地民族属性", description="", examples=[''])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])
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


# 学校的 基本信息模型   视图的额模型是按需提供的
class SchoolBaseInfo(BaseModel):
    id:int|str= Query(..., title="", description="学校id", example='1')
    school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    school_short_name: str = Field('', title="", description="园所简称",examples=['MXXX'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_school_date: str = Field('', title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field('', title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field('', title="", description="举办者名称",examples=['上海教育局'])
    urban_rural_nature: str = Field('', title="", description="城乡性质",examples=['城镇'])
    school_edu_level: str|None = Field('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_org_form: str = Field('', title="", description="办学组织形式",examples=['教学点'])
    # school_nature: str = Field('', title="", description="学校性质",examples=['学前'])

    school_category: str|None = Field('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Field('', title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field('', title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field('', title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field('', title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description=" 状态",examples=[])
    school_en_name: str = Field('', title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    social_credit_code: str = Field('', title="", description="统一社会信用代码",examples=['XH423423876867'])
    school_closure_date: str = Field('', title="", description="学校关闭日期",examples=[''])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    location_economic_attribute: str |None= Field(None, title="所属地经济属性", description="", examples=[''])
    urban_ethnic_nature: str |None= Field(None, title="所在地民族属性", description="", examples=[''])
    leg_repr_certificatenumber: str |None = Field("",   title='法人证书号',  description=" 法人证书号",examples=['DF1256565656'])
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


class SchoolKeyInfo(BaseModel):
    id:int|str= Query(None, title="", description="学校id", example='1')

    school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    planning_school_id: int|str = Field(None, title="", description="规划校id",examples=['1'])
    borough:str=Query('', title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    block: str = Query('', title=" Author", description="地域管辖区",examples=['铁西区'])
    school_name: str = Query('', title="学校名称", description="园所名称",examples=['XX小学'])
    # school_type: str = Query('', title="", description=" 学校类型",examples=['中小学'])
    school_edu_level: str|None = Query('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_category: str|None = Query('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Query('', title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Query('', title="", description=" 学校办别",examples=['民办'])
    school_level: str|None = Query(None, title="", description=" 学校星级",examples=['5'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", 'planning_school_id']
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

class SchoolKeyAddInfo(BaseModel):
    id:int|str= Field(None, title="", description="学校id", example='1')
    school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    planning_school_id: int|str = Field(0, title="", description="规划校id",examples=['1'])
    school_no:str= Field(..., title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633')
    borough:str=Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    school_edu_level: str|None = Field('', title="", description="办学类型/学校性质",examples=['学前教育'])
    school_category: str|None = Field('', title="", description=" 办学类型二级",examples=['小学'])
    school_operation_type: str|None = Field('', title="", description=" 办学类型三级",examples=['附设小学班'])
    school_org_type: str = Field('', title="", description=" 学校办别",examples=['民办'])
    school_level: str|None = Field(None, title="", description=" 学校星级",examples=['5'])
    school_code: str = Field('', title="", description=" 园所标识码",examples=['SC562369322SG'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data):
        _change_list= ["id",'planning_school_id' ]
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

class SchoolTask(BaseModel):
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])

class SchoolPageSearch(BaseModel):
    # process_code: str = Query("", title=" ", description="", ),
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
    planning_school_id: int|str|None = Query(0, title=" ", description="", ),
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["planning_school_id", ]
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

