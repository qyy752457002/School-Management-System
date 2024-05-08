from fastapi import Query
from pydantic import BaseModel, Field


class SchoolEduInfo(BaseModel):
    """
    学校教育信息

    """

    id: int = Query(None, title="", description="", example='1'),
    school_id: int = Field(0, title="", description="学校id", examples=['1'])

    is_ethnic_school: bool = Field(None, title="", description="是否民族校", examples=[False])
    is_att_class: bool = Field(None, title="", description="是否附设班", examples=[False])
    att_class_type: str = Field(None, title="", description="附设班类型", examples=[])
    is_province_feat: bool = Field(None, title="", description="是否省特色", examples=[False])
    is_bilingual_clas: bool = Field(None, title="", description="是否具有双语教学班", examples=[False])
    minority_lang_code: str = Field(None, title="", description="少数民族语言编码", examples=['是'])
    is_profitable: bool = Field(None, title="", description="是否营利性", examples=[False])
    prof_org_name: str = Field(None, title="", description="营利性机构名称", examples=['是'])
    is_prov_demo: bool = Field(None, title="", description="是否省示范", examples=[False])
    is_latest_year: bool = Field(None, title="", description="是否最新年份", examples=[False])
    is_town_kinderg: bool = Field(None, title="", description="是否乡镇幼儿园", examples=[False])
    is_incl_kinderg: bool = Field(None, title="", description="是否普惠性幼儿园", examples=[False])
    is_affil_school: bool = Field(None, title="", description="是否附属学校", examples=[False])
    affil_univ_code: str = Field(None, title="", description="附属于高校（机构）标识码", examples=['是'])
    affil_univ_name: str = Field(None, title="", description="附属高校（机构）名称", examples=['是'])
    is_last_yr_revok: bool = Field(None, title="", description="是否上年撤销", examples=[False])
    is_school_counted: bool = Field(None, title="", description="是否计校数", examples=[False])


