from typing import List
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from starlette.requests import Request
from rules.course_rule import CourseRule
from views.common.common_view import get_extend_params
from views.models.course import Course
from fastapi import Query, Depends, Body

class CourseView(BaseView):
    def __init__(self):
        super().__init__()
        self.course_rule = get_injector( CourseRule)
    # 新增课程  市区  校
    async def post(self,
                   request:Request,

                   school_id:int= Query(...,   description="学校ID", example='1'),
                   course_list:List[Course]= Body([], description="选择的课程" , example= [{"course_id":1,"course_name":"语文","course_no":"19","school_id":1,} ]),

                   ):
        # print(course)
        obj= await get_extend_params(request)
        for course in course_list:

            course.city = obj.city
            course.district = obj.county_id
            if obj.school_id:
                course.school_id = int(obj.school_id)
        res =await self.course_rule.add_course_school(school_id,course_list )

        return res


    # 分页

    async def page(self,
                   request:Request,

                   page_request= Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),
                   school_id:int= Query(0,   description="学校ID", example='1'),
                   ):
        print(page_request)
        obj= await get_extend_params(request)

        items=[]

        res = await self.course_rule.query_course_with_page(page_request ,school_id,extobj=obj )
        return res

    # 删除
    async def delete(self, course_id:int= Query(..., title="", description="课程id", example='SC2032633'),):
        print(course_id)
        # return  course_id
        res = await self.course_rule.softdelete_course(course_id)

        return  res

    # 修改 当前用的这个  学校的课程选择 的变更
    async def put(self,
        school_id:int= Query(...,   description="学校ID", example='1'),
        course_list:List[Course]= Body([], description="选择的课程" , example= [{"course_id":1,"course_name":"语文","course_no":"19","school_id":1,} ]),
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.course_rule.softdelete_course_by_school_id(school_id)

        res =await self.course_rule.add_course_school(school_id,course_list )

        return  res

