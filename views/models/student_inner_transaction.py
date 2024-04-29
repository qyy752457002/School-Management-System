from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field

from models.student_transaction import AuditAction


class StudentInnerTransactionRes(BaseModel):
    """
    学籍号  性别 班级  学生状态  行政属地 学校  提交时间
    """
    id: int = Query(None, title="", description="id", example='1'),
    student_name: str = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])

    school_name: str = Query(..., title="", description="学校名称", examples=["XXxiaoxue"])

    classes: str = Query(..., title="", description="班级", examples=["二2班"])

    status: str = Query('', description="", min_length=1, max_length=20, examples=["..."]),
    # apply_user: str = Query('', title="", description="", examples=["申请人"])
    # apply_time: str = Query('', title="", description="", examples=["申请时间"])
    student_gender: str = Query('', title="", description="", examples=[""])



class StudentInnerTransaction(BaseModel):
    id: int = Query(None, title="", description="id", example='1'),
    student_name: str = Field('', title="", description="姓名", examples=[''])
    transaction_type: str = Field('', title="", description="异动类别", examples=[''])
    transaction_reason: str = Field('', title="", description="异动原因", examples=[''])


