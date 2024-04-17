from pydantic import BaseModel, Field

class Classes(BaseModel):
    school_id: str = Field(..., title="学校ID", description="学校ID",examples=[''])
    grade_no: str = Field(..., title="年级编号", description="年级编号",examples=['一年级'])
    grade_id: str = Field(..., title="年级ID", description="年级ID",examples=['一年级'])

    class_name: str = Field(..., title="Grade_name",description="班级名称",examples=['一年级'])
    class_number: str = Field(...,  description="班号",examples=['一年级'])
    year_established: str = Field(None,  description="建班年份",examples=['fsdfdsfsdxxx'])
    teacher_id_card: str = Field(None,  description="班主任身份证",examples=['fsdfdsfsdxxx'])
    teacher_name: str = Field(None,  description="班主任姓名",examples=['fsdfdsfsdxxx'])
    education_stage: str = Field(None,  description="教育阶段",examples=['中职'])
    school_system: str = Field(None,  description="学制",examples=['fsdfdsfsdxxx'])
    monitor: str = Field(None,  description="班长",examples=['fsdfdsfsdxxx'])
    class_type: str = Field(None,  description="中小学班级类型",examples=['小学教学点班'])
    is_bilingual_class: str = Field(None,  description="是否少数民族双语教学班",examples=['fsdfdsfsdxxx'])
    major_for_vocational: str = Field(None,  description="中职班级专业",examples=['fsdfdsfsdxxx'])
    bilingual_teaching_mode: str = Field(None,  description="双语教学模式",examples=['fsdfdsfsdxxx'])
    ethnic_language: str = Field(None,  description="少数民族语言",examples=['fsdfdsfsdxxx'])

