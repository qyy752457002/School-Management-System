from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.common.common_view import convert_snowid_in_model
from views.models.classes import Classes
from views.models.grades import Grades

from fastapi import Query, Depends
from rules.classes_rule import ClassesRule

class ClassesView(BaseView):
    def __init__(self):
        super().__init__()
        self.classes_rule = get_injector(ClassesRule)


    async def page(self,
                   page_request=Depends(PageRequest),

                   borough: str = Query('', title=" ", description=" 行政管辖区", examples=['铁西区']),
                   block: str = Query('', title=" ", description="地域管辖区", examples=['铁西区']),

                   school_id: int|str  = Query(0, title="学校ID", description="学校ID", examples=[1]),
                   school_no: int|str  = Query(None, title="学校编号", description="学校编号", examples=[]),

                   grade_id: int|str  = Query(0, title="年级ID", description="年级ID", examples=[2]),
                   class_name: str = Query('', title="Grade_name", description="班级名称", examples=['一年级'])

                   ):
        school_id= int(school_id)
        # grade_id= int(grade_id)
        print(page_request)
        items = []
        res = await self.classes_rule.query_classes_with_page(page_request, borough, block, school_id, grade_id,
                                                              class_name,school_no)
        return res
 