from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.course_rule import CourseRule
# from views.models.courses import Courses
from views.models.course import Course

from fastapi import Query, Depends


class CourseView(BaseView):
    def __init__(self):
        super().__init__()
        self.course_rule = get_injector( CourseRule)

    async def post(self, course: Course):
        print(course)
        res =await self.course_rule.add_course(course)

        return res




    async def page(self,
                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),




                   ):
        print(page_request)
        items=[]

        res = await self.course_rule.query_course_with_page(page_request , )
        return res



        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 删除
    async def delete(self, course_id:int= Query(..., title="", description="课程id", example='SC2032633'),):
        print(course_id)
        # return  course_id
        res = await self.course_rule.softdelete_course(course_id)

        return  res

    # 修改 关键信息
    async def put(self,course:Course
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.course_rule.update_course(course)


        return  res


    # 获取所有的课程列表 给下拉
    async def get_all(self ):
        # print(page_request)
        items=[]


        res = await self.course_rule.get_course_all( {'school_id':0} )
        return res