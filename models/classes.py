from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Classes(BaseDBModel):
    """
    班级表
    """
    __tablename__ = 'lfun_classes'
    __table_args__ = {'comment': '班级表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    school_id: Mapped[int] = mapped_column(BigInteger, comment="学校ID")
    grade_id: Mapped[int] = mapped_column(BigInteger, comment="年级ID",default=0,nullable=True)
    grade_no: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="年级编号")

    is_att_class: Mapped[bool] = mapped_column(  nullable=True,default=False, comment="是否附设班")
    att_class_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="附设班类型")
    session_id: Mapped[int] = mapped_column(BigInteger, comment="届别ID",default=0,nullable=True)

    session_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="届别名称",default='')

    class_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班级别名")
    class_standard_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班级名称")
    class_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班号")
    class_index: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班级序号")
    year_established: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="建班年份")
    teacher_id_card: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任身份证")
    teacher_id: Mapped[int] = mapped_column( BigInteger, nullable=True,default=0, comment="班主任id")
    teacher_card_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任证件类型")
    teacher_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任姓名")
    teacher_phone: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任电话")
    teacher_job_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任工号")
    care_teacher_id: Mapped[int] = mapped_column( BigInteger, nullable=True,default=0, comment="保育员id")

    care_teacher_id_card: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="保育员身份证")
    care_teacher_card_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任证件类型")
    care_teacher_name: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="保育员姓名")
    care_teacher_phone: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任电话")
    care_teacher_job_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班主任工号")
    education_stage: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="教育阶段")
    school_system: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="学制")
    monitor: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班长")
    monitor_id: Mapped[int] = mapped_column( BigInteger, nullable=True,default=0, comment="班长的学生id")

    monitor_student_number: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="班长学号")
    class_type: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="中小学班级类型")
    is_bilingual_class: Mapped[bool] = mapped_column(  nullable=True,default=False, comment="是否少数民族双语教学班")
    major_for_vocational: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="中职班级专业")
    bilingual_teaching_mode: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="双语教学模式")
    ethnic_language: Mapped[str] = mapped_column(String(48), nullable=True,default='', comment="少数民族语言")
    status: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="状态")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)



