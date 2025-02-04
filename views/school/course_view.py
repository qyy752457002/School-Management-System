from copy import deepcopy
from typing import List
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from starlette.requests import Request

from common.decorators import require_role_permission
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from rules.course_rule import CourseRule
from views.common.common_view import get_extend_params, convert_snowid_to_strings, convert_snowid_in_model
from views.models.course import Course
from fastapi import Query, Depends, Body


class CourseView(BaseView):
    def __init__(self):
        super().__init__()
        self.course_rule = get_injector(CourseRule)

    # 新增课程  市区  校
    @require_role_permission("course", "add")
    async def post(self,
                   request: Request,
                   school_id: int | str = Query(..., description="学校ID", example='1'),
                   course_list: List[Course] = Body([], description="选择的课程", example=[
                       {"course_id": 1, "course_name": "语文", "course_no": "19", "school_id": 1, }]),

                   ):
        # print(course)
        obj = await get_extend_params(request)
        for course in course_list:

            course.city = obj.city
            course.district = obj.county_id
            if obj.school_id:
                course.school_id = int(obj.school_id)
        res = await self.course_rule.add_course_school(school_id, course_list)

        return res

    # 分页
    @require_role_permission("course", "view")


    async def page(self,
                   request: Request,

                   page_request=Depends(PageRequest),
                   # campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   # campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),
                   school_id: int | str = Query(0, description="学校ID", example='1'),
                   ):
        extend_params= obj= await get_extend_params(request)
        print('rucan',page_request,obj)

        if obj.school_id and school_id==0:
            school_id = obj.school_id

        items = []
        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao=get_injector(TenantDAO)
            school_dao=get_injector(SchoolDAO)
            tenant =  await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)


            if tenant is   not None and  tenant.tenant_type== 'school' and len(tenant.code)>=10:
                school =  await  school_dao.get_school_by_id(tenant.origin_id)
                if school:
                    school_id = school.id

            pass

        res = await self.course_rule.query_course_with_page(page_request, school_id, extobj=obj)
        return res

    # 删除
    async def delete(self, course_id: int | str = Query(..., title="", description="课程id", example='SC2032633'), ):
        print(course_id)
        # return  course_id
        res = await self.course_rule.softdelete_course(course_id)
        res = deepcopy(res)
        convert_snowid_in_model(res)

        return res

    # 修改 当前用的这个  学校的课程选择 的变更 区的配置课程也是这个接口
    async def put(self,
                  request: Request,
                  school_id: int | str = Query(0, description="学校ID", example='1'),
                  course_list: List[Course] = Body([], description="选择的课程", example=[
                      {"grade_id": 1, "course_name": "语文", "course_no": "13", }
                  ])
                  ):
        extend_params=obj = await get_extend_params(request)
        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao=get_injector(TenantDAO)
            school_dao=get_injector(SchoolDAO)
            tenant =  await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)

            if tenant is   not None and  tenant.tenant_type== 'school' and len(tenant.code)>=10:
                school =  await  school_dao.get_school_by_id(tenant.origin_id)
                if school:
                    school_id = school.id
                    obj.school_id= school_id
                    print('使用了 租户的学校ID',school_id)

            pass

        # print(planning_school)
        # if obj.school_id:
        #     school_id = obj.school_id
        if obj.county_id:
            res = await self.course_rule.softdelete_course_by_district(obj.county_id)

        else:
            res = await self.course_rule.softdelete_course_by_school_id(school_id)
        res = await self.course_rule.add_course_school(school_id, course_list, obj)

        return res

    # 获取所有的课程列表 给下拉 在用

    async def get_all(self,request: Request,):
        # print(page_request)
        items = []
        extend_params= obj= await get_extend_params(request)
        # print('rucan',page_request,obj)

        items = []
        school=None
        filter_dict = { 'is_deleted': False}
        school_id=0
        if extend_params.school_id  :
            filter_dict['school_id'] = school_id
            # 读取类型  读取ID  加到条件里
            school_dao=get_injector(SchoolDAO)
            school =  await  school_dao.get_school_by_id(extend_params.school_id)
            if school:
                # school_id = school.id
                # filter_dict['school_nature'] = school.school_category

                pass



            pass
        res = await self.course_rule.get_course_all(filter_dict,school)
        return res

    async def post_add_init_course(self, course: Course):
        print(course)
        res = await self.course_rule.add_course(course)

        return res

    # 删除
    async def delete_init_course(self, course_id: int | str = Query(..., title="", description="课程id",
                                                                    example='SC2032633'), ):
        print(course_id)
        # return  course_id
        res = await self.course_rule.softdelete_course(course_id)

        return res

    # 修改 关键信息
    async def put_init_course(self, course: Course
                              ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res = await self.course_rule.update_course(course)

        return res
