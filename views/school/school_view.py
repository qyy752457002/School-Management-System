from mini_framework.web.views import BaseView

from views.models.school import School


class SchoolView(BaseView):
    async def get(self):
        return School(
            school_name= "School Management System",
            school_no= "1.0.0",
            school_operation_license_number= "A school management system",
            block= "Lfun technical",
            borough= "cloud@lfun.cn",
            school_type= "Copyright ? 2024 Lfun technical",
            school_operation_type="Copyright ? 2024 Lfun technical",
            school_operation_type_lv2= "Copyright ? 2024 Lfun technical",
            school_operation_type_lv3= "Copyright ? 2024 Lfun technical",
            school_org_type= "Copyright ? 2024 Lfun technical",
            school_level= "Copyright ? 2024 Lfun technical",
            school_nature= "Copyright ? 2024Lfun technical",
            status= "Copyright ? 2024 Lfun technical",
            school_code= "Copyright ? 2024 Lfun technical",
            kg_level= "Copyright ? 2024 Lfun technical",
            created_uid= "Copyright ? 2024 Lfun technical",
            updated_uid= "Copyright ? 2024 Lfun technical",
            created_at= "Copyright ? 2024 Lfun technical",
            updated_at= "Copyright ? 2024 Lfun technical",
            deleted= "Copyright ? 2024 Lfun technical",
            school_short_name= "Copyright ? 2024 Lfun technical",
            school_en_name= "Copyright ? 2024 Lfun technical",
            create_school_date= "Copyright ? 2024 Lfun technical",
            social_credit_code= "Copyright ? 2024 Lfun technical",
            founder_type= "Copyright ? 2024 Lfun technical",
            founder_name= "Copyright ? 2024 Lfun technical",
            founder_code= "Copyright ? 2024 Lfun technical",
            urban_rural_nature= "Copyright ? 2024 Lfun technical",
            school_org_form= "Copyright ? 2024 Lfun technical",
            school_closure_date= "Copyright ? 2024 Lfun technical",
            department_unit_number= "Copyright ? 2024 Lfun technical",
            sy_zones= "Copyright ? 2024 Lfun technical",
            historical_evolution= "Copyright ? 2024 Lfun technical",

        )
    async def post(self):
        return School(
            name="School Management Systemxxxxx", version="1.0.0",
            description="A school management system", author="Lfun technical",
            author_email="cloud@lfun.cn", copyright="Copyright © 2024 Lfun technical"
        )
