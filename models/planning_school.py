from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger, Text
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PlanningSchool(BaseDBModel):
    """
    规划校

    教育层次 : planning_school_edu_level   1学前教育  <-planning_school_edu_level


    学校（机构）类别: planning_school_category 幼儿园<-  planning_school_operation_type2


    办学类型 planning_school_edu_level  附设幼儿班 <-planning_school_operation_type3


    """
    __tablename__ = 'lfun_planning_school'
    __table_args__ = {'comment': '规划校'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID", autoincrement=False)
    planning_school_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校名称")
    planning_school_no: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="学校编号")
    old_planning_school_no: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="旧的学校编号(例如一期)")

    planning_school_code: Mapped[str] = mapped_column(String(64), nullable=True,default='',  comment="园所标识码")
    planning_school_operation_license_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="办学许可证号", default='')
    block: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="地域管辖区,枚举country")
    borough: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="行政管辖区,枚举country")
    province: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="省份,枚举province")
    city: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="城市,枚举city")

    # planning_school_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="学校类型")
    planning_school_edu_level: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="教育层次,枚举school_nature")
    # planning_school_nature: Mapped[str] = mapped_column(String(64), nullable=True, comment="学校性质",default='')

    planning_school_category: Mapped[str] = mapped_column(String(64), nullable=True, default='',
                                                          comment="学校（机构）类别,枚举 school_nature_lv2")
    planning_school_operation_type: Mapped[str] = mapped_column(String(64), nullable=True, default='',
                                                                comment="办学类型,枚举 school_nature_lv3")
    planning_school_org_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="学校办别")
    planning_school_level: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校星级")
    status: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="状态,枚举planningschool_status")
    kg_level: Mapped[str] = mapped_column(String(64), nullable=True, comment="星级,枚举kg_level", default='')
    planning_school_short_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="园所简称", default='')
    planning_school_en_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="园所英文名称", default='')
    create_planning_school_date: Mapped[str] = mapped_column(String(64), nullable=True, comment="建校年月", default='')
    social_credit_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="统一社会信用代码", default='')
    founder_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="枚举founder_type", default='')
    founder_type_lv2: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型二级,枚举founder_type_lv2", default='')
    founder_type_lv3: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者类型三级,枚举founder_type_lv3", default='')
    founder_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者名称", default='')
    founder_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="举办者识别码", default='')
    location_economic_attribute: Mapped[str] = mapped_column(String(64), nullable=True, comment="所属地经济属性,枚举economic_attributes",
                                                             default='')
    urban_ethnic_nature: Mapped[str] = mapped_column(String(64), nullable=True, comment="所在地民族属性,枚举ethnic_attributes", default='')
    leg_repr_certificatenumber: Mapped[str] = mapped_column(String(64), nullable=True, comment="法人证书号", default='')
    urban_rural_nature: Mapped[str] = mapped_column(String(64), nullable=True, comment="城乡性质,枚举urban_rural_nature", default='')
    planning_school_org_form: Mapped[str] = mapped_column(String(64), nullable=True, comment="办学组织形式", default='')
    planning_school_closure_date: Mapped[str] = mapped_column(String(64), nullable=True, comment="学校关闭日期",
                                                              default='')
    department_unit_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理行政部门单位号",
                                                        default='')
    sy_zones: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理行政部门所在地地区", default='')
    historical_evolution: Mapped[str] = mapped_column(Text, nullable=True, comment="历史沿革", default='')
    sy_zones_pro: Mapped[str] = mapped_column(String(64), nullable=True, comment="属地管理教育行政部门所在地（省级）",
                                              default='')

    primary_planning_school_entry_age: Mapped[str] = mapped_column(String(64), nullable=True, comment="小学入学年龄",
                                                                   default='')

    junior_middle_planning_school_entry_age: Mapped[str] = mapped_column(String(64), nullable=True,
                                                                         comment="初中入学年龄", default='')

    process_instance_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=0, comment="流程ID")
    workflow_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="工作流审核状态", default='')
    admin: Mapped[str] = mapped_column(String(64), nullable=True, comment="管理员", default='')
    admin_phone: Mapped[str] = mapped_column(String(64), nullable=True, comment="管理员手机", default='')
    org_center_info: Mapped[str] = mapped_column(String(255), nullable=True, comment="组织中心信息", default='')

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)

    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
