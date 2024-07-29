from datetime import datetime, date

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Organization(BaseModel):
    """
     org_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="组织分类 行政类等")

    org_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="组织或者部门名称 例如行政部")
    parent_id: Mapped[int] = mapped_column( comment="父级ID",default=0,nullable=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID",default=0,nullable=True)
    member_cnt: Mapped[int] = mapped_column( comment="人数",default=0,nullable=True)
    """
    id:int|str= Query(None, title="", description="id", example='1')
    school_id: int |str= Field(None, title="", description="学校id",examples=['1'])

    org_type: str = Field(None, title="", description="组织分类 行政类等",examples=['行政类'])
    org_name: str = Field(None, title="", description="组织或者部门名称 例如行政部",examples=['行政部'])
    org_code: str|None = Field(None, title="", description=" ",examples=[''])
    parent_id: int|str = Field(None, title="", description="父级ID",examples=['0'])
    member_cnt: int = Field(None, title="", description="人数",examples=['0'])
    created_at: str|None|date|datetime = Field(None, title="", description=" ",examples=[''])
    updated_at: str|None|date|datetime = Field(None, title="", description=" ",examples=[''])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'parent_id','teacher_id','org_id']
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



class OrganizationMembers(BaseModel):
    """
    org_id: Mapped[int] = mapped_column( comment="部门ID",default=0,nullable=True)
    # 要求 这里出现的所有人必须在 教师表里有

    """
    id:int|str= Query(None, title="", description="id", example='1')
    org_id: int|str = Field(None, title="", description="部门ID",examples=['1'])
    teacher_id: int|str = Field(None, title="", description="教师ID",examples=['1'])
    member_type: str = Field(None, title="", description="成员类型/岗位 例如老师 领导 职工等",examples=['老师'])
    identity: str = Field(None, title="", description="身份",examples=['学生'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "org_id",'teacher_id',]
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


class OrganizationMembersSearchRes(BaseModel):
    """

    """
    id:int|str= Query(None, title="", description="id", example='1')
    org_id: int|str = Field(None, title="", description="部门ID",examples=['1'])
    teacher_id: int |str= Field(None, title="", description="教师ID",examples=['1'])
    member_name: str|None = Field(None, title="", description="姓名",examples=['张三'])
    member_type: str|None = Field(None, title="", description="成员类型/岗位 例如老师 领导 职工等",examples=['老师'])
    birthday: str|datetime|None = Field(None, title="", description="生日",examples=['1990-01-01'])
    gender: str|None = Field(None, title="", description="性别",examples=['男'])
    mobile: str|None = Field(None, title="", description="手机",examples=['13800000000'])
    card_type: str|None = Field(None, title="", description="证件类型",examples=['身份证'])
    card_number: str|None = Field(None, title="", description="证件号码",examples=['123456789012345678'])
    identity: str|None = Field(None, title="", description="身份",examples=['学生'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "org_id",'teacher_id',]
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



