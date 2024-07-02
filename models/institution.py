from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Institution(BaseDBModel):
    """
    行政事业单位表
    institution_category: str = Field(...,   description=" 单位分类",examples=['事业单位'])
    institution_type: str = Field(...,   description="单位类型 ",examples=[''])
    leg_repr_certificatenumber: str = Field(...,   description=" 法人证书号",examples=['DF1256565656'])
    is_entity: str = Field(...,   description=" 是否实体",examples=['是'])
    membership_no: str = Field(...,   description=" 隶属单位号",examples=['DFF1565165656'])
    membership_category: str = Field(...,   description=" 隶属单位类型",examples=['行政'])


    """
    __tablename__ = 'lfun_institutions'
    __table_args__ = {'comment': '行政事业单位表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)

    institution_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="单位名称")
    institution_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="机构代码")
    institution_en_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="单位名称英文")
    create_institution_date: Mapped[str] = mapped_column(String(64), nullable=True, comment="成立年月",default='')
    department_unit_number: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="属地管理行政部门单位号")
    sy_zones: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="属地管理行政部门所在地地区")
    social_credit_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="统一社会信用代码")
    postal_code: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="邮政编码")
    urban_rural_nature: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城乡性质")
    status: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="状态")
    block: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="地域管辖区")
    borough: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="行政管辖区")
    fax_number: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="传真电话")
    email: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="单位电子信箱")

    contact_number: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="联系电话")
    area_code: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="电话区号")

    leg_repr_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="法定代表人姓名")
    party_leader_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="党组织负责人姓名")
    party_leader_position: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="党组织负责人职务")
    adm_leader_name: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="行政负责人姓名")
    adm_leader_position: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="行政负责人职务")
    detailed_address: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="详细地址")
    related_license_upload: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="相关证照上传")

    long: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="所在经度")
    lat: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="所在纬度")
    website_url: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="网址")

    institution_category: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 单位分类")
    institution_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="单位类型 公办 民办")
    location_economic_attribute: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 所在地经济属性")
    urban_ethnic_nature: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 所在地民族属性")
    leg_repr_certificatenumber: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 法人证书号")
    is_entity: Mapped[bool] = mapped_column(  nullable=True,default=False, comment=" 是否实体")
    membership_no: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 隶属单位号")
    membership_category: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment=" 隶属单位类型")
    process_instance_id: Mapped[int] = mapped_column(nullable=True,default=0, comment="流程ID")
    workflow_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="工作流审核状态", default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="更新时间")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

