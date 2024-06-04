from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Grade(BaseDBModel):
    """
    年级表
    """
    __tablename__ = 'lfun_grade'
    __table_args__ = {'comment': '年级表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="年级ID",autoincrement=True)
    school_id: Mapped[int] = mapped_column( comment="学校ID")

    city: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城市")
    district: Mapped[str] = mapped_column(String(64), nullable=False, comment="")
    grade_no: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级编号")
    grade_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级名称")
    grade_alias: Mapped[str] = mapped_column(String(64), nullable=False, comment="年级别名")
    description: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="简介")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")

    @staticmethod
    def seed():
        return [
            Grade(grade_name='一年级', grade_alias='一年级', grade_no='一年级', school_id=0, city='沈阳市', district='',),
            Grade(grade_name='二年级', grade_alias='二年级', grade_no='二年级', school_id=0, city='沈阳市', district='',),
            Grade(grade_name='三年级', grade_alias='三年级', grade_no='三年级', school_id=0, city='沈阳市', district='',),
            Grade(grade_name='四年级', grade_alias='四年级', grade_no='四年级', school_id=0, city='沈阳市', district='',),
            Grade(grade_name='一年级', grade_alias='一年级', grade_no='一年级', school_id=0, city='沈阳市', district='和平区',),
            Grade(grade_name='二年级', grade_alias='二年级', grade_no='二年级', school_id=0, city='沈阳市', district='和平区',),
            Grade(grade_name='三年级', grade_alias='三年级', grade_no='三年级', school_id=0, city='沈阳市', district='和平区',),
            Grade(grade_name='四年级', grade_alias='四年级', grade_no='四年级', school_id=0, city='沈阳市', district='和平区',),



        ]
