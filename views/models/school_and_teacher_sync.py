from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class SchoolType(str, Enum):
    """
    学校：planning_school
    分校：school
    校区：campus
    """
    PLANING_SCHOOL = "planning_school"
    SCHOOL = "school"
    CAMPUS = "campus"

    @classmethod
    def to_list(cls):
        return [cls.SCHOOL, cls.CAMPUS, cls.PLANING_SCHOOL]


class SchoolSyncQueryModel(BaseModel):
    """
    这是同步查询的model
    """
    school_name: str = Query("", title="学校名称", description="1-20字符", examples=['XX小学'])
    borough: str | None = Query("", title="  ", description=" 行政管辖区", )
    block: str | None = Query("", title=" ", description="地域管辖区", )
    social_credit_code: str | None = Query("", title="", description="统一社会信用代码",
                                           examples=['XH423423876867'])
    school_edu_level: str | None = Query('', title="", description="办学类型/教育层次", examples=['学前教育'])
    school_category: str | None = Query('', title="", description=" 办学类型二级/学校（机构）类别", examples=['小学'])
    school_operation_type: str | None = Query('', title="", description=" 办学类型三级/办学类型",
                                              examples=['附设小学班'])
    type: SchoolType = Query(..., title="", description="学校类型", examples=['公办'])


class SchoolSyncQueryReModel(BaseModel):
    """
    这是同步查询返回的model
    """

    social_credit_code: str = Field(..., title="", description="统一社会信用代码",
                                    examples=['XH423423876867'])
    school_no: str = Field(..., title="学校编号", description="1-20字符", examples=['XX小学'])
    school_name: str = Field(..., title="学校名称", description="1-20字符", examples=['XX小学'])
    borough: str = Field(..., title="  ", description=" 行政管辖区", )
    block: str = Field(..., title=" ", description="地域管辖区", )
    founder_type: str = Field(..., title="", description="举办者类型", examples=['地方'])
    founder_type_lv2: str = Field(..., title="", description="举办者类型二级", examples=['教育部门'])
    founder_type_lv3: str = Field(..., title="", description="举办者类型三级", examples=['县级教育部门'])


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


class SchoolInfoSyncModel(BaseModel):
    school_name: str | None = Field("", title="学校名称", description="学校名称", examples=['XX小学'])
    school_no: str | None = Field("", title="", description=" 学校编号", examples=['SC562369322SG'])
    block: str | None = Field("", title=" Author", description="地域管辖区", examples=['铁西区'])
    borough: str | None = Field("", title=" Author Email", description=" 行政管辖区", examples=['铁西区'])
    school_org_type: str | None = Field("", title="", description=" 学校办别", examples=['民办'])
    school_short_name: str | None = Field("", title="", description="学校简称", examples=['MXXX'])
    school_en_name: str | None = Field("", title="", description="学校英文名称", examples=['MinxingPrimarySCHOOL'])
    social_credit_code: str | None = Field("", title="", description="统一社会信用代码", examples=['XH423423876867'])
    urban_rural_nature: str | None = Field("", title="", description="城乡性质", examples=['城镇'])
    school_org_form: str | None = Field("", title="", description="办学组织形式", examples=['教学点'])
    school_edu_level: str | None = Field("", title="", description="办学类型/教育层次", examples=['学前教育'])
    school_category: str | None = Field("", title="", description=" 办学类型二级/学校（机构）类别", examples=['小学'])
    school_operation_type: str | None = Field("", title="", description=" 办学类型三级/办学类型",
                                              examples=['附设小学班'])
    sy_zones: str | None = Field("", title="", description="属地管理行政部门所在地地区", examples=['铁西区'])
    postal_code: str | None = Field(None, title="", description="邮政编码", examples=['472566'])
    detailed_address: str | None = Field(None, title="", description="学校详细地址", examples=['FSDFSD'])
