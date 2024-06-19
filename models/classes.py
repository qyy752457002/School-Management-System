from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Classes(BaseDBModel):
    """
    班级表
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



    """
    __tablename__ = 'lfun_classes'
    __table_args__ = {'comment': '班级表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID")
    grade_id: Mapped[int] = mapped_column( comment="年级ID",default=0,nullable=True)
    grade_no: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="年级编号")

    is_att_class: Mapped[bool] = mapped_column(  nullable=True,default=False, comment="是否附设班")
    att_class_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="附设班类型")
    session_id: Mapped[int] = mapped_column( comment="届别ID",default=0,nullable=True)

    session_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="届别名称",default='')

    class_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班级名称")
    class_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班号")
    class_index: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班级序号")
    year_established: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="建班年份")
    teacher_id_card: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任身份证")
    teacher_id: Mapped[int] = mapped_column(  nullable=True,default=0, comment="班主任id")
    teacher_card_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任证件类型")
    teacher_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任姓名")
    teacher_phone: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任电话")
    teacher_job_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任工号")
    care_teacher_id: Mapped[int] = mapped_column(  nullable=True,default=0, comment="保育员id")

    care_teacher_id_card: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="保育员身份证")
    care_teacher_card_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任证件类型")
    care_teacher_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="保育员姓名")
    care_teacher_phone: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任电话")
    care_teacher_job_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任工号")
    education_stage: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="教育阶段")
    school_system: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="学制")
    monitor: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班长")
    monitor_student_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班长学号")
    class_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="中小学班级类型")
    is_bilingual_class: Mapped[bool] = mapped_column(  nullable=True,default=False, comment="是否少数民族双语教学班")
    major_for_vocational: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="中职班级专业")
    bilingual_teaching_mode: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="双语教学模式")
    ethnic_language: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="少数民族语言")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)



