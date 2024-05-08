from fastapi import Query
from pydantic import BaseModel, Field


class PlanningSchoolEduInfo(BaseModel):
    """
    规划校教育信息
    """

    id: int = Query(None, title="", description="", example='1'),
    planning_school_id: int = Field(None, title="", description="规划校id", examples=['1'])

    is_ethnic_school: str|bool = Field(None, title="", description="是否民族校", examples=['是'])
    is_att_class:  str|bool = Field(None, title="", description="是否附设班", examples=['是'])
    att_class_type: str = Field(None, title="", description="附设班类型", examples=['是'])
    is_province_feat:  str|bool = Field(None, title="", description="是否省特色", examples=['是'])
    is_bilingual_clas:  str|bool = Field(None, title="", description="是否具有双语教学班", examples=['是'])
    minority_lang_code: str = Field(None, title="", description="少数民族语言编码", examples=['是'])
    is_profitable:  str|bool = Field(None, title="", description="是否营利性", examples=['是'])
    prof_org_name: str = Field(None, title="", description="营利性机构名称", examples=['是'])
    is_prov_demo:  str|bool = Field(None, title="", description="是否省示范", examples=['是'])
    is_latest_year:  str|bool = Field(None, title="", description="是否最新年份", examples=['是'])
    is_town_kinderg:  str|bool = Field(None, title="", description="是否乡镇幼儿园", examples=['是'])
    is_incl_kinderg:  str|bool = Field(None, title="", description="是否普惠性幼儿园", examples=['是'])
    is_affil_school:  str|bool = Field(None, title="", description="是否附属学校", examples=['是'])
    affil_univ_code: str = Field(None, title="", description="附属于高校（机构）标识码", examples=['是'])
    affil_univ_name: str = Field(None, title="", description="附属高校（机构）名称", examples=['是'])
    is_last_yr_revok:  str|bool = Field(None, title="", description="是否上年撤销", examples=['是'])
    is_school_counted:  str|bool = Field(None, title="", description="是否计校数", examples=['是'])
  
