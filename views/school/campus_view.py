

from mini_framework.web.views import BaseView

from views.models.campus import Campus, CampusBaseInfo
# from fastapi import Field

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse



class CampusView(BaseView):
    async def get(self,campus_no:str= Query(None, title="", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                  campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),
                  ):
        res = Campus(
            campus_name=campus_name,
            campus_no=  campus_no,
            campus_operation_license_number=campus_no,
            block='',
            borough='',
            campus_type='中小学',
            campus_operation_type='学前教育',

            campus_operation_type_lv2='小学',
            campus_operation_type_lv3='附设小学班',
            campus_org_type='民办',
            campus_level='5',
            status='正常',
            campus_code='SC562369322SG',
            kg_level='5',
            created_uid='1',
            updated_uid='21',
            created_at='2021-10-10 00:00:00',
            updated_at='2021-10-10 00:00:00',
            deleted='0',
            campus_short_name='MXXX',
            campus_en_name='MinxingPrimarySCHOOL',
            create_campus_date='2021-10-10 00:00:00',
            social_credit_code='XH423423876867',
            founder_type='地方',
            founder_name='上海教育局',
            founder_code='SC562369322SG',
            urban_rural_nature='城镇',
            campus_org_form='教学点',
            campus_closure_date='',
            department_unit_number='SC562369322SG',
            sy_zones='铁西区',
            sy_zones_pro='沈阳',
            primary_campus_system='6',
            primary_campus_entry_age='6',
            junior_middle_campus_system='3',
            junior_middle_campus_entry_age='12',
            senior_middle_campus_system='3',
            historical_evolution='xxxxxxxxxxxxxxxxxxxx',
            location_city='',
            location_district='',




        )
        return  res

    async def post(self,campus:Campus):
        print(campus)
        return  campus

    # 修改 关键信息
    async def put(self,campus_id:str= Query(None, title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='SC2032633'),
                  campus_no:str= Query(None, title="校区编号", description="校区编号/园所代码",min_length=1,max_length=20,example='SC2032633'),
                  borough:str=Query(..., title=" Author Email", description=" 行政管辖区",examples=['铁西区']),
                  block: str = Query(..., title=" Author", description="地域管辖区",examples=['铁西区']),
                  campus_name: str = Query(..., title="校区名称", description="园所名称",examples=['XX小学']),
                  campus_type: str = Query(..., title="", description=" 校区类型",examples=['中小学']),
                  campus_operation_type: str = Query(..., title="", description="办学类型/校区性质",examples=['学前教育']),
                  campus_operation_type_lv2: str = Query(..., title="", description=" 办学类型二级",examples=['小学']),
                  campus_operation_type_lv3: str = Query(..., title="", description=" 办学类型三级",examples=['附设小学班']),
                  campus_org_type: str = Query(..., title="", description=" 校区办别",examples=['民办']),
                  campus_level: str = Query(..., title="", description=" 校区星级",examples=['5'])


                  ):
        # print(campus)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return  {campus_no,borough,block }
    # 删除
    async def delete(self, campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='SC2032633'),):
        print(campus_id)
        return  campus_id
    # 修改 变更 基本信息
    async def patch_baseinfo(self, campus_baseinfo:CampusBaseInfo, campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='SC2032633'),   ):
        # print(campus)
        return   campus_baseinfo




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(Campus(
                campus_name='xxxxxxxxxxxxxxxxxxxx',
                campus_no='SC562369322SG',
                campus_operation_license_number='EDU2024012569',
                block='铁西区',
                borough='铁西区',
                campus_type='中小学',
                campus_operation_type='学前教育',
                campus_operation_type_lv2='小学',
               campus_operation_type_lv3='附设小学班',
                campus_org_type='民办',
                campus_level='5',
                status='正常',
                campus_code='SC562369322SG',
                kg_level='5',
                created_uid='1',
                updated_uid='21',
                created_at='2021-10-10 00:00:00',
                updated_at='2021-10-10 00:00:00',
                deleted='0',
                campus_short_name='MXXX',
                campus_en_name='MinxingPrimarySCHOOL',
                create_campus_date='2021-10-10 00:00:00',
                social_credit_code='XH423423876867',
                founder_type='地方',
                founder_name='上海教育局',
                founder_code='SC562369322SG',
                urban_rural_nature='城镇',
                campus_org_form='教学点',
                campus_closure_date='',
               department_unit_number='SC562369322SG',
                sy_zones='铁西区',
                sy_zones_pro='沈阳',
                primary_campus_system='6',
                primary_campus_entry_age='6',
                junior_middle_campus_system='3',
                junior_middle_campus_entry_age='12',
                senior_middle_campus_system='3',
                historical_evolution='xxxxxxxxxxxxxxxxxxxx',
                location_city='',
                location_district='',

            ))


        tt= {
            "campus_name": "xx校区",
            "campus_no": "EDU202403256",
            "campus_operation_license_number": "A campus management system",
            "block": "Lfun technical",
            "borough": "cloud@lfun.cn",
            "campus_type": "Copyright © 2024 Lfun technical",
            "campus_operation_type":"Copyright © 2024 Lfun technical",
            "campus_operation_type_lv2": "Copyright © 2024 Lfun technical",
            "campus_operation_type_lv3": "Copyright © 2024 Lfun technical",
            "campus_org_type": "Copyright © 2024 Lfun technical",
            "campus_level": "Copyright © 2024 Lfun technical",
            "campus_nature": "Copyright © 2024Lfun technical",
            "status": "Copyright © 2024 Lfun technical",
            "campus_code": "Copyright © 2024 Lfun technical",
            "kg_level": "Copyright © 2024 Lfun technical",
            "created_uid": "Copyright © 2024 Lfun technical",
            "updated_uid": "Copyright © 2024 Lfun technical",
            "created_at": "Copyright © 2024 Lfun technical",
            "updated_at": "Copyright © 2024 Lfun technical",
            "deleted": "Copyright © 2024 Lfun technical",
            "campus_short_name": "Copyright © 2024 Lfun technical",
            "campus_en_name": "Copyright © 2024 Lfun technical",
            "create_campus_date": "Copyright © 2024 Lfun technical",
            "social_credit_code": "Copyright © 2024 Lfun technical",
            "founder_type": "Copyright © 2024 Lfun technical",
            "founder_name": "Copyright © 2024 Lfun technical",
            "founder_code": "Copyright © 2024 Lfun technical",
            "urban_rural_nature": "Copyright © 2024 Lfun technical",
            "campus_org_form": "Copyright © 2024 Lfun technical",
            "campus_closure_date": "Copyright © 2024 Lfun technical",
            "department_unit_number": "Copyright © 2024 Lfun technical",
            "sy_zones": "Copyright © 2024 Lfun technical",
            "historical_evolution": "Copyright © 2024 Lfun technical",
            "sy_zones_pro": "Copyright © 2024 Lfun technical",
            "primary_campus_system": "Copyright © 2024 Lfun technical",
            "primary_campus_entry_age": "Copyright © 2024 Lfun technical",
            "junior_middle_campus_system": "Copyright © 2024 Lfun technical",
            "junior_middle_campus_entry_age": "Copyright © 2024 Lfun technical",
            "senior_middle_campus_system": "Copyright © 2024 Lfun technical"

        }

        #
        # for i in range(0,page_request.per_page):
        #     items.append(**tt)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
    # 开办
    async def patch_open(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(campus)
        return  campus_id

    # 关闭
    async def patch_close(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(campus)
        return  campus_id

    # 导入 todo 任务队列的
    async def importing(self,campus:Campus):
        print(campus)
        return  campus
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
