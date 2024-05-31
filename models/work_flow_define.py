from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime

from enum import Enum


class ProcessType(str, Enum):
    """
    借动
    调动
    入职
    信息修改
    变动
    """
    BORROW = "borrow"
    TRANSFER = "transfer"
    ENTRY = "entry"
    INFO = "info"
    CHANGE = "change"

    @classmethod
    def to_list(cls):
        return [cls.BORROW, cls.TRANSFER, cls.ENTRY, cls.INFO, cls.CHANGE]


class ProcessCode(str, Enum):
    """
    借入：borrow_in
    借出：borrow_out
    调入：transfer_in
    调出：transfer_out
    信息修改：info
    变动：change
    入职：entry
    """
    BORROW_IN = "borrow_in"
    BORROW_OUT = "borrow_out"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    INFO = "info"
    CHANGE = "change"
    ENTRY = "entry"

    @classmethod
    def to_list(cls):
        return [cls.BORROW_IN, cls.BORROW_OUT, cls.TRANSFER_IN, cls.TRANSFER_OUT, cls.INFO, cls.CHANGE, cls.ENTRY]

class ProcessName(str, Enum):
    """
    借入：borrow_in
    借出：borrow_out
    调入：transfer_in
    调出：transfer_out
    信息修改：info
    变动：change
    入职：entry
    """
    BORROW_IN = "借入"
    BORROW_OUT = "借出"
    TRANSFER_IN = "调入"
    TRANSFER_OUT = "调出"
    INFO = "教师信息修改"
    CHANGE = "教师变动"
    ENTRY = "教师入职"

    @classmethod
    def to_list(cls):
        return [cls.BORROW_IN, cls.BORROW_OUT,cls.TRANSFER_IN, cls.TRANSFER_OUT, cls.INFO, cls.CHANGE, cls.ENTRY]

class WorkFlowDefine(BaseDBModel):
    """
    流程code：process_code 主键
    流程名称：process_name
    流程描述：process_description
    流程类型：process_type
    借入/借出发起：borrow_initiate
    是否借入校审批：is_borrow_in_school_approval
    是否借出校审批：is_borrow_out_school_approval
    是否借入区审批：is_borrow_in_area_approval
    是否借出区审批：is_borrow_out_area_approval
    是否借动市审批：is_borrow_city_approval
    调入/调出发起：transfer_initiate
    是否调入校审批：is_transfer_in_school_approval
    是否调出校审批：is_transfer_out_school_approval
    是否调入区审批：is_transfer_in_area_approval
    是否调出区审批：is_transfer_out_area_approval
    是否调动市审批：is_transfer_city_approval
    是否信息修改校审批：is_info_school_approval
    是否信息修改区审批：is_info_area_approval
    是否信息修改市审批：is_info_city_approval
    是否变动校审批：is_change_school_approval
    是否变动区审批：is_change_area_approval
    是否变动市审批：is_change_city_approval
    是否入职校审批：is_entry_school_approval
    是否入职区审批：is_entry_area_approval
    是否入职市审批：is_entry_city_approval
    是否作废：status
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_work_flow_define'
    __table_args__ = {'comment': 'work_flow_define信息表'}

    process_code: Mapped[str] = mapped_column(String(64), primary_key=True, autoincrement=False, comment="流程code")
    process_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程名称")
    process_description: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程描述")
    process_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="流程类型")

    is_borrow: Mapped[bool] = mapped_column(default=False, comment="true:借出")
    borrow_initiate: Mapped[bool] = mapped_column(default=False, comment="true:借出发起")
    is_borrow_in_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否借入校审批")
    is_borrow_out_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否借出校审批")
    is_borrow_in_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否借入区审批")
    is_borrow_out_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否借出区审批")
    is_borrow_city_approval: Mapped[bool] = mapped_column(default=False, comment="是否借动市审批")

    is_transfer: Mapped[bool] = mapped_column(default=False, comment="true:调出")
    transfer_initiate: Mapped[bool] = mapped_column(default=False, comment="true:调出发起")
    is_transfer_in_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否调入校审批")
    is_transfer_out_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否调出校审批")
    is_transfer_in_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否调入区审批")
    is_transfer_out_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否调出区审批")
    is_transfer_city_approval: Mapped[bool] = mapped_column(default=False, comment="是否调动市审批")

    is_info_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否信息修改校审批")
    is_info_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否信息修改区审批")
    is_info_city_approval: Mapped[bool] = mapped_column(default=False, comment="是否信息修改市审批")

    is_change_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否变动校审批")
    is_change_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否变动区审批")
    is_change_city_approval: Mapped[bool] = mapped_column(default=False, comment="是否变动市审批")

    is_entry_school_approval: Mapped[bool] = mapped_column(default=False, comment="是否入职校审批")
    is_entry_area_approval: Mapped[bool] = mapped_column(default=False, comment="是否入职区审批")
    is_entry_city_approval: Mapped[bool] = mapped_column(default=False, comment="是否入职市审批")

    status: Mapped[bool] = mapped_column(default=False, nullable=False, comment="是否作废")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    create_time: Mapped[date] = mapped_column(Date, default=datetime.now().date, comment="创建时间")
