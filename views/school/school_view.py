

from mini_framework.web.views import BaseView

from views.models.school import School
# from fastapi import Field
from fastapi import Query


class SchoolView(BaseView):
    async def get(self,school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),
                  ):
        res = School(
            school_name=school_name,
            school_no=  school_no,
            school_operation_license_number=school_no,
            block='',
            borough='',
            school_type='中小学',
            school_operation_type='学前教育',

            school_operation_type_lv2='小学',
            school_operation_type_lv3='附设小学班',
            school_org_type='民办',
            school_level='5',
            status='正常',
            school_code='SC562369322SG',
            kg_level='5',
            created_uid='1',
            updated_uid='21',
            created_at='2021-10-10 00:00:00',
            updated_at='2021-10-10 00:00:00',
            deleted='0',
            school_short_name='MXXX',
            school_en_name='MinxingPrimarySCHOOL',
            create_school_date='2021-10-10 00:00:00',
            social_credit_code='XH423423876867',
            founder_type='地方',
            founder_name='上海教育局',
            founder_code='SC562369322SG',
            urban_rural_nature='城镇',
            school_org_form='教学点',
            school_closure_date='',
            department_unit_number='SC562369322SG',
            sy_zones='铁西区',
            sy_zones_pro='沈阳',
            primary_school_system='6',
            primary_school_entry_age='6',
            junior_middle_school_system='3',
            junior_middle_school_entry_age='12',
            senior_middle_school_system='3',
            historical_evolution='xxxxxxxxxxxxxxxxxxxx',



        )
        return  res

    async def post(self,school:School):
        print(school)
        return  school
