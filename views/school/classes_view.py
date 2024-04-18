from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.classes import Classes
from views.models.grades import Grades

from fastapi import Query, Depends
from rules.classes_rule import ClassesRule


class ClassesView(BaseView):
    def __init__(self):
        super().__init__()
        self.classes_rule = get_injector( ClassesRule)

    async def post(self, classes: Classes):
        print(classes)
        res =await  self.classes_rule.add_classes(classes)

        return res




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        res = await self.classes_rule.query_classes_with_page(page_request , )
        return res






    # 删除
    async def delete(self, class_id:str= Query(..., title="", description="班级id",min_length=1,max_length=20,example='SC2032633'),):
        print(class_id)
        res = await self.classes_rule.softdelete_classes(class_id)

        return  res

    # 修改 关键信息
    async def put(self,classes:Classes
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.classes_rule.update_classes(classes)

        return  res