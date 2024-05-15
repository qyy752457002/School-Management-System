from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

class ClassDivisionRecords(BaseModel):
    """
      student_id: Mapped[int] = mapped_column(nullable=True , comment="学生ID",default=0)
    school_id: Mapped[int] = mapped_column(nullable=True , comment="学校ID",default=0)
    grade_id: Mapped[int] = mapped_column(nullable=True , comment="年级ID",default=0)
    class_id: Mapped[int] = mapped_column(nullable=True , comment="班级ID",default=0)
    student_no: Mapped[str] = mapped_column(String(255),  nullable=True, comment="学号",default='')
    student_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="学生姓名",default='')
    status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="状态",default='')

    remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="备注",default='')
    """
    id:int= Query(None, title="", description="id", example='1'),
    school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])
    class_id: int = Field(0, title="班级ID", description="班级ID",examples=['1'])
    student_id: int = Field(0, title="学生ID", description="学生ID",examples=['1'])
    student_no: str = Field('', title="", description="学生编号",examples=['1'])
    student_name: str = Field('', title="Grade_name",description="学生姓名",examples=['1'])
    status: str = Field('', title="", description="状态",examples=['1'])
    remark: str = Field('', title="", description="备注",examples=['1'])




class ClassDivisionRecordsSearchRes(BaseModel):
    """
    报名号
   enrollment_number: str = Query( '', title="", description="报名号",min_length=1, max_length=30, example=''),
                                            school_id: str = Query( 0, title="", description="学校ID",min_length=1, max_length=30, example=''),
                                            id_type: str = Query( '', title="", description="身份证件类型",min_length=1, max_length=30, example=''),
                                            student_name: str = Query( '', title="", description="姓名",min_length=1, max_length=30, example=''),
                                            created_at: str = Query( '', title="", description="分班时间",min_length=1, max_length=30, example=''),
                                            student_gender: str = Query( '', title="", description="性别",min_length=1, max_length=30, example=''),
                                            class_id: int = Query( 0, title="", description="班级",min_length=1, max_length=30, example=''),
                                            status: str = Query( '', title="", description="状态",min_length=1, max_length=30, example=''),
    """
    id:int= Field(0, title="", description="id", example='1')
    enrollment_number: str = Field('', title="", description="报名号",examples=['1'])
    id_type: str = Field('', title="", description="身份证件类型",examples=['1'])
    student_name: str = Field('', title="", description="姓名",examples=['1'])
    created_at: datetime = Field('', title="", description="分班时间",examples=['1'])
    student_gender: str = Field('', title="", description="性别",examples=['1'])
    status: str = Field('', title="", description="状态",examples=['1'])
    class_id: int = Field(0, title="班级ID", description="班级ID",examples=['1'])
    student_id: int = Field(0, title="学生ID", description="学生ID",examples=['1'])
    student_no: str = Field('', title="", description="学生编号",examples=['1'])
    class_name: str = Field('', title="",description="",examples=['1'])
    remark: str = Field('', title="", description="备注",examples=['1'])
    id_number: str = Field('', title="", description="",examples=['1'])

    school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])
