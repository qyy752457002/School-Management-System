from pydantic import BaseModel, Field, model_validator, ValidationError, field_validator
from fastapi import Query
from datetime import date, datetime

from typing import Optional
from models.transfer_details import TransferType
from models.public_enum import Gender

from business_exceptions.teacher_transction import OriginPositionError, CurrentPositionError, PositionDateError

from enum import Enum



class ApprovalStatus(str, Enum):
    """
    未审批：pending
    审批中：progressing
    已撤回：revoked
    已通过：approved
    已拒绝：rejected
    """
    PENDING = "pending"
    PROGRESSING = "progressing"
    REVOKED = "revoked"
    APPROVED = "approved"
    REJECTED = "rejected"
    @classmethod
    def to_list(cls):
        return [status.value for status in cls]
class EmploymentStatus(str, Enum):
    """
    正常在职：active
    已提交：submitted
    未提交：unsubmitted
    调出中：transfer_out
    借出中：borrowed_out
    调入中：transfer_in
    借入中：borrowed_in
    病休：sick_leave
    进修：training
    交流：exchange
    出国：abroad
    早退休：early_retirement
    落聘：unemployed
    死亡：deceased
    其他：other
    """
    ACTIVE = "active"
    SUBMITTED = "submitted"
    UNSUBMITTED = "unsubmitted"
    TRANSFER_OUT = "transfer_out"
    BORROWED_OUT = "borrowed_out"
    TRANSFER_IN = "transfer_in"
    BORROWED_IN = "borrowed_in"
    SICK_LEAVE = "sick_leave"
    TRAINING = "training"
    EXCHANGE = "exchange"
    ABROAD = "abroad"
    EARLY_RETIREMENT = "early_retirement"
    UNEMPLOYED = "unemployed"
    DECEASED = "deceased"
    OTHER = "other"

    @classmethod
    def to_list(cls):
        return [status.value for status in cls]


class TransactionType(str, Enum):
    """
    校内岗位调动：internal
    病休：sick_leave
    进修：training
    交流：exchange
    出国：abroad
    早退休：early_retirement
    落聘：unemployed
    死亡：deceased
    其他：other
    """
    INTERNAL = "internal"
    SICK_LEAVE = "sick_leave"
    TRAINING = "training"
    EXCHANGE = "exchange"
    ABROAD = "abroad"
    EARLY_RETIREMENT = "early_retirement"
    UNEMPLOYED = "unemployed"
    DECEASED = "deceased"
    OTHER = "other"

    @classmethod
    def to_list(cls):
        return [status.value for status in cls]


# 异动相关模型
class TeacherTransactionModel(BaseModel):
    """
    异动类型：transaction_type
    备注：remark
    原岗位：original_position
    现岗位：current_position
    任职日期：position_date
    操作人：operator
    教师ID：teacher_id
    操作时间：transaction_time
    流程ID：process_id
    """
    transaction_type: TransactionType = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    position_date: Optional[date] = Field(None, title="任职日期", description="任职日期")
    operator_name: str = Field(..., title="操作人", description="操作人")
    transaction_time: datetime = Field(datetime.now(), title="操作时间", description="操作时间")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    process_id: int = Field(..., title="流程ID", description="流程ID")

    @model_validator(mode='after')
    def check_transaction_type(self):
        if self.transaction_type == "internal":
            """
            如果是校内，原岗位，现岗位，任职日期都是必填的
            """
            if not self.original_position:
                raise OriginPositionError()
            if not self.current_position:
                raise CurrentPositionError()
            if not self.position_date:
                raise PositionDateError()
        return self


class TeacherTransactionUpdateModel(BaseModel):
    """
    teacher_transaction：teacher_transaction_id
    异动类型：transfer_type
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：transaction_time
    """
    teacher_transaction_id: int = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    position_date: Optional[date] = Field(None, title="任职日期", description="任职日期")
    operator_name: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    transaction_time: datetime = Field(..., title="操作时间", description="操作时间")
    process_id: int = Field(..., title="流程ID", description="流程ID")


class TeacherTransactionGetModel(TeacherTransactionUpdateModel):
    """
    teacher_transaction：teacher_transaction_id
    异动类型：transfer_type
    备注：remark
    操作人：operator_name
    审批人：approval_name
    申请时间：transaction_time
    审批时间：approval_time
    节点实例ID：process_instance_id
    """
    teacher_transaction_id: int = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    remark: Optional[str] = Field("", title="备注", description="备注")
    operator_name: Optional[str] = Field("", title="操作人", description="操作人")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    transaction_time: datetime = Field(..., title="申请时间", description="申请时间")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")
    process_instance_id: int = Field(..., title="流程ID", description="流程ID")


class TeacherTransactionQuery(BaseModel):
    """
    查看系统有没有该老师用的模型
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    """
    teacher_name: str = Query(..., title="姓名", description="姓名")
    teacher_id_type: str = Query(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Query(..., title="证件号码", description="证件号码")


class TeacherTransactionQueryRe(BaseModel):
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: str = Field(..., title="性别", description="性别")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_number: str = Field(..., title="教师编号", description="教师编号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")


class TeacherAddModel(BaseModel):
    """
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    教师性别：teacher_gender
    出生日期：teacher_date_of_birth
    """
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: Gender = Field(..., title="性别", description="性别")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")


class TeacherAddReModel(BaseModel):
    """
    教师id：teacher_id
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    教师性别：teacher_gender
    出生日期：teacher_date_of_birth
    """
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: Gender = Field(..., title="性别", description="性别")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")


class TeacherTransactionQueryModel(BaseModel):
    """
    异动审批的查询
    教师姓名：teacher_name
    教职工号：teacher_number
    身份证类型：teacher_id_type
    身份证号：teacher_id_number
    所属机构：teacher_employer
    教师性别：teacher_gender
    申请时间：transaction_time
    变动类型：transaction_type
    申请人：operator_name
    # 审批人：approval_name
    所在区县：teacher_district
    """
    teacher_name: Optional[str] = Field("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    transaction_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    transaction_type: Optional[str] = Field("", title="异动类型", description="异动类型")
    operator_name: Optional[str] = Field("", title="申请人", description="申请人")
    teacher_district: Optional[str] = Field("", title="所在区县", description="所在区县")
    # approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    teacher_employer: Optional[int] = Field(None, title="所属机构", description="所属机构")


class TeacherTransactionApproval(BaseModel):
    """
    异动审批中四项中的基本模型
    流程审批id：process_id
    教师姓名：teacher_name
    教师ID：teacher_id
    证件类型：teacher_id_type
    证件号：teacher_id_number
    所属机构：teacher_employer
    学校名称：school_name
    异动id：transaction_id
    教职工号： teacher_number
    教师性别：teacher_gender
    异动类型：transaction_type
    # 申请人：operator_name
    # 审批人：approval_name
    所在区县：teacher_district
    申请时间：transaction_time
    备注：remark
    # 审批时间：approval_time
    """
    process_instance_id: int = Field(..., title="流程审批实例id", description="流程审批实例id")
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_employer: int = Field(..., title="所属机构", description="所属机构")
    school_name: str = Field(..., title="学校名称", description="学校名称")
    transaction_id: int = Field(..., title="异动id", description="异动id")
    teacher_number: Optional[str] = Field(None, title="教职工号", description="教职工号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    teacher_district: Optional[str] = Field("", title="所在区县", description="所在区县")
    # operator_name: str = Field(..., title="申请人", description="申请人")
    # approval_name: str = Field("", title="审批人", description="审批人")
    remark: Optional[str] = Field("", title="备注", description="备注")
    transaction_time: Optional[datetime] = Field(None, title="申请时间", description="申请时间")




# 调动相关模型
class TransferDetailsModel(BaseModel):
    """

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
    调动类型：transfer_type
    流程id：process_instance_id
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district: Optional[str] = Field(..., title="原行政属地", description="原行政属地")
    transfer_in_date: Optional[date] = Field(None, title="调入日期", description="调入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: Optional[str] = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    transfer_out_date: Optional[date] = Field(..., title="调出日期", description="调出日期")
    transfer_reason: str = Field("", title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调入或者调出")
    process_instance_id: int = Field(0, title="流程ID", description="流程ID")


class TransferDetailsReModel(BaseModel):
    """
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
    """
    transfer_details_id: int = Field(..., title="transfer_details_id", description="transfer_details_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    transfer_in_date: Optional[date] = Field(..., title="调入日期", description="调入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    transfer_out_date: Optional[date] = Field(..., title="调出日期", description="调出日期")
    transfer_reason: str = Field("", title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调动类型")


class TransferDetailsGetModel(BaseModel):
    """
    单个教师的所有的调动记录
    """
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")



class TeacherTransferQueryModel(BaseModel):
    """
    调动审批的查询
    教师姓名：teacher_name
    教职工号：teacher_number
    身份证类型：teacher_id_type
    身份证号：teacher_id_number
    教师性别：teacher_gender
    原行政属地：original_district
    原单位：original_unit
    现行政属地：current_district
    现单位：current_unit
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name

    """
    teacher_name: Optional[str] = Field("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")


class TeacherTransferQueryReModel(BaseModel):

    """
    调动审批的查询
    调动主键：transfer_details_id
    教师姓名：teacher_name
    教职工号：teacher_number
    身份证类型：teacher_id_type
    身份证号：teacher_id_number
    教师性别：teacher_gender
    原行政属地：original_district
    原单位：original_unit
    现行政属地：current_district
    现单位：current_unit
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name
    流程实例id：process_instance_id

    """
    transfer_details_id: int = Field(0, title="调动主键", description="调动主键")
    teacher_name: str= Field("", title="姓名", description="姓名")
    teacher_number: Optional[int] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    process_instance_id: int = Field(0, title="流程实例id", description="流程实例id")





# 借动的模型
class TeacherBorrowModel(BaseModel):
    """

    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    借入日期：borrow_in_date
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    借出日期：borrow_out_date
    借动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    借动类型：borrow_type
    流程id：process_instance_id
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district: Optional[str] = Field(..., title="原行政属地", description="原行政属地")
    borrow_in_date: Optional[date] = Field(None, title="借入日期", description="借入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: Optional[str] = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    borrow_out_date: Optional[date] = Field(..., title="借出日期", description="借出日期")
    transfer_reason: str = Field("", title="借动原因", description="借动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    borrow_type: TransferType = Field("borrow_in", title="借动类型", description="借入或者借出")
    process_instance_id: int = Field(0, title="流程ID", description="流程ID")


class TeacherBorrowReModel(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    借入日期：borrow_in_date
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    借出日期：borrow_out_date
    借动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    teacher_borrow_id: int = Field(..., title="teacher_borrow_id", description="teacher_borrow_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    borrow_in_date: Optional[date] = Field(..., title="借入日期", description="借入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    borrow_out_date: Optional[date] = Field(..., title="借出日期", description="借出日期")
    transfer_reason: str = Field("", title="借动原因", description="借动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    borrow_type: TransferType = Field("borrow_in", title="借动类型", description="借动类型")


class TeacherBorrowGetModel(BaseModel):
    """
    单个教师的所有的借动记录
    """
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")



class TeacherBorrowQueryModel(BaseModel):
    """
    借动审批的查询
    教师姓名：teacher_name
    教职工号：teacher_number
    身份证类型：teacher_id_type
    身份证号：teacher_id_number
    教师性别：teacher_gender
    原行政属地：original_district
    原单位：original_unit
    现行政属地：current_district
    现单位：current_unit
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name

    """
    teacher_name: Optional[str] = Field("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")


class TeacherBorrowQueryReModel(BaseModel):

    """
    借动审批的查询
    借动主键：teacher_borrow_id
    教师姓名：teacher_name
    教职工号：teacher_number
    身份证类型：teacher_id_type
    身份证号：teacher_id_number
    教师性别：teacher_gender
    原行政属地：original_district
    原单位：original_unit
    现行政属地：current_district
    现单位：current_unit
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name
    流程实例id：process_instance_id

    """
    teacher_borrow_id: int = Field(0, title="借动主键", description="借动主键")
    teacher_name: str= Field("", title="姓名", description="姓名")
    teacher_number: Optional[int] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_district: Optional[str] = Field("", title="原行政属地", description="原行政属地")
    original_region: Optional[str] = Field("", title="原地域管辖区域", description="原地域管辖区域")
    original_unit: Optional[str] = Field("", title="原单位", description="原单位")
    current_district: Optional[str] = Field("", title="现行政属地", description="现行政属地")
    current_region: Optional[str] = Field("", title="现地域管辖区域", description="现地域管辖区域")
    current_unit: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    operation_time: Optional[date] = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[date] = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    process_instance_id: int = Field(0, title="流程实例id", description="流程实例id")
