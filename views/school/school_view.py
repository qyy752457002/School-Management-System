

from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse



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

    # 修改 关键信息
    async def put(self,school_id:str= Query(None, title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),
                  school_no:str= Query(None, title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
                  borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
                  block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
                  school_name: str = Query(..., title="学校名称", description="园所名称",examples=['XX小学']),
                  school_type: str = Query(..., title="", description=" 学校类型",examples=['中小学']),
                  school_operation_type: str = Query(..., title="", description="办学类型/学校性质",examples=['学前教育']),
                  school_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
                  school_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
                  school_org_type: str = Query(..., title="", description=" 学校办别",examples=['民办']),
                  school_level: str = Query(..., title="", description=" 学校星级",examples=['5'])


                  ):
        # print(school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return  {school_no,borough,block }
    # 删除
    async def delete(self, school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),):
        print(school_id)
        return  school_id
    # 修改 变更 基本信息
    async def patch_baseinfo(self, school_baseinfo:PlanningSchoolBaseInfo, school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),   ):
        # print(school)
        return   school_baseinfo




    async def page(self,
                   page_request= Depends(PageRequest),
                   # school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                   # school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(School(
                school_name='xxxxxxxxxxxxxxxxxxxx',
                school_no='SC562369322SG',
                school_operation_license_number='EDU2024012569',
                block='铁西区',
                borough='铁西区',
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

            ))


        tt= {
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
            "historical_evolution": "Copyright © 2024 Lfun technical",
            "sy_zones_pro": "Copyright © 2024 Lfun technical",
            "primary_school_system": "Copyright © 2024 Lfun technical",
            "primary_school_entry_age": "Copyright © 2024 Lfun technical",
            "junior_middle_school_system": "Copyright © 2024 Lfun technical",
            "junior_middle_school_entry_age": "Copyright © 2024 Lfun technical",
            "senior_middle_school_system": "Copyright © 2024 Lfun technical"

        }

        #
        # for i in range(0,page_request.per_page):
        #     items.append(**tt)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
    # 开办
    async def patch_open(self,school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(school)
        return  school_id

    # 关闭
    async def patch_close(self,school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(school)
        return  school_id

    # 导入 todo 任务队列的
    async def importing(self,school:School):
        print(school)
        return  school
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
