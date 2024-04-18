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
    async def get(self,school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example=''),
                  school_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example=''),
                  school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),
                  ):

        school = await self.school_rule.get_school_by_id(school_id)
        return school


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
