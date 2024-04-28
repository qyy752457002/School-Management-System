from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TransferDetails(BaseDBModel):
    """
    transfer_details：transfer_details_id
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_transfer_details'
    __table_args__ = {'comment': 'transfer_details信息表'}

    transfer_details_id: Mapped[int] = mapped_column(primary_key=True, comment="transfer_detailsID")
    original_unit: Mapped[str] = mapped_column(String(64), nullable=False, comment="原单位")
    original_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="原岗位")
    current_unit: Mapped[str] = mapped_column(String(64), nullable=False, comment="现单位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="现岗位")
    transfer_reason: Mapped[str] = mapped_column(String(64), nullable=False, comment="调动原因")
    remark: Mapped[str] = mapped_column(String(64), nullable=False, comment="备注")
    operator: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    operation_time: Mapped[date] = mapped_column(Date, nullable=False, comment="操作时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    approval_status: Mapped[str] = mapped_column(String(255), nullable=False, comment="审批状态",
                                                         default="submitting")
    
