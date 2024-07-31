from pydantic import BaseModel, Field, model_validator
from datetime import date, datetime
from fastapi import Query
from enum import Enum
from typing import Optional, List


class WorkFlowInstanceStatus(str, Enum):
    """
    进行中：pending
    已撤回：revoked
    已同意：approved
    已拒绝：rejected
    """
    REVOKED = "revoked"
    PENDING = "pending"
    PROGRESSING = "progressing"
    APPROVED = "approved"
    REJECTED = "rejected"
    TQUERY = "t_query"
    TLAUNCH = "t_launch"
    TAPPROVAL = "t_approval"


    @classmethod
    def to_list(cls):
        return [cls.REVOKED, cls.PENDING, cls.PROGRESSING, cls.APPROVED, cls.REJECTED, cls.TQUERY, ]


class WorkFlowInstanceCreateModel(BaseModel):
    """
    流程定义id：process_code
    申请人id：applicant_id
    开始时间：start_time
    结束时间：end_time
    流程状态：process_status
    说明：description
    """

    process_code: str = Field(..., title="流程定义id", description="流程定义id")
    applicant_name: str = Field(..., title="申请人姓名", description="申请人姓名")
    approval_name: Optional[str] = Field(None, title="审批人姓名", description="审批人姓名")
    start_time: datetime = Field(datetime.now(), title="开始时间", description="开始时间")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")
    end_time: Optional[datetime] = Field(None, title="结束时间", description="结束时间")
    process_status: Optional[WorkFlowInstanceStatus] = Field("pending", title="流程状态", description="流程状态")
    reason: str = Field("", title="说明", description="说明")
    # 老师入职和关键信息变更相关
    teacher_id: Optional[int | str] = Field(None, title="教师ID", description="教师ID")
    teacher_name: Optional[str] = Field("", title="教师姓名", description="教师姓名")
    teacher_gender: Optional[str] = Field("", title="教师性别", description="教师性别")
    teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: Optional[date] = Field(None, title="出生日期", description="出生日期")
    teacher_employer: Optional[int | str] = Field(None, title="任职单位", description="任职单位")
    teacher_main_status: Optional[str] = Field("unemployed", title="主状态", description="主状态")
    teacher_sub_status: Optional[str] = Field("submitted", title="子状态", description="子状态")
    highest_education: Optional[str] = Field("", title="最高学历", description="最高学历")
    employment_form: Optional[str] = Field("", title="用工形式", description="用工形式")

    identity: Optional[str] = Field("", title="身份", description="身份")
    mobile: Optional[str] = Field("", title="手机号", description="手机号")
    enter_school_time: Optional[date] = Field(None, title="入校时间", description="入校时间")
    in_post: Optional[bool] = Field(False, title="是否在编", description="是否在编")
    # 老师调动和借动相关
    original_unit_id: Optional[int | str] = Field(None, title="原单位", description="原单位")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] = Field(None, title="原管辖区域区", description="原管辖区域区")
    transfer_in_date: Optional[date] = Field(None, title="调入日期", description="调入日期")
    borrow_in_date: Optional[date] = Field(None, title="借入日期", description="借入日期")
    current_unit_id: Optional[int | str] = Field(None, title="现单位", description="现单位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] = Field(None, title="现管辖区域区", description="现管辖区域区")
    borrow_out_date: Optional[date] = Field(None, title="借出日期", description="借出日期")
    transfer_out_date: Optional[date] = Field(None, title="调出日期", description="调出日期")
    json_data: Optional[str] = Field("", title="json数据", description="json数据")
    transfer_type: Optional[str] = Field("", title="调动类型", description="调动类型")
    borrow_type: Optional[str] = Field("", title="借动类型", description="借动类型")
    student_name: Optional[str] = Field("", title="", description="")
    school_name: Optional[str] = Field("", title="", description="")
    student_gender: Optional[str] = Field("", title="", description="")
    edu_number: Optional[str] = Field("", title="", description="")
    apply_user: Optional[str] = Field("", title="", description="")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_id", "teacher_base_id", "original_unit_id", "current_unit_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class WorkFlowInstanceModel(WorkFlowInstanceCreateModel):
    process_instance_id: int|str = Field(..., title="流程实例id", description="流程实例id")

    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_id", "teacher_base_id", "original_unit_id", "current_unit_id",
                        "process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class WorkFlowInstanceQueryModel(BaseModel):
    """
    流程定义id：process_code
    申请人id：applicant_id
    开始时间：start_time
    结束时间：end_time
    流程状态：process_status
    说明：description
    """

    process_code: Optional[str] = Query(None, title="流程定义id", description="流程定义id")
    applicant_name: Optional[str] = Query(None, title="申请人姓名", description="申请人姓名")
    start_time: Optional[datetime] = Query(None, title="开始时间", description="开始时间")
    approval_time: Optional[datetime] = Query(None, title="审批时间", description="审批时间")
    end_time: Optional[datetime] = Query(None, title="结束时间", description="结束时间")
    process_status: Optional[WorkFlowInstanceStatus] = Query(None, title="流程状态", description="流程状态")
    reason: str = Query("", title="说明", description="说明")
    # 老师入职和关键信息变更相关
    teacher_id: Optional[int] = Query(None, title="教师ID", description="教师ID")
    teacher_name: Optional[str] = Query("", title="教师姓名", description="教师姓名")
    teacher_gender: Optional[str] = Query("", title="教师性别", description="教师性别")
    teacher_id_type: Optional[str] = Query("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Query("", title="身份证件号", description="证件号")
    teacher_date_of_birth: Optional[date] = Query(None, title="出生日期", description="出生日期")
    teacher_employer: Optional[int|str] = Query(None, title="任职单位", description="任职单位")
    teacher_main_status: Optional[str] = Query("", title="主状态", description="主状态")
    teacher_sub_status: Optional[str] = Query("", title="子状态", description="子状态")
    highest_education: Optional[str] = Field("", title="最高学历", description="最高学历")
    employment_form: Optional[str] = Field("", title="用工形式", description="用工形式")
    identity: Optional[str] = Query("", title="身份", description="身份")
    mobile: Optional[str] = Query("", title="手机号", description="手机号")
    enter_school_time: Optional[date] = Field(None, title="入校时间", description="入校时间")
    in_post: Optional[bool] = Field(False, title="是否在编", description="是否在编")

    # 老师调动和借动相关
    original_unit_id: Optional[int] = Query(None, title="原单位", description="原单位")
    original_position: Optional[str] = Query("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] = Query(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] = Query(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] = Query(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] = Query(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] = Query(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] = Query(None, title="原管辖区域区", description="原管辖区域区")
    transfer_in_date: Optional[date] = Query(None, title="调入日期", description="调入日期")
    borrow_in_date: Optional[date] = Query(None, title="借入日期", description="借入日期")
    current_unit_id: Optional[int] = Query(None, title="现单位", description="现单位")
    current_position: Optional[str] = Query("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] = Query(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] = Query(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] = Query(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] = Query(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] = Query(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] = Query(None, title="现管辖区域区", description="现管辖区域区")
    borrow_out_date: Optional[date] = Query(None, title="借出日期", description="借出日期")
    transfer_out_date: Optional[date] = Query(None, title="调出日期", description="调出日期")
    json_data: Optional[str] = Query("", title="json数据", description="json数据")
    student_name: Optional[str] = Query("", title="", description="")
    school_name: Optional[str] = Query("", title="", description="")
    student_gender: Optional[str] = Query("", title="", description="")
    edu_number: Optional[str] = Query("", title="", description="")
    apply_user: Optional[str] = Query("", title="", description="")
    planning_school_code: Optional[str] = Query("", title="", description="")
    planning_school_name: Optional[str] = Query("", title="", description="")
    # founder_type_lv3: Optional[str|None] = Query("", title="", description="")
    founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级", )
    block: Optional[str] = Query("", title="", description="")
    borough: Optional[str] = Query("", title="", description="")
    planning_school_level: Optional[str] = Query("", title="", description="")
    school_no: Optional[str] = Query("", title="", description="")
    school_level: Optional[str] = Query("", title="", description="")
    social_credit_code: Optional[str] = Query("", title="", description="")
    institution_name: Optional[str] = Query("", title="", description="")
    @model_validator(mode='before')
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["teacher_employer", "teacher_id", "teacher_base_id", "original_unit_id", "current_unit_id",
                        "process_instance_id"]
        for _change in _change_list:
            if _change in data and isinstance(data[_change], int):
                data[_change] = str(data[_change])
            else:
                pass
        return data


class WorkFlowInstanceQueryReModel(BaseModel):
    process_instance_id: int = Field(..., title="流程实例id", description="流程实例id")
    process_code: str = Field(None, title="流程定义id", description="流程定义id")
    applicant_name: Optional[str] = Field(None, title="申请人姓名", description="申请人姓名")
    start_time: Optional[datetime] = Field(None, title="开始时间", description="开始时间")
    approval_time: Optional[datetime] = Field(None, title="审批时间", description="审批时间")
    end_time: Optional[datetime] = Field(None, title="结束时间", description="结束时间")
    process_status: Optional[WorkFlowInstanceStatus] = Field(None, title="流程状态", description="流程状态")
    reason: str = Field("", title="说明", description="说明")
    # 老师入职和关键信息变更相关
    teacher_id: Optional[int] = Field(None, title="教师ID", description="教师ID")
    teacher_name: Optional[str] = Field("", title="教师姓名", description="教师姓名")
    teacher_gender: Optional[str] = Field("", title="教师性别", description="教师性别")
    teacher_id_type: Optional[str] = Field("", title="身份证件类型", description="证件类型")
    teacher_id_number: Optional[str] = Field("", title="身份证件号", description="证件号")
    teacher_date_of_birth: Optional[date] = Field(None, title="出生日期", description="出生日期")
    teacher_employer: Optional[int] = Field(None, title="任职单位", description="任职单位")
    teacher_main_status: Optional[str] = Field("", title="主状态", description="主状态")
    teacher_sub_status: Optional[str] = Field("", title="子状态", description="子状态")
    highest_education: Optional[str] = Field("", title="最高学历", description="最高学历")
    employment_form: Optional[str] = Field("", title="用工形式", description="用工形式")
    identity: Optional[str] = Field("", title="身份", description="身份")
    mobile: Optional[str] = Field("", title="手机号", description="手机号")
    enter_school_time: Optional[date] = Field(None, title="入校时间", description="入校时间")
    in_post: Optional[bool] = Field(False, title="是否在编", description="是否在编")

    # 老师调动和借动相关
    original_unit_id: Optional[int] = Field(None, title="原单位", description="原单位")
    original_position: Optional[str] = Field("", title="原岗位", description="原岗位")
    original_district_province_id: Optional[int] = Field(None, title="原行政属地省", description="原行政属地省")
    original_district_city_id: Optional[int] = Field(None, title="原行政属地市", description="原行政属地市")
    original_district_area_id: Optional[int] = Field(None, title="原行政属地区", description="原行政属地区")
    original_region_province_id: Optional[int] = Field(None, title="原管辖区域省", description="原管辖区域省")
    original_region_city_id: Optional[int] = Field(None, title="原管辖区域市", description="原管辖区域市")
    original_region_area_id: Optional[int] = Field(None, title="原管辖区域区", description="原管辖区域区")
    transfer_in_date: Optional[date] = Field(None, title="调入日期", description="调入日期")
    borrow_in_date: Optional[date] = Field(None, title="借入日期", description="借入日期")
    current_unit_id: Optional[int] = Field(None, title="现单位", description="现单位")
    current_position: Optional[str] = Field("", title="现岗位", description="现岗位")
    current_district_province_id: Optional[int] = Field(None, title="现行政属地省", description="现行政属地省")
    current_district_city_id: Optional[int] = Field(None, title="现行政属地市", description="现行政属地市")
    current_district_area_id: Optional[int] = Field(None, title="现行政属地区", description="现行政属地区")
    current_region_province_id: Optional[int] = Field(None, title="现管辖区域省", description="现管辖区域省")
    current_region_city_id: Optional[int] = Field(None, title="现管辖区域市", description="现管辖区域市")
    current_region_area_id: Optional[int] = Field(None, title="现管辖区域区", description="现管辖区域区")
    borrow_out_date: Optional[date] = Field(None, title="借出日期", description="借出日期")
    transfer_out_date: Optional[date] = Field(None, title="调出日期", description="调出日期")
    json_data: Optional[str] = Field("", title="json数据", description="json数据")

    student_name: Optional[str] = Field("", title="", description="")
    school_name: Optional[str] = Field("", title="", description="")
    student_gender: Optional[str] = Field("", title="", description="")
    edu_number: Optional[str] = Field("", title="", description="")
    apply_user: Optional[str] = Field("", title="", description="")
    planning_school_code: Optional[str] = Field("", title="", description="")
    planning_school_name: Optional[str] = Field("", title="", description="")
    founder_type_lv3: Optional[str | None] = Field("", title="", description="")
    block: Optional[str] = Field("", title="", description="")
    borough: Optional[str] = Field("", title="", description="")
    planning_school_level: Optional[str] = Field("", title="", description="")
    school_no: Optional[str] = Field("", title="", description="")
    school_level: Optional[str] = Field("", title="", description="")
    social_credit_code: Optional[str] = Field("", title="", description="")
    institution_name: Optional[str] = Field("", title="", description="")
