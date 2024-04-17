from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PlanningSchool(BaseDBModel):
    """
    规划校
    """
    __tablename__ = 'lfun_planning_school'
    __table_args__ = {'comment': '规划校'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID")
    # school_id: Mapped[int] = mapped_column( comment="学校ID")
    planning_school_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校名称")
    planning_school_no: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校编号")
    planning_school_operation_license_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学许可证号")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政管辖区")
    planning_school_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校类型")
    planning_school_operation_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型/学校性质")
    planning_school_operation_type_lv2: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型二级")
    planning_school_operation_type_lv3: Mapped[str] = mapped_column(String(64), nullable=False, comment="办学类型三级")
    planning_school_org_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校办别")
    planning_school_level: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校星级")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
    block: Mapped[str] = mapped_column(String(64), nullable=False, comment="地域管辖区")
