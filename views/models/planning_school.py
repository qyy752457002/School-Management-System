from enum import Enum
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field



class PlanningSchoolFounderType(str, Enum):
    """
    举办者类型 一级
    """
    LOCAL = "local"
    CENTRAL = "central"

    @classmethod
    def to_list(cls):
        return [cls.LOCAL, cls.CENTRAL]
class SchoolStatus(Enum):
    DRAFT = "draft"
    OPENING = "opening"
    NORMAL = "normal"
    CLOSED = "closed"
class PlanningSchoolStatus(str, Enum):
    """
    状态
    """
    # ALL = "All"
    DRAFT = "draft"
    OPENING = "opening"
    NORMAL = "normal"
    CLOSED = "closed"

    @classmethod
    def to_list(cls):
        return [cls.DRAFT, cls.OPENING, cls.NORMAL, cls.CLOSED]


class PlanningSchool(BaseModel):
    id:int= Query(None, title="", description="规划校id", example='1'),

    planning_school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    planning_school_no: str = Field(..., title="学校编号", description="学校编号/园所代码",examples=['SC2032633'])
    planning_school_operation_license_number: str = Field(..., title=" Description",
                                                 description="办学许可证号",examples=['EDU2024012569'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    borough: str = Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    planning_school_type: str = Field(..., title="", description=" 学校类型",examples=['中小学'])

    planning_school_operation_type: str = Field(..., title="", description="办学类型/学校性质",examples=['学前教育'])
    planning_school_operation_type_lv2: str = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    planning_school_operation_type_lv3: str = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    planning_school_org_type: str = Field(..., title="", description=" 学校办别",examples=['民办'])
    planning_school_level: str = Field(..., title="", description=" 学校星级",examples=['5'])
    status: str = Field(..., title="", description=" 状态",examples=['正常'])
    planning_school_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    kg_level: str = Field(..., title="", description="星级",examples=['5'])
    created_uid: int  = Field(..., title="", description="创建人",examples=['1'])
    # updated_uid: str = Field(..., title="", description="操作人",examples=['21'])
    # created_at: str = Field(..., title="", description="创建时间",examples=['2021-10-10 00:00:00'])
    # updated_at: str = Field(..., title="", description="更新时间",examples=['2021-10-10 00:00:00'])
    # deleted: str = Field(..., title="", description="删除态",examples=['0'])
    planning_school_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    planning_school_en_name: str = Field(..., title="", description="园所英文名称",examples=['MinxingPrimarySCHOOL'])
    create_planning_school_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    social_credit_code: str = Field(..., title="", description="统一社会信用代码",examples=['XH423423876867'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_type_lv2: str = Field(..., title="", description="举办者类型二级",examples=['教育部门'])

    founder_type_lv3: str = Field(..., title="", description="举办者类型三级",examples=['县级教育部门'])

    founder_name: str = Field(..., title="", description="举办者名称",examples=['上海教育局'])
    founder_code: str = Field(..., title="", description="举办者识别码",examples=['SC562369322SG'])
    urban_rural_nature: str = Field(..., title="", description="城乡性质",examples=['城镇'])
    planning_school_org_form: str = Field(..., title="", description="办学组织形式",examples=['教学点'])
    planning_school_closure_date: str = Field(..., title="", description="学校关闭日期",examples=[''])
    department_unit_number: str = Field(..., title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field(..., title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    sy_zones_pro: str = Field(..., title="", description="属地管理教育行政部门所在地（省级）",examples=['沈阳'])
    primary_planning_school_system: str = Field(..., title="", description="小学学制",examples=['6'])
    primary_planning_school_entry_age: str = Field(..., title="", description="小学入学年龄",examples=['6'])
    junior_middle_planning_school_system: str = Field(..., title="", description="初中学制",examples=['3'])
    junior_middle_planning_school_entry_age: str = Field(..., title="", description="初中入学年龄",examples=['12'])
    senior_middle_planning_school_system: str = Field(..., title="", description="高中学制",examples=['3'])

# 规划校的 基本信息模型   视图的额模型是按需提供的
class PlanningSchoolBaseInfo(BaseModel):
    id:int= Query(None, title="", description="规划校id", example='1'),
    planning_school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    planning_school_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    planning_school_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    create_planning_school_date: str = Field(..., title="", description="建校年月",examples=['2021-10-10 00:00:00'])
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_name: str = Field(..., title="", description="举办者名称",examples=['上海教育局'])
    urban_rural_nature: str = Field(..., title="", description="城乡性质",examples=['城镇'])
    planning_school_operation_type: str = Field(..., title="", description="办学类型/学校性质",examples=['学前教育'])
    planning_school_org_form: str = Field(..., title="", description="办学组织形式",examples=['教学点'])

    planning_school_operation_type_lv2: str = Field(..., title="", description=" 办学类型二级",examples=['小学'])
    planning_school_operation_type_lv3: str = Field(..., title="", description=" 办学类型三级",examples=['附设小学班'])
    department_unit_number: str = Field(..., title="", description="属地管理行政部门单位号",examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="", description="属地管理行政部门所在地地区",examples=['铁西区'])
    historical_evolution: str = Field(..., title="", description="历史沿革",examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description="",examples=[''])

class PlanningSchoolKeyInfo(BaseModel):
    id:int= Query(None, title="", description="规划校id", example='1'),

    planning_school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    # planning_school_short_name: str = Field(..., title="", description="园所简称",examples=['MXXX'])
    planning_school_code: str = Field(..., title="", description=" 园所标识码",examples=['SC562369322SG'])
    planning_school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
    borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
    block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
    planning_school_type: str = Query(..., title="", description=" 学校类型",examples=['中小学']),
    planning_school_operation_type: str = Query(..., title="", description="办学类型/学校性质",examples=['学前教育']),
    planning_school_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
    planning_school_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
    planning_school_org_type: str = Query(..., title="", description=" 学校办别",examples=['民办']),
    planning_school_level: str = Query(..., title="", description=" 学校星级",examples=['5'])



class PlanningSchoolPageSearch(BaseModel):
    block: str = Query("", title=" ", description="地域管辖区", ),
    planning_school_code: str = Query("", title="", description=" 园所标识码", )
    planning_school_level: str = Query("", title="", description=" 学校星级", )
    planning_school_name: str = Query("", title="学校名称", description="1-20字符",)
    planning_school_no:str= Query("", title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,),
    borough:str=Query("", title="  ", description=" 行政管辖区", ),
    status: PlanningSchoolStatus = Query("", title="", description=" 状态",examples=['正常'])

    # status: Optional[str] = Query(None,enum=SchoolStatus, title="", description=" 状态", )
    # founder_type: List[ PlanningSchoolFounderType]  = Query("", title="", description="举办者类型",examples=['地方'])
    # founder_type_lv2:  List[ PlanningSchoolFounderType] = Query("", title="", description="举办者类型二级",examples=['教育部门'])
    # founder_type_lv3:  List[ PlanningSchoolFounderType] = Query("", title="", description="举办者类型三级",examples=['县级教育部门'])










