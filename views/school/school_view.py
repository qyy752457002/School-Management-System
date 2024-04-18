from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

# from views.models.school import PlanningSchoolBaseInfo
from views.models.school import School, SchoolBaseInfo,SchoolKeyInfo
# from fastapi import Field

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse


# from rules.school_eduinfo_rule import PlanningSchoolEduinfoRule
from rules.school_rule import SchoolRule


class SchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.school_rule = get_injector(SchoolRule)
    async def get(self,school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),
                  school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),
                  ):

        school = await self.school_rule.get_school_by_id(school_id)
        return school
        # res = School(
        #     school_name=school_name,
        #     school_no=  school_no,
        #     school_operation_license_number=school_no,
        #     block='',
        #     borough='',
        #     school_type='中小学',
        #     school_operation_type='学前教育',
        #
        #     school_operation_type_lv2='小学',
        #     school_operation_type_lv3='附设小学班',
        #     school_org_type='民办',
        #     school_level='5',
        #     status='正常',
        #     school_code='SC562369322SG',
        #     kg_level='5',
        #     created_uid='1',
        #     updated_uid='21',
        #     created_at='2021-10-10 00:00:00',
        #     updated_at='2021-10-10 00:00:00',
        #     deleted='0',
        #     school_short_name='MXXX',
        #     school_en_name='MinxingPrimarySCHOOL',
        #     create_school_date='2021-10-10 00:00:00',
        #     social_credit_code='XH423423876867',
        #     founder_type='地方',
        #     founder_name='上海教育局',
        #     founder_code='SC562369322SG',
        #     urban_rural_nature='城镇',
        #     school_org_form='教学点',
        #     school_closure_date='',
        #     department_unit_number='SC562369322SG',
        #     sy_zones='铁西区',
        #     sy_zones_pro='沈阳',
        #     primary_school_system='6',
        #     primary_school_entry_age='6',
        #     junior_middle_school_system='3',
        #     junior_middle_school_entry_age='12',
        #     senior_middle_school_system='3',
        #     historical_evolution='xxxxxxxxxxxxxxxxxxxx',
        #
        #
        #
        # )
        # return  res

    async def post(self,school:School):
        res = await self.school_rule.add_school(school)
        print(res)


        return res
        # return  school

    # 修改 关键信息
    async def put(self,
                  school: SchoolKeyInfo,


                  ):
        # print(school)
        res = await self.school_rule.update_school(school)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res

        # return  {school_no,borough,block }
    # 删除
    async def delete(self, school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),):
        print(school_id)
        res = await self.school_rule.softdelete_school(school_id)

        return res
        # return  school_id
    # 修改 变更 基本信息
    async def patch_baseinfo(self, school_baseinfo:SchoolBaseInfo, school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),   ):
        # print(school)
        res = await self.school_rule.update_school(school_baseinfo,2)

        return res
        # return   school_baseinfo




    async def page(self,
                   page_request= Depends(PageRequest),


                   # school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
                   #                                 max_length=20, example='SC2032633'),
                   # school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                   #                                   example='XX小学'),
                   school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                   school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),
                   ):
        print(page_request)
        items=[]

        paging_result = await self.school_rule.query_school_with_page(page_request,
                                                                                        school_name, None,
                                                                                        school_no, )
        return paging_result


        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)
    # 开办
    async def patch_open(self,school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(school)
        res = await self.school_rule.update_school_status(school_id,1)

        return res
        # return  school_id

    # 关闭
    async def patch_close(self,school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633')):
        # print(school)

        res = await self.school_rule.update_school_status(school_id,2)

        return res
        # return  school_id

    # 导入 todo 任务队列的
    async def importing(self,school:School):
        print(school)
        return  school
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
    # 新增 通信信息
    # async def post_comminfo(self,
    #                         school: PlanningSchoolCommunications,
    #
    #                         ):
    #
    #     res = await self.school_communication_rule.add_school_communication(school)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res
    #
    # # 新增 教学信息
    # async def post_eduinfo(self,
    #                        school: PlanningSchoolEduInfo,
    #
    #                        ):
    #
    #     res = await self.school_eduinfo_rule.add_school_eduinfo(school)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res
