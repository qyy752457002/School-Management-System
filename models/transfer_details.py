from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime
from enum import Enum


class TransferType(str, Enum):
    """
    调动类型
    """
    IN = "transfer_in"
    OUT = "transfer_out"

    @classmethod
    def to_list(cls):
        return [cls.IN, cls.OUT,]


class TransferDetails(BaseDBModel):
    """
    transfer_details：transfer_details_id
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    调入日期：transfer_in_date
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    调出日期：transfer_out_date
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    删除状态：is_deleted
    调动类型：transfer_type
    """
    __tablename__ = 'lfun_transfer_details'
    __table_args__ = {'comment': 'transfer_details信息表'}

    transfer_details_id: Mapped[int] = mapped_column(primary_key=True, comment="transfer_detailsID")
    original_unit: Mapped[str] = mapped_column(String(64), nullable=True, comment="原单位")
    original_position: Mapped[str] = mapped_column(String(64), nullable=True, comment="原岗位")
    original_district: Mapped[str] = mapped_column(String(64), nullable=True, comment="原行政属地")
    original_region: Mapped[str] = mapped_column(String(64), nullable=True, comment="原管辖区域")
    transfer_in_date: Mapped[date] = mapped_column(Date, nullable=True, comment="调入日期")
    current_unit: Mapped[str] = mapped_column(String(64), nullable=True, comment="现单位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=True, comment="现岗位")
    current_district: Mapped[str] = mapped_column(String(64), nullable=True, comment="现行政属地")
    current_region: Mapped[str] = mapped_column(String(64), nullable=True, comment="现管辖区域")
    transfer_out_date: Mapped[date] = mapped_column(Date, nullable=True, comment="调出日期")
    transfer_reason: Mapped[str] = mapped_column(String(64), nullable=True, comment="调动原因")
    remark: Mapped[str] = mapped_column(String(64), nullable=True, comment="备注")
    operator_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="操作人")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    operation_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(),  nullable=False, comment="操作时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    transfer_type: Mapped[str] = mapped_column(String(255), nullable=False, comment="调动类型")
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                 default="submitting")
    process_instance_id: Mapped[int] = mapped_column(nullable=False, comment="流程ID", default=0)
