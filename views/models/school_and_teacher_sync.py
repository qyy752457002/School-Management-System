from typing import List

from fastapi import Query
from pydantic import BaseModel, Field, model_validator

from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.system import InstitutionType
from typing import Optional


class SchoolSyncQueryModel(BaseModel):
    """
    这是同步查询的model
    """
    school_name: str = Query("", title="学校名称", description="1-20字符", examples=['XX小学'])
    borough: str | None = Query("", title="  ", description=" 行政管辖区", )
    block: str | None = Query("", title=" ", description="地域管辖区", )
    social_credit_code: str | None = Query(None, title="", description="统一社会信用代码",
                                           examples=['XH423423876867'])
    school_edu_level: str | None = Query('', title="", description="办学类型/教育层次", examples=['学前教育'])
    school_category: str | None = Query('', title="", description=" 办学类型二级/学校（机构）类别", examples=['小学'])
    school_operation_type: str | None = Query('', title="", description=" 办学类型三级/办学类型",
                                              examples=['附设小学班'])


class SchoolSyncQueryReModel(BaseModel):
    """
    这是同步查询返回的model
    """

    social_credit_code: str = Field(..., title="", description="统一社会信用代码",
                                    examples=['XH423423876867'])
    school_name: str = Field(..., title="学校名称", description="1-20字符", examples=['XX小学'])
    borough: str = Query(..., title="  ", description=" 行政管辖区", )
    block: str = Query(..., title=" ", description="地域管辖区", )
    founder_type: str = Field(..., title="", description="举办者类型",examples=['地方'])
    founder_type_lv2: str = Field(..., title="", description="举办者类型二级",examples=['教育部门'])
    founder_type_lv3: str = Field(..., title="", description="举办者类型三级",examples=['县级教育部门'])




class SupervisorSyncQueryModel(BaseModel):
    """
    同步查询的模型
    """
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名")
    school_name: Optional[int | str] = Query("", title="单位", alias="supervisor_employer", description="单位")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="身份证件类型")
    teacher_id_number: Optional[str] = Query("", title="身份证件号", description="身份证件号")
    mobile: Optional[str] = Query("", title="联系电话", description="联系电话")
    teacher_gender: Optional[str] = Query("", title="性别", description="性别")


class SupervisorSyncQueryReModel(BaseModel):
    """
    同步查询返回的模型
    """
    teacher_name: str = Field(..., title="姓名", description="姓名")
    school_name: str = Field(..., title="单位", description="单位")
    borough: str = Field(..., title="单位所在区县", description="单位所在区县")
    teacher_id_type: str = Field(..., title="身份证件类型", description="身份证件类型")
    teacher_id_number: str = Field(..., title="身份证件号", description="身份证件号")
    mobile: str = Field(..., title="联系电话", description="联系电话")
    teacher_gender: str = Field(..., title="性别", description="性别")
    current_technical_position: str = Field("", title="职称", description="职称")
    staff_category: str = Field("", title="职务", description="职务")
