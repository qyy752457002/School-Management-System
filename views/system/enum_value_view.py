from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.enum_value_rule import EnumValueRule
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.enum_value import EnumValue


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class EnumValueView(BaseView):
    def __init__(self):
        super().__init__()
        self.enum_value_rule = get_injector( EnumValueRule)

    async def page(self,
                   page_request=Depends(PageRequest),
                   enum_name:str= Query(..., title="", description="枚举类型的名称",min_length=1,max_length=20,example='province'),
                   parent_code:str= Query('', title="", description="父级的code",min_length=1,max_length=20,example='130000'),

                   ):
        print(page_request)
        items = []

        res = await self.enum_value_rule.query_enum_value_with_page(page_request ,enum_name,parent_code )
        return res
        #
        # res = EnumValue(enum_name="国家", enum_value="中国", description="", sort_number=1, parent_id="")
        #
        #
        # for i in range(0, 1):
        #     items.append(res)
        # print(items)
        #
        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
        #                          per_page=page_request.per_page, total=100, items=items)

    # 获取所有的课程列表 给下拉
    # async def get_all(self ):
    #     # print(page_request)
    #     items=[]
    #     res = await self.enum_value_rule.get_enum_value_all( {'school_id':0} )
    #     return res
