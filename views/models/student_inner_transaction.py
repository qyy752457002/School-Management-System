from datetime import datetime
from enum import Enum
from typing import Optional, Iterable

from fastapi import Query
from pydantic import BaseModel, Field, model_validator

from models.student_transaction import AuditAction


class StudentInnerTransactionRes(BaseModel):
    """

    """
    id: int|str = Query(None, title="", description="id", example='1'),
    student_name: str|None = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])
    school_name: str|None = Query('', title="", description="学校名称", examples=["XXxiaoxue"])
    classes: str|None = Query('', title="", description="班级", examples=["二2班"])
    student_gender: str |None= Query('', title="", description="", examples=[""])
    edu_number: str |None= Field('', title="", description="学籍号码")
    transaction_time: datetime = Field('', title="", description="提交时间")
    class_name: str|None = Field('', title="Grade_name", description="班级名称", examples=['一年级'])
    borough: str |None= Field('', title=" Author Email", description=" 行政管辖区", examples=['铁西区'])
    approval_status: Optional[str] = Query(None, title="", description="学生状态")
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id",]
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


class StudentInnerTransaction(BaseModel):
    student_id: int|str = Field(..., title="", description="", examples=['1'])
    # id: int = Query(None, title="", description="id", example='1'),
    student_name: str = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id",'student_id']
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


class StudentInnerTransactionSearch(BaseModel):
    """
    """
    borough: str = Query('', title=" ", description=" 行政管辖区", examples=['铁西区'])
    school_id: int |str = Query( 0, title="", description="学校名称", examples=["XXxiaoxue"])
    student_name: str = Query('', title="", description="姓名", examples=[''])
    student_gender: str = Query('', title="", description="", examples=[""])
    edu_number: str = Query('', title="", description="学籍号码")
    class_id: int |str = Query( 0, title="", description="班级", examples=["二2班"])
    @model_validator(mode="before")
    def check_id_before(self, data: dict):
        _change_list= ["id",'student_id','school_id','class_id']
        for _change in _change_list:
            # if isinstance()
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                pass
            else:
                pass
        return data

class StudentInnerTransactionAudit(BaseModel):
    remark: str = Query("", description="审批的备注", min_length=0, max_length=200,
                        example='同意 无误')
    transaction_id: int|str = Query(..., description="申请id", example='2')
    transaction_audit_action: AuditAction = Query(..., description="审批的操作")
    @model_validator(mode="before")
    def check_id_before(self, data: dict):
        _change_list= ["id",'student_id','school_id','class_id','transaction_id']
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
