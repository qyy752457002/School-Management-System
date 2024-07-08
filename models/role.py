from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Role(BaseDBModel):

    """
    角色

    """
    __tablename__ = 'lfun_role'
    __table_args__ = {'comment': '角色表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="角色ID",autoincrement=False)
    system_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="系统类型",default='')
    edu_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="教育类型",default='')
    unit_type: Mapped[str] = mapped_column(String(64),  nullable=True, comment="单位类型",default='')
    app_name: Mapped[str] = mapped_column(String(64),  nullable=True, comment="系统名称",default='')
    remark: Mapped[str] = mapped_column(String(64),  nullable=True, comment="备注",default='')
    unit_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="单位ID",default=0)
    school_id: Mapped[int] =mapped_column(BigInteger,nullable=True, comment="学校id",default=0)
    county_id: Mapped[int] =mapped_column(BigInteger,nullable=True, comment="区id",default=0)
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
    #
    # @staticmethod
    # def seed():
    #     return [
    #         Role(id=1, system_type='unit', edu_type='kg', unit_type='city', app_name='园所信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=2, system_type='unit', edu_type='k12', unit_type='city', app_name='中小学信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=3, system_type='unit', edu_type='vocational', unit_type='city', app_name='职高信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=4, system_type='unit', edu_type='kg', unit_type='school', app_name='园所信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=5, system_type='unit', edu_type='kg', unit_type='county', app_name='园所信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=6, system_type='unit', edu_type='k12', unit_type='county', app_name='中小学信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=7, system_type='unit', edu_type='k12', unit_type='school', app_name='中小学信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=8, system_type='unit', edu_type='vocational', unit_type='county', app_name='职高信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #         Role(id=9, system_type='unit', edu_type='vocational', unit_type='school', app_name='职高信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #
    #         Role(id=10, system_type='teacher', edu_type='', unit_type='', app_name='教职工信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #
    #         Role(id=11, system_type='student', edu_type='', unit_type='', app_name='学生信息管理系统', unit_id=0, school_id=0, county_id=0, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
    #     ]



