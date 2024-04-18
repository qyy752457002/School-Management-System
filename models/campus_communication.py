from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class CampusCommunication(BaseDBModel):
    """
    校区 通信表
    """
    __tablename__ = 'lfun_campus_communications'
    __table_args__ = {'comment': '校区通信表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    campus_id: Mapped[int] = mapped_column( nullable=True  , comment="校区id",default=0)

    postal_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="邮政编码")
    fax_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="传真电话")
    email: Mapped[str] = mapped_column(String(64), nullable=False, comment="单位电子信箱")

    campus_web_url: Mapped[str] = mapped_column(String(64), nullable=False, comment="校园网域名")
    related_license_upload: Mapped[str] = mapped_column(String(64), nullable=False, comment="相关证照上传")
    detailed_address: Mapped[str] = mapped_column(String(64), nullable=False, comment="园所详细地址")

    contact_number: Mapped[str] = mapped_column(String(64), nullable=False, comment="联系电话")
    area_code: Mapped[str] = mapped_column(String(64), nullable=False, comment="电话区号")
    long: Mapped[str] = mapped_column(String(64), nullable=False, comment="所在经度")
    lat: Mapped[str] = mapped_column(String(64), nullable=False, comment="所在纬度")
    leg_repr_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="法定代表人姓名")

    party_leader_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="党组织负责人姓名")
    party_leader_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="党组织负责人职务")
    adm_leader_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政负责人姓名")
    adm_leader_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="行政负责人职务")
    loc_area: Mapped[str] = mapped_column(String(64), nullable=False, comment="园所所在地区")

    loc_area_pro: Mapped[str] = mapped_column(String(64), nullable=False, comment="园所所在地(省级)")
    campus_leader_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="校区负责人姓名")
    campus_leader_position: Mapped[str] = mapped_column(String(20), nullable=False, comment="校区负责人职位")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

