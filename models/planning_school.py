from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PlanningSchool(BaseDBModel):
    """
    规划校
    """
    __tablename__ = 'lfun_planning_school'
    __table_args__ = {'comment': '规划校'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    # school_id: Mapped[int] = mapped_column( comment="学校ID")
    planning_school_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校名称")
    planning_school_no: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校编号")
    planning_school_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="园所标识码")
    planning_school_operation_license_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="办学许可证号",default='')
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政管辖区")
    planning_school_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校类型")
    planning_school_operation_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型/学校性质")
    planning_school_operation_type_lv2: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型二级")
    planning_school_operation_type_lv3: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型三级")
    planning_school_org_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校办别")
    planning_school_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校星级")
    status: Mapped[str] = mapped_column(String(64), nullable=False, comment="状态")
    kg_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="星级",default='')
    planning_school_short_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="园所简称",default='')
    planning_school_en_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="园所英文名称",default='')
    create_planning_school_date: Mapped[str] = mapped_column(String(64), nullable=True, comment="建校年月",default='')
    social_credit_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="统一社会信用代码",default='')
    founder_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="founder_type",default='')
    founder_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者名称",default='')
    founder_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者识别码",default='')
    urban_rural_nature: Mapped[str] = mapped_column(String(64), nullable=True, comment="城乡性质",default='')
    planning_school_org_form: Mapped[str] = mapped_column(String(64), nullable=True, comment="办学组织形式",default='')
    planning_school_closure_date: Mapped[str] = mapped_column(String(64), nullable=True, comment="学校关闭日期",default='')
    department_unit_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理行政部门单位号",default='')
    sy_zones: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理行政部门所在地地区",default='')
    historical_evolution: Mapped[str] = mapped_column(String(300), nullable=True, comment="历史沿革",default='')
    sy_zones_pro: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理教育行政部门所在地（省级）",default='')
    primary_planning_school_system: Mapped[str] = mapped_column(String(64), nullable=True, comment="小学学制",default='')
    primary_planning_school_entry_age: Mapped[str] = mapped_column(String(64), nullable=True, comment="小学入学年龄",default='')
    junior_middle_planning_school_system: Mapped[str] = mapped_column(String(64), nullable=True, comment="初中学制",default='')
    junior_middle_planning_school_entry_age: Mapped[str] = mapped_column(String(64), nullable=True, comment="初中入学年龄",default='')
    senior_middle_planning_school_system: Mapped[str] = mapped_column(String(64), nullable=True, comment="高中学制",default='')
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    deleted: Mapped[int] = mapped_column( nullable=True  , comment="删除态",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
