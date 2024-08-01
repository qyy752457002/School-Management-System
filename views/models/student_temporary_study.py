from enum import Enum
from typing import Iterable

from fastapi import Query
from pydantic import BaseModel, Field, model_validator

from models.student_transaction import AuditAction
from views.models.student_transaction import StudentTransactionStatus



class StudentTemporaryStudy(BaseModel):
    student_id: int | str | None = Query(..., description="学生id", title='学生id',    examples=["1"], example="1")
    school_id: int | str | None = Query(..., title="", description="目标学校ID", examples=["102"])
    class_id: str | int | None = Query(..., title="", description="目标班级id", examples=["125"])
    grade_id: int | str = Field(..., title="年级ID", description="目标年级ID", examples=['1'])
    session_id: int | str = Field(..., title="目标届别id", description="目标届别id", examples=['1'])

    id: int | str = Query(None, title="", description="id", example='1')
    student_name: int | str = Query(None, title="", description="", example='')
    id_number: int | str = Query(None, title="", description="", example='')
    student_gender: int | str = Query(None, title="", description="", example='')
    edu_number: int | str = Query(None, title="", description="", example='')
    student_no: int | str = Query(None, title="", description="", example='')

    origin_school_id: int | str = Field(0, title="", description="", examples=['1'])
    origin_session_id: int | str = Field(0, title="", description="", examples=['1'])
    origin_grade_id: int | str = Field(0, title="", description="", examples=['1'])
    origin_class_id: int | str = Field(0, title="", description="", examples=['1'])

    process_instance_id: int | str = Field(0, title="", description="", examples=['1'])
    status: str = Field('', title="", description="状态", examples=[''])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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




class StudentTemporaryStudyPageSearch(BaseModel):
    audit_status: StudentTransactionStatus = Query("", title="", description="状态", examples=['needaudit'])
    student_name: str = Query("", title="", description="学生姓名", min_length=1, max_length=20)

    school_id: int = Query(0, title="", description="学校ID", )
    school_name: str  = Query('', title="", description="学校", )
    student_gender: str = Query("", title="", description=" 学生性别", min_length=1, max_length=20)

    applicant_name: str = Query("",alias='apply_user', title="", description="申请人", min_length=1, max_length=20, )
    edu_number: str = Query("",alias='edu_no', title="  ", description=" 学籍号码", min_length=1, max_length=20)
