from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class School(BaseDBModel):
    """
    学校
    """
    __tablename__ = 'lfun_school'
    __table_args__ = {'comment': '学校'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True,)
    school_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校名称")
    school_no: Mapped[str] = mapped_column(String(30), nullable=False, comment="学校编号")
    school_code: Mapped[str] = mapped_column(String(30), nullable=False, comment="学校标识码")
    school_operation_license_number: Mapped[str] = mapped_column(String(30), nullable=False, comment="办学许可证号")
    block: Mapped[str] = mapped_column(String(20), nullable=False, comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(20), nullable=False, comment="行政管辖区")
    school_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="学校类型")
    school_operation_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="办学类型/学校性质")
    school_operation_type_lv2: Mapped[str] = mapped_column(String(20), nullable=False, comment="办学类型二级")
    school_operation_type_lv3: Mapped[str] = mapped_column(String(20), nullable=False, comment="办学类型三级")
    school_org_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="学校办别")
    school_level: Mapped[str] = mapped_column(String(20), nullable=False, comment="学校星级")
    status: Mapped[str] = mapped_column(String(20), nullable=False, comment="状态")
    kg_level: Mapped[str] = mapped_column(String(20), nullable=False, comment="星级")
    school_short_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="园所简称")
    school_en_name: Mapped[str] = mapped_column(String(30), nullable=False, comment="园所英文名称")
    create_school_date: Mapped[str] = mapped_column(String(30), nullable=False, comment="建校年月")
    social_credit_code: Mapped[str] = mapped_column(String(32), nullable=True, comment="统一社会信用代码")
    founder_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="举办者类型")
    founder_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="举办者名称")
    founder_code: Mapped[str] = mapped_column(String(32), nullable=False, comment="举办者识别码")
    urban_rural_nature: Mapped[str] = mapped_column(String(20), nullable=False, comment="城乡性质")
    school_org_form: Mapped[str] = mapped_column(String(20), nullable=False, comment="办学组织形式")
    school_closure_date: Mapped[str] = mapped_column(String(20), nullable=True, comment="学校关闭日期")
    department_unit_number: Mapped[str] = mapped_column(String(32), nullable=False, comment="属地管理行政部门单位号")
    sy_zones: Mapped[str] = mapped_column(String(32), nullable=False, comment="属地管理行政部门所在地地区")
    historical_evolution: Mapped[str] = mapped_column(String(300), nullable=False, comment="历史沿革")
    sy_zones_pro: Mapped[str] = mapped_column(String(64), nullable=False, comment="属地管理教育行政部门所在地（省级）")
    primary_school_system: Mapped[str] = mapped_column(String(20), nullable=False, comment="小学学制")
    primary_school_entry_age: Mapped[str] = mapped_column(String(10), nullable=False, comment="小学入学年龄")
    junior_middle_school_system: Mapped[str] = mapped_column(String(10), nullable=False, comment="初中学制")
    junior_middle_school_entry_age: Mapped[str] = mapped_column(String(10), nullable=False, comment="初中入学年龄")
    senior_middle_school_system: Mapped[str] = mapped_column(String(10), nullable=False, comment="高中学制")
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

