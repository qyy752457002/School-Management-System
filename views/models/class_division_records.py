from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class ClassDivisionRecords(BaseModel):
    id:int|str= Query(None, title="", description="id", example='1'),
    school_id: int|str = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int |str= Field(0, title="年级ID", description="年级ID",examples=['1'])
    class_id: int |str= Field(0, title="班级ID", description="班级ID",examples=['1'])
    student_id: int|str = Field(0, title="学生ID", description="学生ID",examples=['1'])
    student_no: str = Field('', title="", description="学生编号",examples=['1'])
    student_name: str = Field('', title="Grade_name",description="学生姓名",examples=['1'])
    status: str = Field('', title="", description="状态",examples=['1'])
    remark: str = Field('', title="", description="备注",examples=['1'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','student_id','class_id']
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



class ClassDivisionRecordsSearchRes(BaseModel):
    id:int|str= Field(0, title="", description="id", example='1')
    enrollment_number: str = Field('', title="", description="报名号",examples=['1'])
    id_type: str = Field('', title="", description="身份证件类型",examples=['1'])
    student_name: str = Field('', title="", description="姓名",examples=['1'])
    created_at: datetime|None = Field(None, title="", description="分班时间",examples=['1'])
    student_gender: str = Field('', title="", description="性别",examples=['1'])
    status: str = Field('', title="", description="状态",examples=['1'])
    class_id: int|str = Field(0, title="班级ID", description="班级ID",examples=['1'])
    student_id: int|str = Field(0, title="学生ID", description="学生ID",examples=['1'])
    student_no: str = Field('', title="", description="学生编号",examples=['1'])
    class_name: str = Field('', title="",description="",examples=['1'])
    remark: str = Field('', title="", description="备注",examples=['1'])
    id_number: str = Field('', title="", description="",examples=['1'])
    school_id: int |str= Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int |str= Field(0, title="年级ID", description="年级ID",examples=['1'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','student_id','class_id']
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
class ClassDivisionRecordsImport(BaseModel):
    id:int|str= Field(0, title="", description="id", example='1')
    school_id: int|str = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int |str= Field(0, title="年级ID", description="年级ID",examples=['1'])
    class_id: int |str= Field(0, title="班级ID", description="班级ID",examples=['1'])
    student_id: int|str = Field(0, title="学生ID", description="学生ID",examples=['1'])
    student_no: str = Field('', title="", description="学生编号",examples=['1'])
    student_name: str = Field('', title="Grade_name",description="学生姓名",examples=['1'])
    status: str = Field('', title="", description="状态",examples=['1'])
    remark: str = Field('', title="", description="备注",examples=['1'])
    enrollment_number: str = Field('', title="", description="报名号",examples=['1'])
    id_type: str = Field('', title="", description="身份证件类型",examples=['1'])
    created_at: datetime|None = Field(None, title="", description="分班时间",examples=['1'])
    student_gender: str = Field('', title="", description="性别",examples=['1'])
    # class_id: int|str = Field(0, title="班级ID", description="班级ID",examples=['1'])
    # student_id: int|str = Field(0, title="学生ID", description="学生ID",examples=['1'])
    # student_no: str = Field('', title="", description="学生编号",examples=['1'])
    class_name: str = Field('', title="",description="",examples=['1'])
    # remark: str = Field('', title="", description="备注",examples=['1'])
    id_number: str = Field('', title="", description="",examples=['1'])
    # school_id: int |str= Field(0, title="学校ID", description="学校ID",examples=['1'])
    # grade_id: int |str= Field(0, title="年级ID", description="年级ID",examples=['1'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','student_id','class_id']
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
