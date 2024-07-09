from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class Subject(BaseModel):
    """
    """
    id:int|str= Query(None, title="", description="id", example='1'),
    school_id: int|str = Field(0, title="学校ID", description="学校ID",examples=['1'])
    course_no: str = Field(None, title="", description="课程编码",examples=['19'])

    grade_id: int|str = Field(0, title="年级ID", description="年级ID",examples=['1'])
    course_name: str = Field(None, title="Grade_name",description="课程名称",examples=['语文'])

    subject_name: str = Field(None, title="", description="课程名称",examples=['1年级语文'])
    subject_alias: str = Field(None, title="", description="课程别名",examples=['入门语文1'])
    subject_level: str = Field(None, title="", description="课程等级",examples=['国家'])
    subject_description: str = Field(None, title="", description="课程简介",examples=['语文xxxxxx'])
    subject_requirement: str = Field(None, title="", description="课程要求",examples=['语文kkkkkkkkkk'])
    credit_hour: int = Field(None, title="", description="总学时",examples=['1'])
    week_credit_hour: int = Field(None, title="", description="周学时",examples=['1'])
    self_study_credit_hour: int = Field(None, title="", description="自学学时",examples=['1'])
    teach_method: str = Field(None, title="", description="授课方式",examples=['函授'])
    textbook_code: str = Field(None, title="", description="教材编码",examples=['YU20329996'])
    reference_book: str = Field(None, title="", description="参考书目",examples=['<语文 初级>'])
    @model_validator(mode="before")
    def check_id_before(self, data: dict):
        _change_list= ["id",'student_id','school_id','class_id','session_id','relation_id','process_instance_id','in_school_id','grade_id','transferin_audit_id']
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


