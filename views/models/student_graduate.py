from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class StudentsGraduationCreate(BaseModel):
    """
    状态 毕业      行政属地
    graduation_type: Mapped[str] = mapped_column(String(10), nullable=True, default='', comment="毕业类型")
    borough: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政管辖区")
    """

    student_id: int | str = Field(0, title="学生id", description="学生id", examples=['0'])
    student_name: str = Field('', title="学生姓名", description="学生姓名")
    student_gender: str = Field('', title="性别", description="性别")
    school: str = Field('', title="学校", description="学校")
    school_id: int | None | str = Field(0, title="", description="")
    borough: str = Field('', title="", description="行政属地")
    edu_number: str = Field('', title="", description="学籍号码")
    class_id: int | str = Field(0, title="", description="班级")
    session: str | None = Field(None, title="届别", description="")
    session_id: str | int = Field(0, title="届别id", description="")
    status: str = Field('', title="毕业状态", description="毕业状态")
    graduation_date: str = Field('', title="毕业年份", description="毕业年份")
    graduation_remark: str = Field('', title="毕业备注", description="毕业备注")
    photo: str = Field('', title="照片", description="照片")
    archive_status: bool = Field(False, title="是否已归档", description="是否已归档")
    archive_date: str = Field('', title="归档年份", description="归档年份")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['student_id', 'school_id', 'class_id', 'session_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                pass
            else:
                pass
        return data


class GraduateStudentQueryModel(BaseModel):
    school_id: Optional[int | str] = Query(None, title="", description="")
    student_name: Optional[str] = Query(None, title="学生姓名", description="学生姓名")
    graduation_date_s: Optional[date] = Query(None, title="毕业日期开始", description="毕业日期开始")
    graduation_date_e: Optional[date] = Query(None, title="毕业日期结束", description="毕业日期结束")
    status: Optional[str] = Query(None, title="毕业状态", description="毕业状态")
    archive_status: Optional[bool] = Query(None, title="归档状态", description="归档状态")
    borough: Optional[str] = Query(None, title="行政属地", description="行政属地")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['school_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            else:
                pass
        return data


class GraduateStudentQueryReModel(BaseModel):
    student_id: int | str = Field(0, title="学生id", description="学生id", examples=['0'])
    school_id: int | str = Field(0, title="学校id", description="学校id", examples=['0'])
    student_name: str = Field('', title="学生姓名", description="学生姓名")
    status: str = Field('', title="毕业状态", description="毕业状态")
    archive_status: bool = Field(False, title="是否已归档", description="是否已归档")
    class_name: str = Field('', title="班级", description="班级")
    school: str = Field('', title="学校", description="学校")
    graduation_date: date | None = Field(None, title="毕业日期", description="毕业日期")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['school_id', 'student_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class StudentsGraduationUpdate(BaseModel):
    student_id: int | str = Field(0, title="学生id", description="学生id", examples=['0'])
    student_name: str = Field('', title="学生姓名", description="学生姓名")
    school: str = Field('', title="学校", description="学校")
    school_id: int | None | str = Field(0, title="", description="")
    borough: str = Field('', title="", description="行政属地")
    edu_number: str = Field('', title="", description="学籍号码")
    class_id: int | str = Field(0, title="", description="班级")
    session: str | None = Field(None, title="届别", description="")
    session_id: str | int = Field(0, title="届别id", description="")
    status: str = Field('', title="毕业状态", description="毕业状态")
    graduation_date: str = Field('', title="毕业年份", description="毕业年份")
    graduation_remark: str = Field('', title="毕业备注", description="毕业备注")
    photo: str = Field('', title="照片", description="照片")
    archive_status: bool = Field(False, title="是否已归档", description="是否已归档")
    archive_date: str = Field('', title="归档年份", description="归档年份")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['student_id', 'school_id', 'class_id', 'session_id']
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


class CountySchoolArchiveQueryModel(BaseModel):
    archive_status: Optional[bool] = Query(None, title="归档状态", description="归档状态")
    borough: Optional[str] = Query(None, title="行政属地", description="行政属地")
    school_id: Optional[int | str] = Query(None, title="", description="")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['school_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            else:
                pass
        return data


class CountySchoolArchiveQueryReModel(BaseModel):
    school_id: int | str = Field(0, title="学校id", description="学校id", examples=['0'])
    school: str = Field('', title="学校", description="学校")
    borough: str = Field('', title="行政属地", description="行政属地")
    archive_status: bool = Field(False, title="是否已归档", description="是否已归档")
    graduate_count: int = Field(0, title="毕业人数", description="毕业人数")

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ['school_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data
