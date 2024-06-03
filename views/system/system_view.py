from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.sub_system_rule import SubSystemRule
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.sub_system import SubSystem


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class SystemView(BaseView):
    def __init__(self):
        super().__init__()
        self.sub_system_rule = get_injector(SubSystemRule)

    async def page(self,
                   page_request=Depends(PageRequest),
                   role_id: int = Query(None, title="", description="角色id",
                                                 example='1'),

                   unit_type :str= Query(None, title="单位类型 例如学校 市/区", description="",min_length=1,max_length=20,example=''),
                   edu_type :str= Query(None, title="教育阶段类型 例如幼儿园 中小学 职高", description="",min_length=1,max_length=20,example=''),
                   system_type :str= Query(None, title="系统类型 例如老师 单位 学生", description="",min_length=1,max_length=20,example=''),

                   ):
        print(page_request)
        items = []
        res = await self.sub_system_rule.query_sub_system_with_page(page_request, )
        return res
        # res = SubSystem(system_name='学校版',
        #                 system_no='02',
        #                 system_url='www.fsdfsd.cc',
        #                 system_icon='www.dd.cc/343.jpg',
        #                 system_description='学校版的教育登录')
        #
        # for i in range(0, 1):
        #     items.append(res)
        # print(items)
        #
        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
        #                          per_page=page_request.per_page, total=100, items=items)
