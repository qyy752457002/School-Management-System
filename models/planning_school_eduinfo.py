from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PlanningSchoolEduinfo(BaseDBModel):
    """
    规划校教学信息表
    """
    __tablename__ = 'lfun_planning_school_eduinfo'
    __table_args__ = {'comment': '规划校教学信息表'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID", autoincrement=False)
    planning_school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="规划校id", default=0)

    is_ethnic_school: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否民族校")
    is_att_class: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否附设班")
    att_class_type: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="附设班类型")
    is_province_feat: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否省特色")
    is_bilingual_clas: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否具有双语教学班")
    minority_lang_code: Mapped[str] = mapped_column(String(64), nullable=False, default='', comment="少数民族语言编码")
    is_profitable: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否营利性")
    prof_org_name: Mapped[str] = mapped_column(String(64), nullable=False, default='', comment="营利性机构名称")
    is_prov_demo: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否省示范")
    is_latest_year: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否最新年份")
    is_town_kinderg: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否乡镇幼儿园")
    is_incl_kinderg: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否普惠性幼儿园")
    is_affil_school: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否附属学校")
    affil_univ_code: Mapped[str] = mapped_column(String(64), nullable=False, default='',
                                                 comment="附属于高校（机构）标识码")
    affil_univ_name: Mapped[str] = mapped_column(String(64), nullable=False, default='', comment="附属于高校（机构）名称")
    is_last_yr_revok: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否上年撤销")
    is_school_counted: Mapped[bool] = mapped_column(nullable=False, default=False, comment="是否计校数")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="更新时间")

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
