from enum import Enum
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field

from models.student_transaction import AuditAction


class StudentInnerTransactionRes(BaseModel):
    """

    """
    id: int = Query(None, title="", description="id", example='1'),
    student_name: str = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])

    school_name: str = Query(..., title="", description="学校名称", examples=["XXxiaoxue"])
    classes: str = Query(..., title="", description="班级", examples=["二2班"])
    status: str = Query('', description="", min_length=1, max_length=20, examples=["..."]),
    student_gender: str = Query('', title="", description="", examples=[""])
    edu_number: str = Field('', title="", description="学籍号码")
    transaction_time: str = Field('', title="", description="提交时间")
    class_name: str = Field('', title="Grade_name", description="班级名称", examples=['一年级'])
    borough: str = Field('', title=" Author Email", description=" 行政管辖区", examples=['铁西区'])
    approval_status: Optional[str] = Query(None, title="", description="学生状态")


class StudentInnerTransaction(BaseModel):
    id: int = Query(None, title="", description="id", example='1'),
    student_name: str = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])


class StudentInnerTransactionSearch(BaseModel):
    """
    """
    borough: str = Field('', title=" ", description=" 行政管辖区", examples=['铁西区'])
    school_id: int  = Query( 0, title="", description="学校名称", examples=["XXxiaoxue"])
    student_name: str = Field('', title="", description="姓名", examples=[''])
    student_gender: str = Query('', title="", description="", examples=[""])
    edu_number: str = Field('', title="", description="学籍号码")
    class_id: int  = Query( 0, title="", description="班级", examples=["二2班"])
