from pydantic import BaseModel, Field, model_validator
from fastapi import Query
from datetime import date, datetime

from typing import Optional
from models.transfer_details import TransferType
from models.teacher_borrow import BorrowType
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
    离休：retire_honor
    退休：retire
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
    RETIRE = "retire"
    RETIRE_HONOR = "retire_honor"

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
    离休：retire_honor
    退休：retire
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
    RETIRE = "retire"
    RETIRE_HONOR = "retire_honor"

    @classmethod
    def to_list(cls):
        return [status.value for status in cls]

    @classmethod
    def to_dict(cls):
        return {
            cls.INTERNAL: "校内岗位调动",
            cls.SICK_LEAVE: "病休",
            cls.TRAINING: "进修",
            cls.EXCHANGE: "交流",
            cls.ABROAD: "出国（境）",
            cls.EARLY_RETIREMENT: "内退",
            cls.UNEMPLOYED: "落聘",
            cls.DECEASED: "死亡",
            cls.OTHER: "其他",
            cls.RETIRE: "退休",
            cls.RETIRE_HONOR: "离休"
        }

    @classmethod
    def get_chinese(cls, value):
        return cls.to_dict().get(value, "未知")


# 异动相关模型
class TeacherTransactionModel(BaseModel):
    """
    异动类型：transaction_type
    备注：remark
    原岗位：original_position
    现岗位：current_position
    任职日期：position_date
    教师ID：teacher_id
    操作时间：transaction_time
    """
    transaction_type: TransactionType = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    # retire_number: str|None = Field("", title="离退休证号", description="")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    position_date: Optional[date] | None = Field(None, title="任职日期", description="任职日期")
    transaction_time: Optional[datetime] | None = Field(datetime.now(), title="操作时间", description="操作时间")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data

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
    transaction_id: int | str = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    position_date: Optional[date] | None = Field(None, title="任职日期", description="任职日期")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    transaction_time: Optional[datetime] | None = Field(default=datetime.now(), title="操作时间",
                                                        description="操作时间")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "transaction_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TeacherTransactionGetModel(BaseModel):
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
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    transaction_id: int | str = Field(..., title="teacher_transaction_id", description="teacher_transaction_id")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    remark: Optional[str] = Field("", title="备注", description="备注")
    transaction_time: datetime = Field(..., title="申请时间", description="申请时间")
    is_active: bool = Field(..., title="是否已经恢复在职", description="是否已经恢复在职")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "transaction_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TeacherTransactionQuery(BaseModel):
    """
    查看系统有没有该老师用的模型
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    """
    teacher_name: str = Query(..., title="姓名", description="姓名")
    teacher_id_type: str = Query(..., title="身份证件类型", description="证件类型")
    teacher_id_number: str = Query(..., title="证件号码", description="证件号码")


class TeacherTransactionQueryRe(BaseModel):
    teacher_id: int | str = Field(None, title="教师ID", description="教师ID")
    teacher_name: str = Field(..., title="姓名", description="教师名称")
    teacher_gender: Gender = Field(..., title="教师性别", description="教师性别")
    teacher_id_type: str = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")
    teacher_employer: int | str = Field(0, title="任职单位", description="任职单位")
    teacher_avatar: str = Field("", title="头像", description="头像")
    mobile: str | None = Field("", title="手机号", description="手机号")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TeacherAddModel(BaseModel):
    """
    姓名：teacher_name
    证件类型：teacher_id_type
    证件号码：teacher_id_number
    教师性别：teacher_gender
    出生日期：teacher_date_of_birth
    """
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id_type: str = Field(..., title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: Gender = Field(..., title="性别", description="性别")
    teacher_date_of_birth: date | None = Field(..., title="出生日期", description="出生日期")


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
    teacher_id_type: str = Field(..., title="身份证件类型", description="证件类型")
    teacher_id_number: str = Field(..., title="证件号码", description="证件号码")
    teacher_gender: Gender = Field(..., title="性别", description="性别")
    teacher_date_of_birth: date = Field(..., title="出生日期", description="出生日期")

    # @model_validator(mode='before')
    # @classmethod
    # def check_id_before(self, data: dict):
    #     if isinstance(data["teacher_id"], str):
    #         data["teacher_id"] = int(data["teacher_id"])
    #     elif isinstance(data["teacher_id"], int):
    #         data["teacher_id"] = str(data["teacher_id"])
    #     else:
    #         pass
    #
    #     return data


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
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Query("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Query("", title="身份证件号", description="证件号")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别")
    transaction_time_s: Optional[date] = Query(None, title="申请开始时间", description="申请开始时间")
    transaction_time_e: Optional[date] = Query(None, title="申请结束时间", description="申请结束时间")
    transaction_type: Optional[str] = Query("", title="异动类型", description="异动类型")
    teacher_employer: Optional[int | str] = Query(None, title="所属机构", description="所属机构")
    borough: Optional[str] = Query("", title="所在区县", description="所在区县")
    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


class TeacherTransactionQueryReModel(BaseModel):
    teacher_name: str = Field(..., title="姓名", description="姓名")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="身份证件号", description="证件号")
    transaction_id: int | str = Field(..., title="异动id", description="异动id")
    teacher_number: Optional[str] = Field(None, title="教职工号", description="教职工号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    transaction_type: str = Field(..., title="异动类型", description="异动类型")
    transaction_remark: Optional[str] = Field("", title="备注", description="备注")
    transaction_time: Optional[datetime] = Field(None, title="申请时间", description="申请时间")
    school_name: Optional[str] = Field("", title="所属机构", description="所属机构")
    borough: Optional[str] = Field("", title="所在区县", description="所在区县")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "transaction_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


# 离退休相关模型
class TeacherRetireQueryRe(BaseModel):
    """
    教师姓名：teacher_name
    # 教师ID：teacher_id
    身份证号：id_number
    性别：gender
    任职单位：employer
    # 最高学历：highest_education
    政治面貌：political_status
    是否在编：in_post
    用人形式：employment_form
    进本校时间：enter_school_time
    审核状态：approval_status
    """
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    teacher_name: str = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: str = Query("", title="性别", description="性别", example="男")
    teacher_employer: Optional[int | str] = Query(None, title="任职单位", description="任职单位", example="xx学校")
    highest_education: Optional[str] = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: Optional[str] = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    enter_school_time: Optional[date] | None = Query(None, title="进本校时间", description="进本校时间",
                                                     example="2010-01-01")
    retire_date: Optional[date] = Query(None, title="离退休时间", description="离退休时间", example="2020-01-01")
    school_name: Optional[str] = Query("", title="", description="", example="")
    retire_number: str = Field('', title="离退休证号", description="离退休证号")
    teacher_main_status: str = Field(..., title="教师状态", description="教师状态")
    teacher_sub_status: str = Field(..., title="教师子状态", description="教师子状态")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TeacherRetireQuery(BaseModel):
    """
    """
    teacher_name: str = Query("", title="姓名", description="姓名", example="张三")
    teacher_id_number: str = Query("", title="身份证号", description="身份证号", example="123456789012345678")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别", example="男")
    teacher_employer: Optional[int | str] = Query(None, title="任职单位", description="任职单位", example="xx学校")
    highest_education: str = Query("", title="最高学历", description="最高学历", example="本科")
    political_status: str = Query("", title="政治面貌", description="政治面貌", example="群众")
    in_post: Optional[bool] = Query(None, title="是否在编", description="是否在编", example="yes")
    enter_school_time_s: Optional[date] = Query(None, title="进本校时间", description="进本校时间",
                                                example="2010-01-01")
    enter_school_time_e: Optional[date] = Query(None, title="进本校时间", description="进本校时间",
                                                example="2010-01-01")
    retire_date_s: Optional[date] = Query(None, title="非在职时间起始", description="", example="2010-01-01")
    retire_date_e: Optional[date] = Query(None, title="非在职时间截止", description="", example="2010-01-01")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


class TeacherRetireCreateModel(BaseModel):
    transaction_type: TransactionType = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    transaction_time: Optional[datetime] | None = Field(default=datetime.now(), title="操作时间",
                                                        description="操作时间")
    retire_date: Optional[date] | None = Field(None, title="离退休时间", description="离退休时间")
    retire_number: str = Field(..., title="离退休证号", description="离退休证号")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


class TeacherRetireUpdateModel(BaseModel):
    teacher_retire_id: int | str = Field(..., title="teacher_retire_id", description="teacher_retire_id")
    transaction_type: TransactionType = Field(..., title="异动类型", description="异动类型")
    transaction_remark: str = Field("", title="备注", description="备注")
    teacher_id: int | str = Field(..., title="教师ID", description="教师ID")
    transaction_time: Optional[datetime] | None = Field(default=datetime.now(), title="操作时间",
                                                        description="操作时间")
    retire_date: Optional[date] | None = Field(None, title="离退休时间", description="离退休时间")
    retire_number: str = Field(..., title="离退休证号", description="离退休证号")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "teacher_retire_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


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

    original_unit_id: Optional[int | str] = Field(None, title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] | None = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] | None = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] | None = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] | None = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] | None = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] | None = Field(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] | None = Field("", title="原单位", description="原单位")
    transfer_in_date: Optional[date] | None = Field(None, title="调入日期", description="调入日期")

    current_unit_id: Optional[int | str] | None = Field(None, title="现单位", description="现单位")
    current_unit_name: Optional[str] | None = Field("", title="现单位", description="现单位")
    current_position: str = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] | None = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] | None = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] | None = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] | None = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] | None = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] | None = Field(None, title="现管辖区域区", description="现管辖区域区")
    transfer_out_date: Optional[date] | None = Field(None, title="调出日期", description="调出日期")

    transfer_reason: str = Field("", title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    teacher_id: Optional[int | str] | None = Field(None, title="教师ID", description="教师ID")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调入或者调出")
    process_instance_id: int | str = Field(0, title="流程ID", description="流程ID")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "original_unit_id", "process_instance_id", "current_unit_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


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
    transfer_details_id: int | str = Field(..., title="transfer_details_id", description="transfer_details_id")

    original_unit_id: Optional[int | str] = Field(None, title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] | None = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] | None = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] | None = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] | None = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] | None = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] | None = Field(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] | None = Field("", title="原单位", description="原单位")
    transfer_in_date: Optional[date] | None = Field(None, title="调入日期", description="调入日期")

    current_unit_id: Optional[int | str] | None = Field(None, title="现单位", description="现单位")
    current_unit_name: Optional[str] | None = Field("", title="现单位", description="现单位")
    current_position: str = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] | None = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] | None = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] | None = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] | None = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] | None = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] | None = Field(None, title="现管辖区域区", description="现管辖区域区")
    transfer_out_date: Optional[date] | None = Field(None, title="调出日期", description="调出日期")

    transfer_reason: str = Field("", title="调动原因", description="调动原因")
    remark: str = Field("", title="备注", description="备注")
    teacher_id: Optional[int | str] | None = Field(None, title="教师ID", description="教师ID")
    transfer_type: TransferType = Field("transfer_in", title="调动类型", description="调入或者调出")
    process_instance_id: int | str = Field(0, title="流程ID", description="流程ID")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "original_unit_id", "process_instance_id", "current_unit_id",
                        "transfer_details_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TransferAndBorrowExtraModel(BaseModel):
    original_district_province_name: Optional[str] | None = Field("", title="原行政属地省", description="原行政属地省")
    original_district_city_name: Optional[str] | None = Field("", title="原行政属地市", description="原行政属地市")
    original_district_area_name: Optional[str] | None = Field("", title="原行政属地区", description="原行政属地区")
    # original_region_province_name: Optional[str] = Field("", title="原管辖区域省", description="原管辖区域省")
    # original_region_city_name: Optional[str] = Field("", title="原管辖区域市", description="原管辖区域市")
    # original_region_area_name: Optional[str] = Field("", title="原管辖区域区", description="原管辖区域区")
    current_district_province_name: Optional[str] | None = Field("", title="现行政属地省", description="现行政属地省")
    current_district_city_name: Optional[str] | None = Field("", title="现行政属地市", description="现行政属地市")
    current_district_area_name: Optional[str] | None = Field("", title="现行政属地区", description="现行政属地区")
    # current_region_province_name: Optional[str]| None = Field("", title="现管辖区域省", description="现管辖区域省")
    # current_region_city_name: Optional[str]| None = Field("", title="现管辖区域市", description="现管辖区域市")
    # current_region_area_name: Optional[str]| None = Field("", title="现管辖区域区", description="现管辖区域区")
    original_unit_name: Optional[str] | None = Field("", title="原单位", description="原单位")
    current_unit_name: Optional[str] | None = Field("", title="现单位", description="现单位")


class TransferDetailsGetModel(BaseModel):
    """
    单个教师的所有的调动记录
    """
    original_district_province_name: Optional[str] = Field("", title="原行政属地省", description="原行政属地省")
    original_district_city_name: Optional[str] = Field("", title="原行政属地市", description="原行政属地市")
    original_district_area_name: Optional[str] = Field("", title="原行政属地区", description="原行政属地区")
    original_region_province_name: Optional[str] = Field("", title="原管辖区域省", description="原管辖区域省")
    original_region_city_name: Optional[str] = Field("", title="原管辖区域市", description="原管辖区域市")
    original_region_area_name: Optional[str] = Field("", title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] = Field("", title="原单位", description="原单位")
    current_district_province_name: Optional[str] = Field("", title="现行政属地省", description="现行政属地省")
    current_district_city_name: Optional[str] = Field("", title="现行政属地市", description="现行政属地市")
    current_district_area_name: Optional[str] = Field("", title="现行政属地区", description="现行政属地区")
    current_region_province_name: Optional[str] = Field("", title="现管辖区域省", description="现管辖区域省")
    current_region_city_name: Optional[str] = Field("", title="现管辖区域市", description="现管辖区域市")
    current_region_area_name: Optional[str] = Field("", title="现管辖区域区", description="现管辖区域区")
    current_unit_name: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    start_time: Optional[datetime] | None = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[datetime] | None = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    process_instance_id: int | str = Field(0, title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class WorkflowQueryModel(BaseModel):
    teacher_id: Optional[int | str] = Field(None, title="教师ID", description="教师ID")
    process_code: Optional[str] = Field(None, title="流程code", description="流程code")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


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
    现单位：current_unit_id
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name
    """
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Query("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Query("", title="身份证件号", description="证件号")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别")
    original_district_province_id: Optional[int] = Query(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] = Query(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] = Query(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] = Query(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] = Query(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] = Query(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_id: Optional[int | str] = Query(None, title="原单位", description="原单位")
    current_district_province_id: Optional[int] = Query(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] = Query(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] = Query(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] = Query(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] = Query(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] = Query(None, title="现管辖区域区", description="现管辖区域区")
    current_unit_id: Optional[int | str] = Query(None, title="现单位id", description="现单位id")
    approval_status: Optional[str] = Query("", title="审批状态", description="审批状态")
    start_time_s: Optional[date] = Query(None, title="申请开始时间", description="申请开始时间")
    start_time_e: Optional[date] = Query(None, title="申请结束时间", description="申请结束时间")
    approval_time_s: Optional[date] = Query(None, title="审批开始时间", description="审批开始时间")
    approval_time_e: Optional[date] = Query(None, title="审批结束时间", description="审批结束时间")
    approval_name: Optional[str] = Query("", title="审批人", description="审批人")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["current_unit_id", "original_unit_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


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
    现单位：current_unit_name
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name
    流程实例id：process_instance_id

    """
    transfer_details_id: int | str = Field(0, title="调动主键", description="调动主键")
    teacher_id: int | str = Field(0, title="教师ID", description="教师ID")
    teacher_name: str = Field("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="身份证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_district_province_name: Optional[str] = Field("", title="原行政属地省", description="原行政属地省")
    original_district_city_name: Optional[str] = Field("", title="原行政属地市", description="原行政属地市")
    original_district_area_name: Optional[str] = Field("", title="原行政属地区", description="原行政属地区")
    original_region_province_name: Optional[str] = Field("", title="原管辖区域省", description="原管辖区域省")
    original_region_city_name: Optional[str] = Field("", title="原管辖区域市", description="原管辖区域市")
    original_region_area_name: Optional[str] = Field("", title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] = Field("", title="原单位", description="原单位")
    current_district_province_name: Optional[str] = Field("", title="现行政属地省", description="现行政属地省")
    current_district_city_name: Optional[str] = Field("", title="现行政属地市", description="现行政属地市")
    current_district_area_name: Optional[str] = Field("", title="现行政属地区", description="现行政属地区")
    current_region_province_name: Optional[str] = Field("", title="现管辖区域省", description="现管辖区域省")
    current_region_city_name: Optional[str] = Field("", title="现管辖区域市", description="现管辖区域市")
    current_region_area_name: Optional[str] = Field("", title="现管辖区域区", description="现管辖区域区")
    current_unit_name: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    start_time: Optional[datetime] | None = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[datetime] | None = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    process_instance_id: int | str = Field(0, title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["transfer_details_id", "process_instance_id", "teacher_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


# 借动的模型
class TeacherBorrowModel(BaseModel):
    """

    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    借入日期：borrow_in_date
    现单位：current_unit_id
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
    original_unit_id: Optional[int | str] = Field(None, title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] | None = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] | None = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] | None = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] | None = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] | None = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] | None = Field(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] | None = Field("", title="原单位", description="原单位")
    borrow_in_date: Optional[date] = Field(None, title="借入日期", description="借入日期")

    current_unit_id: Optional[int | str] | None = Field(None, title="现单位", description="现单位")
    current_unit_name: Optional[str] | None = Field("", title="现单位", description="现单位")
    current_position: Optional[str] | None = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] | None = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] | None = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] | None = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] | None = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] | None = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] | None = Field(None, title="现管辖区域区", description="现管辖区域区")
    borrow_out_date: Optional[date] | None = Field(None, title="借出日期", description="借出日期")

    borrow_reason: str = Field("", title="借动原因", description="借动原因")
    remark: str = Field("", title="备注", description="备注")
    teacher_id: Optional[int] | None = Field(None, title="教师ID", description="教师ID")
    borrow_type: BorrowType = Field("borrow_in", title="借动类型", description="借入或者借出")
    process_instance_id: int | str = Field(0, title="流程ID", description="流程ID")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "original_unit_id", "process_instance_id", "current_unit_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


class TeacherBorrowReModel(BaseModel):
    """
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    借入日期：borrow_in_date
    现单位：current_unit_id
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

    original_unit_id: Optional[int | str] = Field(None, title="原单位", description="原单位")
    original_position: str = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] | None = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] | None = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] | None = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] | None = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] | None = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] | None = Field(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] | None = Field("", title="原单位", description="原单位")
    borrow_in_date: Optional[date] = Field(None, title="借入日期", description="借入日期")

    current_unit_id: Optional[int | str] | None = Field(None, title="现单位", description="现单位")
    current_unit_name: Optional[str] | None = Field("", title="现单位", description="现单位")
    current_position: Optional[str] | None = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] | None = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] | None = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] | None = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] | None = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] | None = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] | None = Field(None, title="现管辖区域区", description="现管辖区域区")
    borrow_out_date: Optional[date] | None = Field(None, title="借出日期", description="借出日期")

    borrow_reason: str = Field("", title="借动原因", description="借动原因")
    remark: str = Field("", title="备注", description="备注")
    teacher_id: Optional[int] | None = Field(None, title="教师ID", description="教师ID")
    borrow_type: BorrowType = Field("borrow_in", title="借动类型", description="借入或者借出")
    process_instance_id: int | str = Field(0, title="流程ID", description="流程ID")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_id", "original_unit_id", "process_instance_id", "current_unit_id",
                        "teacher_borrow_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


class TeacherBorrowGetModel(BaseModel):
    """
    单个教师的所有的借动记录
    """
    original_district_province_name: Optional[str] = Field("", title="原行政属地省", description="原行政属地省")
    original_district_city_name: Optional[str] = Field("", title="原行政属地市", description="原行政属地市")
    original_district_area_name: Optional[str] = Field("", title="原行政属地区", description="原行政属地区")
    original_region_province_name: Optional[str] = Field("", title="原管辖区域省", description="原管辖区域省")
    original_region_city_name: Optional[str] = Field("", title="原管辖区域市", description="原管辖区域市")
    original_region_area_name: Optional[str] = Field("", title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] = Field("", title="原单位", description="原单位")
    current_district_province_name: Optional[str] = Field("", title="现行政属地省", description="现行政属地省")
    current_district_city_name: Optional[str] = Field("", title="现行政属地市", description="现行政属地市")
    current_district_area_name: Optional[str] = Field("", title="现行政属地区", description="现行政属地区")
    current_region_province_name: Optional[str] = Field("", title="现管辖区域省", description="现管辖区域省")
    current_region_city_name: Optional[str] = Field("", title="现管辖区域市", description="现管辖区域市")
    current_region_area_name: Optional[str] = Field("", title="现管辖区域区", description="现管辖区域区")
    current_unit_name: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    start_time: Optional[datetime] | None = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[datetime] | None = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    process_instance_id: int | str = Field(0, title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data


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
    现单位：current_unit_id
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name

    """
    teacher_name: Optional[str] = Query("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Query("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Query("", title="身份证件号", description="证件号")
    teacher_gender: Optional[Gender] = Query(None, title="性别", description="性别")
    original_district_province_id: Optional[int] = Query(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] = Query(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] = Query(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] = Query(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] = Query(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] = Query(None, title="原管辖区域区", description="原管辖区域区")
    original_unit_id: Optional[int | str] = Query(None, title="原单位", description="原单位")
    current_district_province_id: Optional[int] = Query(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] = Query(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] = Query(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] = Query(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] = Query(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] = Query(None, title="现管辖区域区", description="现管辖区域区")
    current_unit_id: Optional[int | str] = Query(None, title="现单位id", description="现单位id")
    approval_status: Optional[str] = Query("", title="审批状态", description="审批状态")
    start_time_s: Optional[date] = Query(None, title="申请开始时间", description="申请开始时间")
    start_time_e: Optional[date] = Query(None, title="申请结束时间", description="申请结束时间")
    approval_time_s: Optional[date] = Query(None, title="审批开始时间", description="审批开始时间")
    approval_time_e: Optional[date] = Query(None, title="审批结束时间", description="审批结束时间")
    approval_name: Optional[str] = Query("", title="审批人", description="审批人")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["current_unit_id", "original_unit_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], str):
                data[_change] = int(data[_change])
        return data


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
    现单位：current_unit_name
    审批状态：approval_status
    申请时间：operation_time
    审批时间：approval_time
    申请人：operator_name
    审批人：approval_name
    流程实例id：process_instance_id

    """

    teacher_id: int | str = Field(0, title="教师ID", description="教师ID")
    teacher_name: str = Field("", title="姓名", description="姓名")
    teacher_number: Optional[str] = Field("", title="教职工号", description="教职工号")
    teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="身份证件号", description="证件号")
    teacher_gender: Optional[Gender] = Field(None, title="性别", description="性别")
    original_district_province_name: Optional[str] = Field("", title="原行政属地省", description="原行政属地省")
    original_district_city_name: Optional[str] = Field("", title="原行政属地市", description="原行政属地市")
    original_district_area_name: Optional[str] = Field("", title="原行政属地区", description="原行政属地区")
    original_region_province_name: Optional[str] = Field("", title="原管辖区域省", description="原管辖区域省")
    original_region_city_name: Optional[str] = Field("", title="原管辖区域市", description="原管辖区域市")
    original_region_area_name: Optional[str] = Field("", title="原管辖区域区", description="原管辖区域区")
    original_unit_name: Optional[str] = Field("", title="原单位", description="原单位")
    current_district_province_name: Optional[str] = Field("", title="现行政属地省", description="现行政属地省")
    current_district_city_name: Optional[str] = Field("", title="现行政属地市", description="现行政属地市")
    current_district_area_name: Optional[str] = Field("", title="现行政属地区", description="现行政属地区")
    current_region_province_name: Optional[str] = Field("", title="现管辖区域省", description="现管辖区域省")
    current_region_city_name: Optional[str] = Field("", title="现管辖区域市", description="现管辖区域市")
    current_region_area_name: Optional[str] = Field("", title="现管辖区域区", description="现管辖区域区")
    current_unit_name: Optional[str] = Field("", title="现单位", description="现单位")
    approval_status: Optional[str] = Field("", title="审批状态", description="审批状态")
    start_time: Optional[datetime] | None = Field(None, title="申请时间", description="申请时间")
    approval_time: Optional[datetime] | None = Field(None, title="审批时间", description="审批时间")
    approval_name: Optional[str] = Field("", title="审批人", description="审批人")
    teacher_borrow_id: int | str = Field(0, title="teacher_borrow_id", description="teacher_borrow_id")
    process_instance_id: int | str = Field(0, title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_borrow_id", "process_instance_id", "teacher_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
        return data
