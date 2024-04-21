from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Campus(BaseDBModel):
    """
    校区

校区负责人姓名
campus_leader_name
校区负责人职位
campus_leader_position
    """
    __tablename__ = 'lfun_campus'
    __table_args__ = {'comment': '校区'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True,)
    school_id: Mapped[int] = mapped_column( nullable=True  , comment="学校id",default=0)

    campus_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="校区名称")
    campus_no: Mapped[str] = mapped_column(String(30), nullable=True,default='', comment="校区编号")
    campus_code: Mapped[str] = mapped_column(String(30), nullable=True,default='', comment="校区标识码")
    campus_operation_license_number: Mapped[str] = mapped_column(String(30), nullable=True,default='', comment="办学许可证号")
    block: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="行政管辖区")
    campus_type: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="校区类型")
    campus_operation_type: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="办学类型/校区性质")
    campus_operation_type_lv2: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="办学类型二级")
    campus_operation_type_lv3: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="办学类型三级")
    campus_org_type: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="校区办别")
    campus_level: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="校区星级")
    status: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="状态")
    kg_level: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="星级")
    campus_short_name: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="园所简称")
    campus_en_name: Mapped[str] = mapped_column(String(30), nullable=True,default='', comment="园所英文名称")
    create_campus_date: Mapped[str] = mapped_column(String(30), nullable=True,default='', comment="建校年月")
    social_credit_code: Mapped[str] = mapped_column(String(32), nullable=True, comment="统一社会信用代码")
    founder_type: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="举办者类型")
    founder_type_lv2: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型二级",default='')
    founder_type_lv3: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型三级",default='')

    founder_name: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="举办者名称")
    founder_code: Mapped[str] = mapped_column(String(32), nullable=True,default='', comment="举办者识别码")
    urban_rural_nature: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="城乡性质")
    campus_org_form: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="办学组织形式")
    campus_closure_date: Mapped[str] = mapped_column(String(20), nullable=True, comment="校区关闭日期")
    department_unit_number: Mapped[str] = mapped_column(String(32), nullable=True,default='', comment="属地管理行政部门单位号")
    sy_zones: Mapped[str] = mapped_column(String(32), nullable=True,default='', comment="属地管理行政部门所在地地区")
    historical_evolution: Mapped[str] = mapped_column(String(300), nullable=True,default='', comment="历史沿革")
    campus_leader_name: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="校区负责人姓名")
    campus_leader_position: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="校区负责人职位")
    location_city: Mapped[str] = mapped_column(String(32), nullable=True,default='', comment="校区所在地(省市)")
    location_district: Mapped[str] = mapped_column(String(32), nullable=True,default='', comment="校区所在地(区县)")


    sy_zones_pro: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="属地管理教育行政部门所在地（省级）")
    primary_campus_system: Mapped[str] = mapped_column(String(20), nullable=True,default='', comment="小学学制")
    primary_campus_entry_age: Mapped[str] = mapped_column(String(10), nullable=True,default='', comment="小学入学年龄")
    junior_middle_campus_system: Mapped[str] = mapped_column(String(10), nullable=True,default='', comment="初中学制")
    junior_middle_campus_entry_age: Mapped[str] = mapped_column(String(10), nullable=True,default='', comment="初中入学年龄")
    senior_middle_campus_system: Mapped[str] = mapped_column(String(10), nullable=True,default='', comment="高中学制")
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





