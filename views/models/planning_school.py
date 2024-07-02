from enum import Enum
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel, Field

from models.student_transaction import AuditAction
from views.models.planning_school_communications import PlanningSchoolCommunications


class PlanningSchoolFounderType(str, Enum):
    """
    举办者类型 一级
    规划校性质
    """
    LOCAL = "regional"
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
    id: int = Query(None, title="规划校id", description="规划校id", example='1'),

    planning_school_name: str = Field(..., title="规划校名称", description="1-20字符", examples=['XX小学'])
    planning_school_no: str = Field(..., title="规划校编号", description="规划校编号/规划校代码", examples=['SC2032633'])
    planning_school_operation_license_number: str = Field(..., title="办学许可证号",
                                                          description="办学许可证号", examples=['EDU2024012569'])
    block: str = Field(..., title="地域管辖区", description="地域管辖区", examples=['铁西区'])
    borough: str = Field(..., title="行政管辖区", description=" 行政管辖区", examples=['铁西区'])
    planning_school_edu_level: str|None = Field(..., title="办学类型", description="办学类型", examples=['学前教育'])
    planning_school_category: str|None = Field(..., title="办学类型二级", description=" 办学类型二级", examples=['小学'])
    planning_school_operation_type: str|None = Field(..., title="办学类型三级", description=" 办学类型三级", examples=['附设小学班'])
    planning_school_org_type: str = Field(..., title="规划校办别", description=" 规划校办别", examples=['民办'])
    planning_school_level: str|int|None = Field(None, title="规划校星级", description=" 规划校星级", examples=['5'])
    status: str = Field(..., title="状态", description=" 状态", examples=['正常'])
    planning_school_code: str = Field(..., title="规划校标识码", description=" 规划校标识码", examples=['SC562369322SG'])
    kg_level: str|None = Field(None, title="星级", description="星级", examples=['5'])
    created_uid: int = Field(..., title="创建人", description="创建人", examples=['1'])
   
    planning_school_short_name: str = Field(..., title="规划校简称", description="规划校简称", examples=['MXXX'])
    planning_school_en_name: str = Field(..., title="规划校英文名称", description="规划校英文名称", examples=['MinxingPrimarySCHOOL'])
    create_planning_school_date: str = Field(..., title="建校年月", description="建校年月", examples=['2021-10-10 00:00:00'])
    social_credit_code: str = Field(..., title="统一社会信用代码", description="统一社会信用代码", examples=['XH423423876867'])
    founder_type: str = Field(..., title="举办者类型", description="举办者类型", examples=['地方'])
    founder_type_lv2: str = Field(..., title="举办者类型二级", description="举办者类型二级", examples=['教育部门'])

    founder_type_lv3: str = Field(..., title="举办者类型三级", description="举办者类型三级", examples=['县级教育部门'])

    founder_name: str = Field(..., title="举办者名称", description="举办者名称", examples=['上海教育局'])
    founder_code: str = Field(..., title="举办者识别码", description="举办者识别码", examples=['SC562369322SG'])
    urban_rural_nature: str = Field(..., title="城乡性质", description="城乡性质", examples=['城镇'])
    planning_school_org_form: str = Field(..., title="办学组织形式", description="办学组织形式", examples=['教学点'])
    planning_school_closure_date: str = Field('', title="规划校关闭日期", description="规划校关闭日期", examples=[''])
    department_unit_number: str = Field(..., title="属地管理行政部门单位号", description="属地管理行政部门单位号", examples=['SC562369322SG'])
    sy_zones: str = Field(..., title="属地管理行政部门所在地地区", description="属地管理行政部门所在地地区", examples=['铁西区'])
    historical_evolution: str = Field(..., title="历史沿革", description="历史沿革", examples=['xxxxxxxxxxxxxxxxxxxx'])
    sy_zones_pro: str = Field(..., title="属地管理教育行政部门所在地（省级）", description="属地管理教育行政部门所在地（省级）", examples=['沈阳'])
    primary_planning_school_system: str = Field(..., title="小学学制", description="小学学制", examples=['6'])
    primary_planning_school_entry_age: str = Field(..., title="小学入学年龄", description="小学入学年龄", examples=['6'])
    junior_middle_planning_school_system: str = Field(..., title="初中学制", description="初中学制", examples=['3'])
    junior_middle_planning_school_entry_age: str = Field(..., title="初中入学年龄", description="初中入学年龄", examples=['12'])
    senior_middle_planning_school_system: str = Field(..., title="高中学制", description="高中学制", examples=['3'])
    province: str|None= Field('', title="省份", description="", examples=[''], max_length=30)
    city: str|None = Field('', title="城市", description="", examples=[''],  max_length=30)
    workflow_status: str |None= Field(None, title="", description="", examples=[''])

# 规划校的 基本信息模型   视图的额模型是按需提供的
class PlanningSchoolBaseInfo(BaseModel):
    id: int = Query(None, title="", description="规划校id", example='1'),
    planning_school_name: str = Query(..., title="规划校名称", description="1-20字符", examples=['XX小学'])
    planning_school_short_name: str = Query(..., title="", description="规划校简称", examples=['MXXX'])
    planning_school_code: str = Query(..., title="", description=" 规划校标识码", examples=['SC562369322SG'])
    create_planning_school_date: str = Query(..., title="", description="建校年月", examples=['2021-10-10 00:00:00'])
    founder_type: str = Query(..., title="", description="举办者类型", examples=['地方'])
    founder_type_lv2: str = Query(..., title="", description="举办者类型二级", examples=['教育部门'])

    founder_type_lv3: str = Query(..., title="", description="举办者类型三级", examples=['县级教育部门'])
    founder_name: str = Query(..., title="", description="举办者名称", examples=['上海教育局'])
    urban_rural_nature: str = Query(..., title="", description="城乡性质", examples=['城镇'])
    planning_school_edu_level: str|None = Query(..., title="", description="办学类型/规划校性质", examples=['学前教育'])
    # planning_school_nature: str = Query('', title="", description="规划校性质", examples=['学前'])

    planning_school_org_form: str = Query(..., title="", description="办学组织形式", examples=['教学点'])
    social_credit_code: str = Query(..., title="", description="统一社会信用代码", examples=['XH423423876867'])
    planning_school_en_name: str = Query(..., title="", description="规划校英文名称", examples=['MinxingPrimarySCHOOL'])
    founder_code: str = Query(..., title="", description="举办者识别码", examples=['SC562369322SG'])
    planning_school_closure_date: str = Query('', title="", description="规划校关闭日期", examples=[''])
    planning_school_org_type: str = Query(..., title="", description=" 规划校办别", examples=['民办'])

    planning_school_category: str |None= Query(..., title="", description=" 办学类型二级", examples=['小学'])
    planning_school_operation_type: str |None= Query(..., title="", description=" 办学类型三级", examples=['附设小学班'])
    department_unit_number: str = Query(..., title="", description="属地管理行政部门单位号", examples=['SC562369322SG'])
    sy_zones: str = Query(..., title="", description="属地管理行政部门所在地地区", examples=['铁西区'])
    historical_evolution: str = Query(..., title="", description="历史沿革", examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Query(None, title="", description="", examples=[''])


# 规划校的 基本信息模型   视图的额模型是按需提供的
class PlanningSchoolBaseInfoOptional(BaseModel):
    id: int = Query(None, title="", description="规划校id", example='1'),
    planning_school_name: str = Field(None, title="规划校名称", description="1-20字符", examples=['XX小学'])
    planning_school_short_name: str = Field(None, title="", description="规划校简称", examples=['MXXX'])
    planning_school_code: str = Field(None, title="", description=" 规划校标识码", examples=['SC562369322SG'])
    create_planning_school_date: str = Field(None, title="", description="建校年月", examples=['2021-10-10 00:00:00'])
    founder_type: str = Field(None, title="", description="举办者类型", examples=['地方'])
    founder_type_lv2: str = Field(None, title="", description="举办者类型二级", examples=['教育部门'])

    founder_type_lv3: str = Field(None, title="", description="举办者类型三级", examples=['县级教育部门'])
    founder_name: str = Field(None, title="", description="举办者名称", examples=['上海教育局'])
    urban_rural_nature: str = Field(None, title="", description="城乡性质", examples=['城镇'])
    planning_school_edu_level: str|None = Field(None, title="", description="办学类型/规划校性质", examples=['学前教育'])
    # planning_school_nature: str = Field('', title="", description="规划校性质", examples=['学前'])

    planning_school_org_form: str = Field(None, title="", description="办学组织形式", examples=['教学点'])
    social_credit_code: str = Query('', title="", description="统一社会信用代码", examples=['XH423423876867'])
    planning_school_en_name: str = Query('', title="", description="规划校英文名称", examples=['MinxingPrimarySCHOOL'])
    founder_code: str = Query('', title="", description="举办者识别码", examples=['SC562369322SG'])
    planning_school_closure_date: str = Query('', title="", description="规划校关闭日期", examples=[''])
    planning_school_org_type: str = Query('', title="", description=" 规划校办别", examples=['民办'])

    planning_school_category: str|None = Field(None, title="", description=" 办学类型二级", examples=['小学'])
    planning_school_operation_type: str|None = Field(None, title="", description=" 办学类型三级",
                                                    examples=['附设小学班'])
    department_unit_number: str = Field(None, title="", description="属地管理行政部门单位号",
                                        examples=['SC562369322SG'])
    sy_zones: str = Field(None, title="", description="属地管理行政部门所在地地区", examples=['铁西区'])
    historical_evolution: str = Field(None, title="", description="历史沿革", examples=['xxxxxxxxxxxxxxxxxxxx'])
    status: str = Field(None, title="", description="", examples=[''])
    workflow_status: str|None = Field(None, title="", description="", examples=[''])
    process_instance_id: int = Field(None, title="", description="", examples=[''])


class PlanningSchoolKeyAddInfo(BaseModel):
    id: int = Query(None, title="", description="规划校id", example='1')

    planning_school_name: str = Field(..., title="规划校名称", description="规划校名称", min_length=1, max_length=30,
                                      examples=['XX小学'])
    planning_school_no: str = Query(None, title="规划校编号", description="规划校编号/规划校代码", min_length=1,
                                    max_length=20, example='SC2032633')
    planning_school_code: str = Field('', title="", description=" 规划校标识码", examples=['SC562369322SG'], min_length=1,
                                      max_length=30)
    borough: str = Query(..., title=" Author Email", description=" 行政管辖区", examples=['铁西区'], min_length=1,
                         max_length=30)
    block: str = Query(..., title=" Author", description="地域管辖区", examples=['铁西区'], min_length=1, max_length=30)
    province: str|None = Query('', title=" ", description="", examples=[''],  max_length=30)
    city: str |None= Query('', title=" ", description="", examples=[''],   max_length=30)

    # planning_school_type: str = Query(..., title="", description=" 规划校类型", examples=['中小学'])
    planning_school_edu_level: str|None = Query(..., title="", description="办学类型/规划校性质", examples=['学前教育'])
    planning_school_category: str|None = Query(..., title="", description=" 办学类型二级", examples=['小学'])
    planning_school_operation_type: str|None = Query(..., title="", description=" 办学类型三级", examples=['附设小学班'])
    planning_school_org_type: str = Query(..., title="", description=" 规划校办别", examples=['民办'])
    planning_school_level: str|None = Query(None, title="", description=" 规划校星级", examples=['5'])


class PlanningSchoolKeyInfo(BaseModel):
    id: int = Query(None, title="规划校id", description="规划校id", example='1'),
    planning_school_name: str = Field(..., title="规划校名称", description="1-20字符", examples=['XX小学'])
    planning_school_no: str = Query(None, title="规划校编号", description="规划校编号/规划校代码", min_length=1,
                                    max_length=20, example='SC2032633'),
    borough: str = Query(..., title=" 行政管辖区", description=" 行政管辖区", examples=['铁西区']),
    block: str = Query(..., title=" 地域管辖区", description="地域管辖区", examples=['铁西区']),
    # planning_school_type: str = Query(..., title="", description=" 规划校类型", examples=['中小学']),
    planning_school_edu_level: str|None = Query(..., title="办学类型", description="办学类型/规划校性质", examples=['学前教育']),
    planning_school_category: str|None = Query(..., title="办学类型二级", description=" 办学类型二级", examples=['小学']),
    planning_school_operation_type: str|None = Query(..., title="办学类型三级", description=" 办学类型三级",
                                                    examples=['附设小学班']),
    planning_school_org_type: str = Query(..., title="规划校办别", description=" 规划校办别", examples=['民办']),
    planning_school_level: str|None = Query(None, title="规划校星级", description=" 规划校星级", examples=['5'])


class PlanningSchoolPageSearch(BaseModel):
    # process_code: str = Query("", title=" ", description="", ),
    block: str = Query("", title=" ", description="地域管辖区", ),
    planning_school_code: str = Query("", title="", description=" 园所标识码", ),
    planning_school_level: str = Query("", title="", description=" 学校星级", ),
    planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),
    planning_school_no: str = Query("", title="学校编号", description="学校编号/园所代码", min_length=1,
                                    max_length=20, ),
    borough: str = Query("", title="  ", description=" 行政管辖区", ),
    status: PlanningSchoolStatus|None = Query("", title="", description=" 状态", examples=['正常']),

    founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                          examples=['地方']),
    founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                        examples=['教育部门']),
    founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                        examples=['县级教育部门']),

class PlanningSchoolTask(BaseModel):
    file_name: str = Field('', title="",description="",examples=[' '])
    bucket: str = Field('', title="",description="",examples=[' '])
    scene: str = Field('', title="",description="",examples=[' '])

class PlanningSchoolImport(PlanningSchool, PlanningSchoolCommunications):
    pass

class PlanningSchoolTransactionAudit(BaseModel):
    node_id: int = Query(0, description="节点ID", example='2')
    process_instance_id: int = Query(0, description="流程实例ID", example='2')
    transaction_audit_action: AuditAction = Query(..., description="审批的操作",
                                                 example='pass')
    remark: str = Query("", description="审批的备注", min_length=0, max_length=200,
                        example='同意 无误')