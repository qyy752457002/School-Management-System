from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Roles(BaseDBModel):

    """
    角色
    system_type

单位管理
unit
教师管理
teacher
学生管理
student
edu_type

幼儿园
kg
中小学
k12
职业技术学校
vocational
unit_type

市
city
区
county
学校
school
school_id: 学校id
county_id: 区id
    """
    __tablename__ = 'lfun_roles'
    __table_args__ = {'comment': '角色'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="角色ID",autoincrement=True)
    system_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="系统类型",default='')
    edu_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="教育类型",default='')
    unit_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="单位类型",default='')
    app_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment=" ",default='')
    unit_id: Mapped[int] = mapped_column(nullable=True, comment="单位ID",default=0)
    school_id: Mapped[int] =mapped_column(nullable=True, comment="学校id",default=0)
    county_id: Mapped[int] =mapped_column(nullable=True, comment="区id",default=0)

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)

    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)


    @staticmethod
    def seed():
        return [

            Roles(id=1,system_type='unit',edu_type='kg',unit_type='city',app_name='园所信息管理系统',unit_id=0,school_id=0,county_id=0,created_uid=1,updated_uid=1,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),

        ]



