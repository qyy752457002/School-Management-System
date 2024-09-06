from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Grade(BaseDBModel):
    """
    年级表
    """
    __tablename__ = 'lfun_grade'
    __table_args__ = {'comment': '年级表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="年级ID",autoincrement=False)
    school_id: Mapped[int] = mapped_column(BigInteger, comment="学校ID",default=0,nullable=True)

    school_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="教育阶段/学校类别 例如 小学 初中")
    city: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城市 编码")
    district: Mapped[str] = mapped_column(String(64), nullable=True, comment="区 编码",default='')
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码/中职用枚举")
    course_no_lv2: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码2")
    course_no_lv3: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码3")


    grade_no: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级编号")
    grade_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="年级类型/班级类型 例如 一年级 二年级 三年级,枚举grade")

    grade_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级名称/班级名称")
    sort_number: Mapped[int] = mapped_column(nullable=True,default=0, comment="排序序号")
    class_number: Mapped[int] = mapped_column(nullable=False,default=0, comment="本年级班级数量")

    grade_alias: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级别名")
    description: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="简介")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
