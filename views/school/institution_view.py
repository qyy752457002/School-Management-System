from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchool,PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.institutions import Institutions
from rules.institution_rule import InstitutionRule

# 当前工具包里支持get  patch前缀的 方法的自定义使用
class InstitutionView(BaseView):
    def __init__(self):
        super().__init__()
        self.institution_rule = get_injector(InstitutionRule)



    async def page(self,
                   page_request= Depends(PageRequest),
                   # planning_school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  # planning_school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),




                  ):
        print(page_request)
        items=[]
        res = await self.institution_rule.query_institution_with_page(page_request,)
        return res

        #
        # res = Institutions(institution_name='XXX',institution_en_name='XXX',institution_category='XXX',institution_type='XXX',fax_number='XXX',email='XXX',contact_number='XXX',area_code='XXX',institution_code='XXX',create_date='XXX',leg_repr_name='XXX',party_leader_name='XXX',party_leader_position='XXX',adm_leader_name='XXX',adm_leader_position='XXX',department_unit_number='XXX',sy_zones='XXX',social_credit_code='XXX',postal_code='XXX',detailed_address='XXX',related_license_upload='XXX',long='XXX',lat='XXX', urban_rural_nature='XXX',location_economic_attribute='XXX',leg_repr_certificatenumber='XXX',is_entity='XXX',website_uRL='XXX',status='XXX',membership_no='XXX',membership_category='XXX',)
        # for i in range(0,page_request.per_page):
        #     items.append(res)
        #
        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)


