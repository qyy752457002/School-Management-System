from pydantic import BaseModel, Field


class School(BaseModel):
    school_name: str = Field(..., title="学校名称", description="1-20字符")
    school_no: str = Field(..., title="学校编号", description="1-20字符")
    school_operation_license_number: str = Field(..., title="Application Description",
                                                 description="Application Description")
    block: str = Field(..., title="Application Author", description="Application Author")
    borough: str = Field(..., title="Application Author Email", description="Application Author Email")
    school_type: str = Field(..., title="Application Copyright", description="Application Copyright")

    school_operation_type: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_operation_type_lv2: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_operation_type_lv3: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_org_type: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_level: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_nature: str = Field(..., title="Application Copyright", description="Application Copyright")
    status: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_code: str = Field(..., title="Application Copyright", description="Application Copyright")
    kg_level: str = Field(..., title="Application Copyright", description="Application Copyright")
    created_uid: str = Field(..., title="Application Copyright", description="Application Copyright")
    updated_uid: str = Field(..., title="Application Copyright", description="Application Copyright")
    created_at: str = Field(..., title="Application Copyright", description="Application Copyright")
    updated_at: str = Field(..., title="Application Copyright", description="Application Copyright")
    deleted: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_short_name: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_en_name: str = Field(..., title="Application Copyright", description="Application Copyright")
    create_school_date: str = Field(..., title="Application Copyright", description="Application Copyright")
    social_credit_code: str = Field(..., title="Application Copyright", description="Application Copyright")
    founder_type: str = Field(..., title="Application Copyright", description="Application Copyright")
    founder_name: str = Field(..., title="Application Copyright", description="Application Copyright")
    founder_code: str = Field(..., title="Application Copyright", description="Application Copyright")
    urban_rural_nature: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_org_form: str = Field(..., title="Application Copyright", description="Application Copyright")
    school_closure_date: str = Field(..., title="Application Copyright", description="Application Copyright")
    department_unit_number: str = Field(..., title="Application Copyright", description="Application Copyright")
    sy_zones: str = Field(..., title="Application Copyright", description="Application Copyright")
    historical_evolution: str = Field(..., title="Application Copyright", description="Application Copyright")

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
