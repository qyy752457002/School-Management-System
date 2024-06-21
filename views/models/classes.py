from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field


class Classes(BaseModel):
    """
    班级表
    """
    id: int = Query(None, title="", description="id", example='1'),

    school_id: int = Field(None, title="学校ID", description="学校ID", examples=['1'])
    grade_no: str = Field('', title="年级编号", description="年级编号", examples=['一年级'])
    grade_id: int = Field(0, title="年级ID", description="年级ID", examples=['2'])
    session_id: int = Field(0, title="届别ID", description="届别ID", examples=['2'])
    session_name: str = Field('', title="届别名称", description="届别名称", examples=['一年级'])

    class_name: str = Field('', title="Grade_name", description="班级名称", examples=['一年级'])
    class_number: str = Field('', description="班号", examples=['一年级'])
    class_index: str = Field('', description="班级序号", examples=['一班'])
    year_established: str = Field(None, description="建班年份", examples=['2023'])
    teacher_id: int = Field(None, description="班主任id", examples=['1'])
    teacher_id_card: str = Field(None, description="班主任身份证", examples=['fsdfdsfsdxxx'])
    teacher_card_type: str = Field(None, description="班主任证件类型", examples=['idcard'])

    teacher_name: str = Field(None, description="班主任姓名", examples=['fsdfdsfsdxxx'])
    teacher_phone: str = Field(None, description="班主任电话", examples=['fsdfdsfsdxxx'])
    teacher_job_number: str = Field(None, description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id: int|None = Field(None, description="保育员id", examples=['1'])

    care_teacher_id_card: str = Field(None, description="保育员身份证", examples=['fsdfdsfsdxxx'])
    care_teacher_card_type: str = Field(None, description="保育员证件类型", examples=['fsdfdsfsdxxx'])
    care_teacher_name: str = Field(None, description="保育员姓名", examples=['fsdfdsfsdxxx'])
    care_teacher_phone: str = Field(None, description="保育员电话", examples=['fsdfdsfsdxxx'])
    care_teacher_job_number: str = Field(None, description="保育员工号", examples=['fsdfdsfsdxxx'])

    education_stage: str = Field(None, description="教育阶段", examples=['中职'])
    school_system: str = Field(None, description="学制", examples=['fsdfdsfsdxxx'])
    monitor: str = Field(None, description="班长", examples=['fsdfdsfsdxxx'])
    monitor_student_number: str = Field(None, description="班长学号", examples=['S11000236001'])
    class_type: str = Field(None, description="中小学班级类型", examples=['小学教学点班'])
    is_bilingual_class: str|bool = Field(None, description="是否少数民族双语教学班", examples=[True])
    major_for_vocational: str|None = Field(None, description="中职班级专业", examples=['770301'])
    bilingual_teaching_mode: str = Field(None, description="双语教学模式", examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None, description="少数民族语言", examples=['fsdfdsfsdxxx'])
    is_att_class: str|bool = Field(None, description="是否附设班", examples=[True])
    att_class_type: str = Field(None, description="附设班类型", examples=['附设班类型'])
    monitor_id: int|None = Field(None, description="班长的学生id", examples=['1'])


class ClassesSearchRes(BaseModel):
    """
    """
    id: int = Query(None, title="", description="id", example='1'),

    school_id: int = Field(None, title="学校ID", description="学校ID", examples=['1'])
    grade_no: str = Field(None, title="年级编号", description="年级编号", examples=['一年级'])
    grade_id: int = Field(None, title="年级ID", description="年级ID", examples=['2'])
    grade_type: str = Field(None, title="", description="", examples=[''])
    grade_type_name: str = Field(None, title="", description="", examples=[''])

    class_name: str|None = Field(None, title="Grade_name", description="班级名称", examples=['一年级'])
    class_number: str |None= Field(None, description="班号", examples=['一年级'])
    class_index: str = Field('', description="班级序号", examples=['一班'])

    year_established: str = Field(None, description="建班年份", examples=['fsdfdsfsdxxx'])
    teacher_id_card: str = Field(None, description="班主任身份证", examples=['fsdfdsfsdxxx'])
    teacher_card_type: str = Field(None, description="班主任证件类型", examples=['idcard'])
    teacher_id: int|None = Field(None, description="班主任id", examples=['1'])

    teacher_name: str|None = Field(None, description="班主任姓名", examples=['fsdfdsfsdxxx'])
    education_stage: str = Field(None, description="教育阶段", examples=['中职'])
    school_system: str = Field(None, description="学制", examples=['fsdfdsfsdxxx'])
    monitor: str = Field(None, description="班长", examples=['fsdfdsfsdxxx'])
    monitor_student_number: str = Field(None, description="班长学号", examples=['S11000236001'])
    class_type: str|None = Field(None, description="中小学班级类型", examples=['小学教学点班'])
    is_bilingual_class: str|bool = Field(None, description="是否少数民族双语教学班", examples=['fsdfdsfsdxxx'])
    major_for_vocational: str = Field(None, description="中职班级专业", examples=['fsdfdsfsdxxx'])
    bilingual_teaching_mode: str = Field(None, description="双语教学模式", examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None, description="少数民族语言", examples=['fsdfdsfsdxxx'])
    is_att_class: str|bool = Field(None, description="是否附设班", examples=['是否附设班'])
    att_class_type: str = Field(None, description="附设班类型", examples=['附设班类型'])
    borough: str = Field(None, title=" Author Email", description=" 行政管辖区", examples=['铁西区'])
    block: str = Field(None, title=" Author", description="地域管辖区", examples=['铁西区'])
    school_name: str = Field(None, title="学校名称", description="学校名称", examples=['XX小学'])
    # session_id: int = Field(0, title="届别ID", description="届别ID", examples=['2'])
    session_name: str = Field('', title="届别名称", description="届别名称", examples=['一年级'])
    teacher_phone: str = Field(None, description="班主任电话", examples=['fsdfdsfsdxxx'])
    teacher_job_number: str = Field(None, description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id_card: str = Field(None, description="保育员身份证", examples=['fsdfdsfsdxxx'])
    care_teacher_card_type: str = Field(None, description="班主任证件类型", examples=['fsdfdsfsdxxx'])
    care_teacher_name: str = Field(None, description="保育员姓名", examples=['fsdfdsfsdxxx'])
    care_teacher_phone: str = Field(None, description="班主任电话", examples=['fsdfdsfsdxxx'])
    care_teacher_job_number: str = Field(None, description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id: int|None = Field(None, description="保育员id", examples=['1'])
    monitor_id: int|None = Field(None, description="班长的学生id", examples=['1'])
    session_id: int|None = Field(None, description="", examples=['1'])
    created_at: datetime|None = Field('',  description="",examples=[''])
#     created /school/v1/classes/page session_id teacher_id class_name  create_at class_type class_number
