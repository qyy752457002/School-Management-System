from pydantic import BaseModel, Field
from fastapi import Query
from datetime import date, datetime

from typing import Optional
from models.transfer_details import TransferType
from models.public_enum import Gender


# 异动相关模型
class TeacherTransactionModel(BaseModel):
    """
    异动类型：transaction_type
    异动原因：transaction_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：transaction_time
    """
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_reason: str = Field("", title="异动原因", description="异动原因")
    transaction_remark: str = Field("", title="备注", description="备注")
    operator_name: str = Field(..., title="操作人", description="操作人")
    transaction_time: datetime = Field(..., title="操作时间", description="操作时间")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")

class TeacherTransactionUpdateModel(BaseModel):
    """
    teacher_transaction：teacher_transaction_id
    异动类型：transfer_type
    异动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    teacher_transaction_id: int = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_reason: str = Field(..., title="异动原因", description="异动原因")
    transaction_remark: str = Field("", title="备注", description="备注")
    operator_name: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    transaction_time: datetime = Field(..., title="操作时间", description="操作时间")


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
    所属机构：teacher_employer
    教师性别：teacher_gender
    申请人：operator_name
    审批人：approval_name
    教职工号：teacher_number
    """
    teacher_name: Optional[str] = Field("", title="姓名", description="姓名")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    operator_name: Optional[str] = Field("", title="申请人", description="申请人")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    teacher_employer: Optional[int] = Field(None, title="所属机构", description="所属机构")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")


class TeacherTransactionApproval(BaseModel):
    """
    异动审批中四项中的基本模型
    异动审批id：transaction_approval_id
    教师姓名：teacher_name
    教师ID：teacher_id
    所属机构：teacher_employer
    学校名称：school_name
    异动id：transaction_id
    教职工号： teacher_number
    教师性别：teacher_gender
    异动类型：transaction_type
    异动原因：transaction_reason
    申请人：operator_name
    审批人：approval_name
    申请时间：transaction_time
    审批时间：approval_time
    """
    transaction_approval_id: int = Field(..., title="调动审批id", description="调动审批id")
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_employer: int = Field(..., title="所属机构", description="所属机构")
    school_name: str = Field(..., title="学校名称", description="学校名称")
    transaction_id: int = Field(..., title="异动id", description="异动id")
    teacher_number: Optional[str] = Field(None, title="教职工号", description="教职工号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_reason: str = Field("", title="异动原因", description="异动原因")
    operator_name: str = Field(..., title="申请人", description="申请人")
    approval_name: str = Field("", title="审批人", description="审批人")
    transaction_time: Optional[datetime] = Field(None, title="申请时间", description="申请时间")


class TransactionLaunch(TeacherTransactionApproval):
    """我发起"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")


class TransactionSubmitted(TeacherTransactionApproval):
    """待审核"""
    pass


class TransactionApproved(TeacherTransactionApproval):
    """已审核"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")


class TransactionAll(TeacherTransactionApproval):
    """所有"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")



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
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    transfer_in_date: date = Field(..., title="调入日期", description="调入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    transfer_out_date: date = Field(..., title="调出日期", description="调出日期")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调入或者调出")


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
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    transfer_in_date: date = Field(..., title="调入日期", description="调入日期")
    current_unit: str = Field("", title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    current_district: str = Field("", title="现行政属地", description="现行政属地")
    transfer_out_date: date = Field(..., title="调出日期", description="调出日期")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调动类型")


class TransferDetailsUpdateModel(BaseModel):
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
    """
    transfer_details_id: int = Field(..., title="transfer_details_id", description="transfer_details_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field(..., title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")


class TransferDetailsGetModel(TransferDetailsUpdateModel):
    """
    单个教师的所有的调动记录
    """
    pass


class TeacherTransferQueryModel(BaseModel):
    """
    调动审批的查询
    教师姓名：teacher_name
    所属机构：teacher_employer
    教师性别：teacher_gender
    申请人：operator_name
    审批人：approval_name
    身份证号：teacher_id_number
    """
    teacher_name: Optional[str] = Field("", title="姓名", description="姓名")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    operator_name: Optional[str] = Field("", title="申请人", description="申请人")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    teacher_employer: Optional[int] = Field(None, title="所属机构", description="所属机构")
    teacher_id_number: Optional[str] = Field("", title="身份证号", description="身份证号")
class TeacherTransferApproval(BaseModel):
    """
    调动审批中的四个基本模型
    调动审批id：transfer_approval_id
    教师姓名：teacher_name
    教师ID：teacher_id
    身份证号：teacher_id_number
    性别：teacher_gender
    申请人：operator_name
    审批人：approval_name
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    操作时间：operation_time
    """
    transfer_approval_id: int = Field(..., title="调动审批id", description="调动审批id")
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    teacher_id_number: str = Field(..., title="身份证号", description="身份证号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    operator_name: str = Field(..., title="申请人", description="申请人")
    approval_name: str = Field("", title="审批人", description="审批人")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")


class TransferLaunch(TeacherTransferApproval):
    """我发起"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")


class TransferSubmitted(TeacherTransferApproval):
    """待审核"""
    pass


class TransferApproved(TeacherTransferApproval):
    """已审核"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")


class TransferAll(TeacherTransferApproval):
    """所有"""
    approval_status: str = Field("submitting", title="审批状态", description="审批状态")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")

#借动的模型
class TransferInternalCreateModel(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    仅仅是校内岗位调动
    """

    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
    transfer_type: TransferType = Field("internal", title="调动类型", description="调动类型")


class TransferDetailsCreateReModel(BaseModel):
    """
    校内岗位调动返回模型
    """
    transfer_details_id: int = Field(..., title="transfer_details_id", description="transfer_details_id")
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    original_district: str = Field(..., title="原行政属地", description="原行政属地")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")


class TransferDetailsModelQuery(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    现单位：current_unit
    现岗位：current_position
    调动原因：transfer_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    """
    original_unit: str = Field(..., title="原单位", description="原单位")
    original_position: str = Field(..., title="原岗位", description="原岗位")
    current_unit: str = Field(..., title="现单位", description="现单位")
    current_position: str = Field(..., title="现岗位", description="现岗位")
    transfer_reason: str = Field(..., title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    operator: str = Field(..., title="操作人", description="操作人")
    teacher_id: int = Field(..., title="教师ID", description="教师ID")
    operation_time: datetime = Field(..., title="操作时间", description="操作时间")
