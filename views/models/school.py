from pydantic import BaseModel, Field


class School(BaseModel):
    school_name: str = Field(..., title="学校名称", description="1-20字符",examples=['XX小学'])
    school_no: str = Field(..., title="学校编号", description="学校编号",examples=['SC2032633'])
    school_operation_license_number: str = Field(..., title=" Description",
                                                 description="办学许可证号",examples=['EDU2024012569'])
    block: str = Field(..., title=" Author", description="地域管辖区",examples=['铁西区'])
    borough: str = Field(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区'])
    school_type: str = Field(..., title=" Copyright", description=" 学校类型",examples=['铁西区'])

    school_operation_type: str = Field(..., title=" Copyright", description="办学类型/学校性质",examples=['学前教育'])
    school_operation_type_lv2: str = Field(..., title=" Copyright", description=" 办学类型二级",examples=['铁西区'])
    school_operation_type_lv3: str = Field(..., title=" Copyright", description=" 办学类型三级",examples=['铁西区'])
    school_org_type: str = Field(..., title=" Copyright", description=" 学校办别",examples=['民办'])
    school_level: str = Field(..., title=" Copyright", description=" 学校星级",examples=['5'])
    status: str = Field(..., title=" Copyright", description=" 状态",examples=['正常'])
    school_code: str = Field(..., title=" Copyright", description=" 园所标识码",examples=['SC562369322SG'])
    kg_level: str = Field(..., title=" Copyright", description=" Copyright")
    created_uid: str = Field(..., title=" Copyright", description=" Copyright")
    updated_uid: str = Field(..., title=" Copyright", description=" Copyright")
    created_at: str = Field(..., title=" Copyright", description=" Copyright")
    updated_at: str = Field(..., title=" Copyright", description=" Copyright")
    deleted: str = Field(..., title=" Copyright", description=" Copyright")
    school_short_name: str = Field(..., title=" Copyright", description=" Copyright")
    school_en_name: str = Field(..., title=" Copyright", description=" Copyright")
    create_school_date: str = Field(..., title=" Copyright", description=" Copyright")
    social_credit_code: str = Field(..., title=" Copyright", description=" Copyright")
    founder_type: str = Field(..., title=" Copyright", description=" Copyright")
    founder_name: str = Field(..., title=" Copyright", description=" Copyright")
    founder_code: str = Field(..., title=" Copyright", description=" Copyright")
    urban_rural_nature: str = Field(..., title=" Copyright", description=" Copyright")
    school_org_form: str = Field(..., title=" Copyright", description=" Copyright")
    school_closure_date: str = Field(..., title=" Copyright", description=" Copyright")
    department_unit_number: str = Field(..., title=" Copyright", description=" Copyright")
    sy_zones: str = Field(..., title=" Copyright", description=" Copyright")
    historical_evolution: str = Field(..., title=" Copyright", description=" Copyright")

    class Config:
        schema_extra = {
            "example": {
                "school_name": "xx学校",
                "school_no": "EDU202403256",
                "school_operation_license_number": "A school management system",
                "block": "Lfun technical",
                "borough": "cloud@lfun.cn",
                "school_type": "Copyright © 2024 Lfun technical",
                "school_operation_type":"Copyright © 2024 Lfun technical",
                "school_operation_type_lv2": "Copyright © 2024 Lfun technical",
                "school_operation_type_lv3": "Copyright © 2024 Lfun technical",
                "school_org_type": "Copyright © 2024 Lfun technical",
                "school_level": "Copyright © 2024 Lfun technical",
                "school_nature": "Copyright © 2024Lfun technical",
                "status": "Copyright © 2024 Lfun technical",
                "school_code": "Copyright © 2024 Lfun technical",
                "kg_level": "Copyright © 2024 Lfun technical",
                "created_uid": "Copyright © 2024 Lfun technical",
                "updated_uid": "Copyright © 2024 Lfun technical",
                "created_at": "Copyright © 2024 Lfun technical",
                "updated_at": "Copyright © 2024 Lfun technical",
                "deleted": "Copyright © 2024 Lfun technical",
                "school_short_name": "Copyright © 2024 Lfun technical",
                "school_en_name": "Copyright © 2024 Lfun technical",
                "create_school_date": "Copyright © 2024 Lfun technical",
                "social_credit_code": "Copyright © 2024 Lfun technical",
                "founder_type": "Copyright © 2024 Lfun technical",
                "founder_name": "Copyright © 2024 Lfun technical",
                "founder_code": "Copyright © 2024 Lfun technical",
                "urban_rural_nature": "Copyright © 2024 Lfun technical",
                "school_org_form": "Copyright © 2024 Lfun technical",
                "school_closure_date": "Copyright © 2024 Lfun technical",
                "department_unit_number": "Copyright © 2024 Lfun technical",
                "sy_zones": "Copyright © 2024 Lfun technical",
                "historical_evolution": "Copyright © 2024 Lfun technical"

            }
        }
