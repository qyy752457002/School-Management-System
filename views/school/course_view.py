from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from views.models.majors import Majors
from views.models.course import Course

from fastapi import Query, Depends


class CourseView(BaseView):

    async def post(self, course: Course):
        print(course)
        return course




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]
        for i in range(page_request.per_page):
            items.append(Course(school_id='SJD1256526',course_no='19',grade_id='一年级',course_name='语文'))






        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, course_id:str= Query(..., title="", description="课程id",min_length=1,max_length=20,example='SC2032633'),):
        print(course_id)
        return  course_id

    # 修改 关键信息
    async def put(self,course:Course
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return  course