from fastapi import Query
from pydantic import BaseModel, Field


class PlanningSchoolEduInfo(BaseModel):
    """
    规划校教育信息

    是否民族校
is_ethnic_school
是否附设班
is_att_class
附设班类型
att_class_type
是否省特色
is_province_feat
是否具有双语教学班
is_bilingual_clas
少数民族语言编码
minority_lang_code
是否营利性
is_profitable
营利性机构名称
prof_org_name
是否省示范
is_prov_demo
是否最新年份
is_latest_year
是否乡镇幼儿园
is_town_kinderg
是否普惠性幼儿园
is_incl_kinderg
是否附属学校
is_affil_school
附属于高校（机构）标识码
affil_univ_code
附属高校（机构）名称
affil_univ_name
是否上年撤销
is_last_yr_revok
是否计校数
is_school_counted
    """

    id: int = Query(None, title="", description="", example='1'),
    planning_school_id: int = Field(..., title="", description="规划校id", examples=['1'])

    postal_code: str = Field(..., title="", description="邮政编码", examples=['472566'])
