from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.classes import Classes
from views.models.grades import Grades

from fastapi import Query, Depends


class ClassesView(BaseView):

    async def post(self, classes: Classes):
        print(classes)
        return classes




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(Classes(school_id='1',grade_no='1',grade_id='1',class_name='1',class_number='1',year_established='1',teacher_id_card='1',teacher_name='1',education_stage='1',school_system='1',monitor='1',class_type='1',is_bilingual_class='1',major_for_vocational='',bilingual_teaching_mode='1',ethnic_language='1',))




        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, class_id:str= Query(..., title="", description="班级id",min_length=1,max_length=20,example='SC2032633'),):
        print(class_id)
        return  class_id

    # 修改 关键信息
    async def put(self,classes:Classes
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return  classes