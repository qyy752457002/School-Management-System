from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from models.work_flow_define import ProcessType,ProcessCode,ProcessName

class WorkFlowDefineModel(BaseModel):
    """
    流程名称：process_name
    流程code：process_code
    流程描述：process_description
    流程类型：process_type
    借入/借出：is_borrow
    借动是否涉及系统外：is_borrow_external
    是否借入校审批：is_borrow_in_school_approval
    是否借出校审批：is_borrow_out_school_approval
    是否借入区审批：is_borrow_in_area_approval
    是否借出区审批：is_borrow_out_area_approval
    是否借动市审批：is_borrow_city_approval
    调入/调出：is_transfer
    调入/调出发起：is_transfer_external
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
    """
    process_code: str = Field(..., title="流程code", description="流程code")
    process_name: str = Field(..., title="流程名称", description="流程名称")
    process_description: str = Field("", title="流程描述", description="流程描述")
    process_type: ProcessType = Field(..., title="流程类型", description="流程类型")
    is_borrow: Optional[bool] = Field(False, title="借入/借出", description="借入/借出")
    is_borrow_external: Optional[bool] = Field(False, title="借入/借出发起", description="借入/借出发起")
    is_borrow_in_school_approval: Optional[bool] = Field(False, title="是否借入校审批", description="是否借入校审批")
    is_borrow_out_school_approval: Optional[bool] = Field(False, title="是否借出校审批", description="是否借出校审批")
    is_borrow_in_area_approval: Optional[bool] = Field(False, title="是否借入区审批", description="是否借入区审批")
    is_borrow_out_area_approval: Optional[bool] = Field(False, title="是否借出区审批", description="是否借出区审批")
    is_borrow_city_approval: Optional[bool] = Field(False, title="是否借动市审批", description="是否借动市审批")

    is_transfer: Optional[bool] = Field(False, title="调入/调出", description="调入/调出")
    is_transfer_external: Optional[bool] = Field(False, title="调入/调出发起", description="调入/调出发起")
    is_transfer_in_school_approval: Optional[bool] = Field(False, title="是否调入校审批", description="是否调入校审批")
    is_transfer_out_school_approval: Optional[bool] = Field(False, title="是否调出校审批", description="是否调出校审批")
    is_transfer_in_area_approval: Optional[bool] = Field(False, title="是否调入区审批", description="是否调入区审批")
    is_transfer_out_area_approval: Optional[bool] = Field(False, title="是否调出区审批", description="是否调出区审批")
    is_transfer_city_approval: Optional[bool] = Field(False, title="是否调动市审批", description="是否调动市审批")
    is_info_school_approval: Optional[bool] = Field(False, title="是否信息修改校审批", description="是否信息修改校审批")
    is_info_area_approval: Optional[bool] = Field(False, title="是否信息修改区审批", description="是否信息修改区审批")
    is_info_city_approval: Optional[bool] = Field(False, title="是否信息修改市审批", description="是否信息修改市审批")
    is_change_school_approval: Optional[bool] = Field(False, title="是否变动校审批", description="是否变动校审批")
    is_change_area_approval: Optional[bool] = Field(False, title="是否变动区审批", description="是否变动区审批")
    is_change_city_approval: Optional[bool] = Field(False, title="是否变动市审批", description="是否变动市审批")
    is_entry_school_approval: Optional[bool] = Field(False, title="是否入职校审批", description="是否入职校审批")
    is_entry_area_approval: Optional[bool] = Field(False, title="是否入职区审批", description="是否入职区审批")
    is_entry_city_approval: Optional[bool] = Field(False, title="是否入职市审批", description="是否入职市审批")


