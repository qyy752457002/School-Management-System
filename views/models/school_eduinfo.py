from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class SchoolEduInfo(BaseModel):
    """
    学校教育信息

    """

    id: int | str = Query(None, title="", description="", example='1'),
    school_id: int | str = Field(0, title="", description="学校id", examples=['1'])

    is_ethnic_school: bool | None = Field(None, title="", description="是否民族校", examples=[False])
    is_att_class: bool | None = Field(None, title="", description="是否附设班", examples=[False])
    att_class_type: str | None = Field(None, title="", description="附设班类型", examples=[])
    is_province_feat: bool | None = Field(None, title="", description="是否省特色", examples=[False])
    is_bilingual_clas: bool | None = Field(None, title="", description="是否具有双语教学班", examples=[False])
    minority_lang_code: str | None = Field(None, title="", description="少数民族语言编码", examples=['是'])
    is_profitable: bool | None = Field(None, title="", description="是否营利性", examples=[False])
    prof_org_name: str | None = Field(None, title="", description="营利性机构名称", examples=['是'])
    is_prov_demo: bool | None = Field(None, title="", description="是否省示范", examples=[False])
    is_latest_year: bool | None = Field(None, title="", description="是否最新年份", examples=[False])
    is_town_kinderg: bool | None = Field(None, title="", description="是否乡镇幼儿园", examples=[False])
    is_incl_kinderg: bool | None = Field(None, title="", description="是否普惠性幼儿园", examples=[False])
    is_affil_school: bool | None = Field(None, title="", description="是否附属学校", examples=[False])
    affil_univ_code: str | None = Field(None, title="", description="附属于高校（机构）标识码", examples=['是'])
    affil_univ_name: str | None = Field(None, title="", description="附属高校（机构）名称", examples=['是'])
    is_last_yr_revok: bool | None = Field(None, title="", description="是否上年撤销", examples=[False])
    is_school_counted: bool | None = Field(None, title="", description="是否计校数", examples=[False])
    primary_school_system: str | None = Field(None, title="", description="小学学制", examples=['是'])
    junior_middle_school_system: str | None = Field(None, title="", description="初中学制", examples=['是'])
    senior_middle_school_system: str | None = Field(None, title="", description="高中学制", examples=['是'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["school_id", 'id']
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
