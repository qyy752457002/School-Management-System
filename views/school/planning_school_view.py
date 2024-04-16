

from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchool,PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse


class PlanningSchoolView(BaseView):

    async def get(self,planning_school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  planning_school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),
                  school_id:str= Query(None, description="学校id|根据学校查规划校" ,min_length=1,max_length=20,example='SJD1256526'),

                  ):

        res = PlanningSchool(
            planning_school_name=planning_school_name,
            planning_school_no=  planning_school_no,
            planning_school_operation_license_number=planning_school_no,
            block='',
            borough='',
            planning_school_type='中小学',
            planning_school_operation_type='学前教育',

            planning_school_operation_type_lv2='小学',
            planning_school_operation_type_lv3='附设小学班',
            planning_school_org_type='民办',
            planning_school_level='5',
            status='正常',
            planning_school_code='SC562369322SG',
            kg_level='5',
            created_uid='1',
            updated_uid='21',
            created_at='2021-10-10 00:00:00',
            updated_at='2021-10-10 00:00:00',
            deleted='0',
            planning_school_short_name='MXXX',
            planning_school_en_name='MinxingPrimarySCHOOL',
            create_planning_school_date='2021-10-10 00:00:00',
            social_credit_code='XH423423876867',
            founder_type='地方',
            founder_name='上海教育局',
            founder_code='SC562369322SG',
            urban_rural_nature='城镇',
            planning_school_org_form='教学点',
            planning_school_closure_date='',
            department_unit_number='SC562369322SG',
            sy_zones='铁西区',
            sy_zones_pro='沈阳',
            primary_planning_school_system='6',
            primary_planning_school_entry_age='6',
            junior_middle_planning_school_system='3',
            junior_middle_planning_school_entry_age='12',
            senior_middle_planning_school_system='3',
            historical_evolution='xxxxxxxxxxxxxxxxxxxx',



        )
        return  res

    async def post(self,planning_school:PlanningSchool):
        print(planning_school)
        return  planning_school
    # 修改 关键信息
    async def put(self,planning_school_id:str= Query(None, title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),
                  planning_school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
                  borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
                  block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
                  planning_school_name: str = Query(..., title="学校名称", description="园所名称",examples=['XX小学']),
                  planning_school_type: str = Query(..., title="", description=" 学校类型",examples=['中小学']),
                  planning_school_operation_type: str = Query(..., title="", description="办学类型/学校性质",examples=['学前教育']),
                  planning_school_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
                  planning_school_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
                  planning_school_org_type: str = Query(..., title="", description=" 学校办别",examples=['民办']),
                  planning_school_level: str = Query(..., title="", description=" 学校星级",examples=['5'])


                  ):
        # print(planning_school)
        return  [planning_school_no,borough,block ]
    # 删除
    async def delete(self,planning_school:PlanningSchool):
        print(planning_school)
        return  planning_school
    # 修改 变更 基本信息
    async def patch(self, planning_school_baseinfo:PlanningSchoolBaseInfo, planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),   ):
        # print(planning_school)
        return   planning_school_baseinfo




    async def page(self,
                   page_request= Depends(PageRequest),
                   # planning_school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  # planning_school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),




                  ):
        print(page_request)
        items=[]

        res = PlanningSchool(
            planning_school_name='',
            planning_school_no=  'planning_school_no',
            planning_school_operation_license_number='planning_school_no',
            block='',
            borough='',
            planning_school_type='中小学',
            planning_school_operation_type='学前教育',

            planning_school_operation_type_lv2='小学',
            planning_school_operation_type_lv3='附设小学班',
            planning_school_org_type='民办',
            planning_school_level='5',
            status='正常',
            planning_school_code='SC562369322SG',
            kg_level='5',
            created_uid='1',
            updated_uid='21',
            created_at='2021-10-10 00:00:00',
            updated_at='2021-10-10 00:00:00',
            deleted='0',
            planning_school_short_name='MXXX',
            planning_school_en_name='MinxingPrimarySCHOOL',
            create_planning_school_date='2021-10-10 00:00:00',
            social_credit_code='XH423423876867',
            founder_type='地方',
            founder_name='上海教育局',
            founder_code='SC562369322SG',
            urban_rural_nature='城镇',
            planning_school_org_form='教学点',
            planning_school_closure_date='',
            department_unit_number='SC562369322SG',
            sy_zones='铁西区',
            sy_zones_pro='沈阳',
            primary_planning_school_system='6',
            primary_planning_school_entry_age='6',
            junior_middle_planning_school_system='3',
            junior_middle_planning_school_entry_age='12',
            senior_middle_planning_school_system='3',
            historical_evolution='xxxxxxxxxxxxxxxxxxxx',



        )
        for i in range(0,page_request.per_page):
            items.append(res)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
    # 开办
    async def open(self,planning_school:PlanningSchool):
        print(planning_school)
        return  planning_school

    # 关闭
    async def close(self,planning_school:PlanningSchool):
        print(planning_school)
        return  planning_school

    # 导入
    async def importing(self,planning_school:PlanningSchool):
        print(planning_school)
        return  planning_school






























