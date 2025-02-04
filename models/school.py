from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger, Text
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class School(BaseDBModel):
    """
    学校
    """
    __tablename__ = 'lfun_school'
    __table_args__ = {'comment': '学校'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID", autoincrement=False, )
    planning_school_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="规划校id", default=0)
    institution_category: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment=" 单位分类")

    school_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校名称")
    school_no: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校编号")
    old_school_no: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="旧的学校编号(例如一期)")
    school_code: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校标识码")
    school_operation_license_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="办学许可证号")
    block: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="行政管辖区")
    school_edu_level: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="教育层次:枚举school_nature 1级")
    # school_category粗 枚举 school_nature_lv2 2级细 目前是枚举 school_nature_lv2
    school_category: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校（机构）类别,枚举 school_nature_lv2 2级")
    school_operation_type: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="办学类型:枚举 school_nature_lv3 3级枚举")
    school_org_type: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校办别")
    school_level: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校星级")
    status: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="状态")
    kg_level: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="星级")
    school_short_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="园所简称")
    school_en_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="园所英文名称")
    create_school_date: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="建校年月")
    social_credit_code: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="统一社会信用代码")
    founder_type: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="举办者类型")
    founder_type_lv2: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型二级", default='')
    founder_type_lv3: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型三级", default='')

    founder_name: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="举办者名称")
    founder_code: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="举办者识别码")
    location_economic_attribute: Mapped[str] = mapped_column(String(64), nullable=True, comment="所属地经济属性",
                                                             default='')
    urban_ethnic_nature: Mapped[str] = mapped_column(String(64), nullable=True, comment="所在地民族属性", default='')
    leg_repr_certificatenumber: Mapped[str] = mapped_column(String(64), nullable=True, comment="法人证书号", default='')

    urban_rural_nature: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="城乡性质")
    school_org_form: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="办学组织形式,枚举school_org_form")
    school_closure_date: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校关闭日期")
    department_unit_number: Mapped[str] = mapped_column(String(64), nullable=True, default='',
                                                        comment="属地管理行政部门单位号")
    sy_zones: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="属地管理行政部门所在地地区")
    historical_evolution: Mapped[str] = mapped_column( Text, nullable=True, default='', comment="历史沿革")
    sy_zones_pro: Mapped[str] = mapped_column(String(64), nullable=True, default='',
                                              comment="属地管理教育行政部门所在地（省级）")
    primary_school_entry_age: Mapped[str] = mapped_column(String(10), nullable=True, default='', comment="小学入学年龄")
    junior_middle_school_entry_age: Mapped[str] = mapped_column(String(10), nullable=True, default='',
                                                                comment="初中入学年龄")
    membership_no: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment=" 隶属单位号")
    is_entity: Mapped[bool] = mapped_column(nullable=True, default=True, comment=" 是否实体")
    admin: Mapped[str] = mapped_column(String(64), nullable=True, comment="管理员", default='')
    admin_phone: Mapped[str] = mapped_column(String(64), nullable=True, comment="管理员手机", default='')
    org_center_info: Mapped[str] = mapped_column(String(255), nullable=True, comment="组织中心信息", default='')

    process_instance_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=0, comment="流程ID")
    workflow_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="工作流审核状态", default='')
    is_master: Mapped[bool] = mapped_column( nullable=True  , comment="是否主分校",default=False)

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
