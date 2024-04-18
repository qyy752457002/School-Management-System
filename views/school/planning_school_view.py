from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo, PlanningSchoolKeyInfo, \
    PlanningSchoolStatus
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from models.grade import Grade
from rules.planning_school_rule import PlanningSchoolRule
from views.models.grades import Grades
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule

from rules.planning_school_eduinfo_rule import PlanningSchoolEduinfoRule

# 当前工具包里支持get  patch前缀的 方法的自定义使用
class PlanningSchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        self.planning_school_eduinfo_rule = get_injector(PlanningSchoolEduinfoRule)


    async def get(self, planning_school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
                                                        max_length=20, example='SC2032633'),
                  planning_school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                                                    example='XX小学'),
                  planning_school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),

                  ):
        planning_school = await self.planning_school_rule.get_planning_school_by_id(planning_school_id)
        return planning_school

    #  新增的实际结果  ID赋值
    async def post(self, planning_school: PlanningSchool):
        print(planning_school)
        res = await self.planning_school_rule.add_planning_school(planning_school)

        return res

    # 修改 关键信息
    async def put(self,
                  planning_school: PlanningSchoolKeyInfo,
                  # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                  ):
        # print(planning_school)

        res = await self.planning_school_rule.update_planning_school(planning_school)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res

    # 删除
    async def delete(self, planning_school_id: int = Query(..., title="", description="学校id/园所id",
                                                           example='2203'), ):
        print(planning_school_id)
        res = await self.planning_school_rule.softdelete_planning_school(planning_school_id)

        return res

    # 修改 变更 基本信息
    async def patch_baseinfo(self, planning_school_baseinfo: PlanningSchoolBaseInfo, ):
        # print(planning_school_baseinfo,type( planning_school_baseinfo))
        res = await self.planning_school_rule.update_planning_school(planning_school_baseinfo,2)

        return res

    async def page(self,
                   # planning_school_baseinfo:PlanningSchoolBaseInfo,
                   page_request=Depends(PageRequest),

                   planning_school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
                                                   max_length=20, example='SC2032633'),
                   planning_school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                                                     example='XX小学'),
                   status: PlanningSchoolStatus = Query(None, title="状态", description="状态")

                   ):
        print(page_request)
        items = []
        paging_result = await self.planning_school_rule.query_planning_school_with_page(page_request,
                                                                                        planning_school_name, None,
                                                                                        planning_school_no, )
        return paging_result

        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 开办
    async def patch_open(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                               min_length=1, max_length=20, example='SC2032633')):
        # print(planning_school)
        res = await self.planning_school_rule.update_planning_school_status(planning_school_id,1)

        return res

    # 关闭
    async def patch_close(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                min_length=1, max_length=20, example='SC2032633')):
        # print(planning_school)
        res = await self.planning_school_rule.update_planning_school_status(planning_school_id,2)

        return res

    # 导入 todo 任务队列的
    async def importing(self, planning_school: PlanningSchool):
        print(planning_school)
        return planning_school
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
    # 新增 通信信息
    async def post_comminfo(self,
                  planning_school: PlanningSchoolCommunications,
                  # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                  ):
        # print(planning_school)

        res = await self.planning_school_communication_rule.add_planning_school_communication(planning_school)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res

    # 新增 教学信息
    async def post_eduinfo(self,
                            planning_school: PlanningSchoolEduInfo,
                            # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                            ):
        # print(planning_school)

        res = await self.planning_school_eduinfo_rule.add_planning_school_eduinfo(planning_school)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res

