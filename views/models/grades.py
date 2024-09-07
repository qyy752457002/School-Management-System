from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Grades(BaseModel):
    """
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码/中职用枚举")
    course_no_lv2: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码2")
    course_no_lv3: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码3")
    sort_number: Mapped[int] = mapped_column(nullable=True,default=0, comment="排序序号")

    """
    grade_name: str|None = Field('', title="",description="年级名称",examples=['一年级'])
    grade_type: str|None = Field('',  description="年级类型/班级类型 例如 一年级 二年级 三年级",examples=['一年级'])
    school_type: str|None = Field('',  description="教育阶段/学校类别 例如 小学 初中",examples=['小学'])

    grade_alias: str|None = Field('',  description="年级别名",examples=['一年级'])
    school_id: int|str = Field(0, title="学校ID", description="学校ID",examples=[0])
    grade_no: str|None = Field("", title="年级编号", description="年级编号",examples=['一年级'])
    course_no: str|None = Field("", title="", description="学科编码/中职用枚举",examples=['19'])
    course_no_lv2: str|None = Field("", title="", description="学科编码2",examples=['19'])
    course_no_lv3: str|None = Field("", title="", description="学科编码3",examples=['19'])

    city: str|None = Field("", title="", description="",examples=[''])
    district: str|None = Field("", title="", description="",examples=[''])
    sort_number: int|None = Field(None, title="", description="排序序号",examples=[0])

    study_section: str|None = Field("", title="", description="",examples=[''])
    is_enabled: bool|None = Field(True, title="", description="是否启用",examples=[True])
    is_graduation_grade: bool|None = Field(True, title="", description="是否毕业年级",examples=[True])

    description: str|None = Field('',  description="简介",examples=['fsdfdsfsdxxx'])
    created_at: datetime = Field('',  description="简介",examples=['2020-01-01'])
    id:int|str= Field(0, title="", description="id", example='1')
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'',]
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                # data[_change] = str(data[_change])
                pass
            else:
                pass
        return data

