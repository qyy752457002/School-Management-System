from datetime import datetime
from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class ClassStatus(str, Enum):
    """
    状态
    """
    NORMAL = "normal"
    LOCKED = "locked"

    @classmethod
    def to_list(cls):
        return [cls.NORMAL, cls.LOCKED ]
class Classes(BaseModel):
    """
    班级表
    """
    id: int|str = Query(None, title="", description="id", example='1')

    school_id: int|str = Field(None, title="学校ID", description="学校ID", examples=['1'])
    grade_no: str = Field('', title="年级编号", description="年级编号", examples=['一年级'])
    grade_id: int|str = Field(0, title="年级ID", description="年级ID", examples=['2'])
    session_id: int|str = Field(0, title="届别ID", description="届别ID", examples=['2'])
    session_name: str = Field('', title="届别名称", description="届别名称", examples=['一年级'])

    class_name: str = Field('', title="Grade_name", description="班级名称", examples=['一年级'])
    class_number: str = Field('', title="班号",description="班号", examples=['一年级'])
    class_index: str |None= Field('', title="班级序号", description="班级序号", examples=['一班'])
    year_established: str = Field(None,  title="建班年份",description="建班年份", examples=['2023'])
    teacher_id: int|str |None= Field(None, title="班主任id", description="班主任id", examples=['1'])
    teacher_id_card: str = Field(None,title="班主任身份证", description="班主任身份证", examples=['fsdfdsfsdxxx'])
    teacher_card_type: str = Field(None, title="班主任证件类型",description="班主任证件类型", examples=['idcard'])

    teacher_name: str = Field(None, title="班主任姓名",description="班主任姓名", examples=['fsdfdsfsdxxx'])
    teacher_phone: str = Field(None,title="班主任电话", description="班主任电话", examples=['fsdfdsfsdxxx'])
    teacher_job_number: str = Field(None, title="班主任工号",description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id: int|None|str = Field(None,title="保育员id", description="保育员id", examples=['1'])

    care_teacher_id_card: str = Field(None, title="保育员身份证",description="保育员身份证", examples=['fsdfdsfsdxxx'])
    care_teacher_card_type: str = Field(None,title="保育员证件类型", description="保育员证件类型", examples=['fsdfdsfsdxxx'])
    care_teacher_name: str = Field(None,title="保育员姓名", description="保育员姓名", examples=['fsdfdsfsdxxx'])
    care_teacher_phone: str = Field(None,title="保育员电话", description="保育员电话", examples=['fsdfdsfsdxxx'])
    care_teacher_job_number: str = Field(None, title="保育员工号",description="保育员工号", examples=['fsdfdsfsdxxx'])

    education_stage: str = Field(None,title="教育阶段", description="教育阶段", examples=['中职'])
    school_system: str = Field(None,title="学制", description="学制", examples=['fsdfdsfsdxxx'])
    monitor: str = Field(None,title="班长", description="班长", examples=['fsdfdsfsdxxx'])
    monitor_student_number: str = Field(None, title="班长学号",description="班长学号", examples=['S11000236001'])
    class_type: str = Field(None,title="中小学班级类型", description="中小学班级类型", examples=['小学教学点班'])
    is_bilingual_class: str|bool = Field(None,title="是否少数民族双语教学班", description="是否少数民族双语教学班", examples=[True])
    major_for_vocational: str|None = Field(None,title="中职班级专业", description="中职班级专业", examples=['770301'])
    bilingual_teaching_mode: str = Field(None,title="双语教学模式", description="双语教学模式", examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None,title="少数民族语言", description="少数民族语言", examples=['fsdfdsfsdxxx'])
    is_att_class: str|bool = Field(None,title="是否附设班", description="是否附设班", examples=[True])
    att_class_type: str = Field(None,title="附设班类型", description="附设班类型", examples=['附设班类型'])
    class_standard_name: str|None = Field(None,title="班级全称", description="", examples=[''])
    monitor_id: int|None = Field(None, title="班长的学生id",description="班长的学生id", examples=['1'])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','session_id','teacher_id','care_teacher_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str) and data[_change].isdigit():
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                # data[_change] = str(data[_change])
                pass
            else:
                pass
        return data


class ClassesSearchRes(BaseModel):
    """
    """
    id: int |str= Query(None, title="", description="id", example='1'),

    school_id: int|str = Field(None, title="学校ID", description="学校ID", examples=['1'])
    school_no: int|str|None = Field(None, title="", description="", examples=['1'])
    grade_no: str = Field(None, title="年级编号", description="年级编号", examples=['一年级'])
    grade_id: int|str = Field(None, title="年级ID", description="年级ID", examples=['2'])
    grade_type: str|None = Field(None, title="", description="", examples=[''])
    grade_type_name: str = Field(None, title="", description="", examples=[''])

    class_name: str|None = Field(None, title="Grade_name", description="班级名称", examples=['一年级'])
    class_number: str |None= Field(None, description="班号", examples=['一年级'])
    class_index: str |None= Field('', description="班级序号", examples=['一班'])
    class_standard_name: str|None = Field(None,title="班级全称", description="", examples=[''])

    year_established: str = Field(None, description="建班年份", examples=['fsdfdsfsdxxx'])
    teacher_id_card: str = Field(None, description="班主任身份证", examples=['fsdfdsfsdxxx'])
    teacher_card_type: str|None = Field(None, description="班主任证件类型", examples=['idcard'])
    teacher_id: int|None|str = Field(None, description="班主任id", examples=['1'])

    teacher_name: str|None = Field(None, description="班主任姓名", examples=['fsdfdsfsdxxx'])
    education_stage: str|None = Field(None, description="教育阶段", examples=['中职'])
    school_system: str |None= Field(None, description="学制", examples=['fsdfdsfsdxxx'])
    monitor: str |None= Field(None, description="班长", examples=['fsdfdsfsdxxx'])
    monitor_student_number: str |None= Field(None, description="班长学号", examples=['S11000236001'])
    class_type: str|None = Field(None, description="中小学班级类型", examples=['小学教学点班'])
    is_bilingual_class: str|bool = Field(None, description="是否少数民族双语教学班", examples=['fsdfdsfsdxxx'])
    major_for_vocational: str|None = Field(None, description="中职班级专业", examples=['fsdfdsfsdxxx'])
    bilingual_teaching_mode: str = Field(None, description="双语教学模式", examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None, description="少数民族语言", examples=['fsdfdsfsdxxx'])
    is_att_class: str|bool = Field(None, description="是否附设班", examples=['是否附设班'])
    att_class_type: str = Field(None, description="附设班类型", examples=['附设班类型'])
    borough: str|None = Field(None, title=" Author Email", description=" 行政管辖区", examples=['铁西区'])
    block: str|None = Field(None, title=" Author", description="地域管辖区", examples=['铁西区'])
    school_name: str|None = Field(None, title="学校名称", description="学校名称", examples=['XX小学'])
    # session_id: int = Field(0, title="届别ID", description="届别ID", examples=['2'])
    session_name: str = Field('', title="届别名称", description="届别名称", examples=['一年级'])
    teacher_phone: str|None = Field(None, description="班主任电话", examples=['fsdfdsfsdxxx'])
    teacher_job_number: str|None = Field(None, description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id_card: str = Field(None, description="保育员身份证", examples=['fsdfdsfsdxxx'])
    care_teacher_card_type: str = Field(None, description="班主任证件类型", examples=['fsdfdsfsdxxx'])
    care_teacher_name: str = Field(None, description="保育员姓名", examples=['fsdfdsfsdxxx'])
    care_teacher_phone: str = Field(None, description="班主任电话", examples=['fsdfdsfsdxxx'])
    care_teacher_job_number: str = Field(None, description="班主任工号", examples=['fsdfdsfsdxxx'])
    care_teacher_id: int|None|str = Field(None, description="保育员id", examples=['1'])
    monitor_id: int|None = Field(None, description="班长的学生id", examples=['1'])
    session_id: int|None = Field(None, description="", examples=['1'])
    created_at: datetime|None = Field('',  description="",examples=[''])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','session_id','teacher_id','care_teacher_id']
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


class ClassesImport(BaseModel):
    """
     字段对照模板

    """
    school_name: str|None = Field(None, title="学校名称", description="", examples=[''])
    class_name: str|None = Field(None, title="班级别名", description="班级名称", examples=['一年级'])
    class_number: str |None= Field(None,title='班号', description="班号", examples=[''])
    session_name: str = Field('', title="班级届别", description="届别名称", examples=[''])
    # 模版里的表头 有问题 这里用模版的
    class_index: str = Field('',title='班级', description="班级序号", examples=['一班'])
    grade_no: str = Field(None, title="当前年级", description="年级编号", examples=['一年级'])
    teacher_name: str|None = Field(None,title='班主任姓名', description="班主任姓名", examples=['fsdfdsfsdxxx'])
    teacher_phone: str = Field(None,title='班主任联系电话', description="班主任电话", examples=['fsdfdsfsdxxx'])
    teacher_card_type: str = Field(None,title='身份证件类型', description="班主任证件类型", examples=['idcard'])
    teacher_id_card: str = Field(None,title='身份证件号', description="班主任身份证", examples=['fsdfdsfsdxxx'])
    teacher_job_number: str = Field(None,title='班主任工号', description="班主任工号", examples=['fsdfdsfsdxxx'])
    monitor: str = Field(None, title='班长姓名',description="班长", examples=['fsdfdsfsdxxx'])
    monitor_student_number: str = Field(None,title='班长学号', description="班长学号", examples=['S11000236001'])
    class_type: str|None = Field(None,title='中小学班级类型', description="中小学班级类型", examples=['小学教学点班'])
    is_bilingual_class: str|bool = Field(None,title='是否为少数民族双语教学班', description="是否少数民族双语教学班", examples=[''])
    bilingual_teaching_mode: str = Field(None,title='双语教学模式码', description="双语教学模式", examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None,title='少数民族语言', description="少数民族语言", examples=['fsdfdsfsdxxx'])

    id: int |str= Query(None, title="", description="id", example='1'),

    school_id: int|str = Field(None, title="学校ID", description="学校ID", examples=['1'])
    grade_id: int|str = Field(None, title="年级ID", description="年级ID", examples=['2'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id", "school_id",'grade_id','session_id','teacher_id','care_teacher_id']
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
