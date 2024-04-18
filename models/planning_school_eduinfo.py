from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PlanningSchoolEduinfo(BaseDBModel):
    """
    规划校教学信息表
    """
    __tablename__ = 'lfun_planning_school_eduinfo'
    __table_args__ = {'comment': '规划校教学信息表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    planning_school_id: Mapped[int] = mapped_column( nullable=True  , comment="规划校id",default=0)

    is_ethnic_school: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否民族校")
    is_att_class: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否附设班")
    att_class_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="附设班类型")
    is_province_feat: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否省特色")
    is_bilingual_clas: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否具有双语教学班")
    minority_lang_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="少数民族语言编码")
    is_profitable: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否营利性")
    prof_org_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="营利性机构名称")
    is_prov_demo: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否省示范")
    is_latest_year: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否最新年份")
    is_town_kinderg: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否乡镇幼儿园")
    is_incl_kinderg: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否普惠性幼儿园")
    is_affil_school: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否附属学校")
    affil_univ_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="附属于高校（机构）标识码")
    affil_univ_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="附属于高校（机构）名称")
    is_last_yr_revok: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否上年撤销")
    is_school_counted: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否计校数")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="更新时间")
    # deleted: Mapped[int] = mapped_column(default=0, comment="是否删除")
    # created_uid: Mapped[int] = mapped_column(default=0, comment="创建人")
    # updated_uid: Mapped[int] = mapped_column(default=0, comment="更新人")


    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    deleted: Mapped[int] = mapped_column( nullable=True  , comment="删除态",default=0)
    # created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    # updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
