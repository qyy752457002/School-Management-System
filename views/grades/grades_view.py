
from starlette.requests import Request

from views.common.common_view import get_extend_params

from fastapi import Query, Depends, Body
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from rules.grade_rule import GradeRule
from views.models.grades import Grades

class GradesView(BaseView):
    def __init__(self):
        super().__init__()
        self.grade_rule = get_injector(GradeRule)

    async def get(self,
                  grade_id: int = Query(None, title="", description="年级ID"),
                  city :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                  district :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                  ):
        account = await self.grade_rule.get_grade_by_id(grade_id)

        return account

    async def post(self, grades: Grades,request:Request):
        print(grades)
        #
        obj= await get_extend_params(request)
        grades.city = obj.city
        grades.district = obj.county_id
        if obj.school_id:
            grades.school_id = int(obj.school_id)

        res = await self.grade_rule.add_grade(grades,obj)
        return res

    async def page(self,
                   request:Request,

                   page_request=Depends(PageRequest),
                   school_id: int = Query(None, title="学校ID", description="学校ID"),
                   grade_name: str = Query(None, description="年级名称", min_length=1, max_length=20),
                   city :str= Query(None, title="市", description="",min_length=1,max_length=20,example=''),
                   district :str= Query(None, title="区", description="",min_length=1,max_length=20,example=''),
                   ):
        print(page_request)
        obj= await get_extend_params(request)

        if obj.school_id:
            school_id = int(obj.school_id)
        if obj.city:
            city = str(obj.city)
        if obj.county_id:
            district = str(obj.county_id)

        paging_result = await self.grade_rule.query_grade_with_page(page_request, grade_name, school_id,city, district)

        return paging_result

    #   搜索的 待处理
    async def query(self,
                    request:Request,

                    grade_name: str = Query('', description="年级名称", min_length=1, max_length=20),

                    city :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                    district :str= Query(None, title="", description="",min_length=1,max_length=20,example=''),
                    ):
        obj= await get_extend_params(request)

        lst = await self.grade_rule.query_grade(grade_name,obj)

        return lst

    # 删除
    async def delete(self, grade_id: int = Query(..., title="", description="年级id", example='1'), ):
        print(grade_id)
        # return  grade_id
        # todo 权限校验
        res = await self.grade_rule.delete_grade(grade_id)

        return res

    # 修改 关键信息
    async def put(self,
                  grades: Grades,
                  request:Request,

                  grade_id: int = Query(..., title="", description="年级id", example='1'),

                  ):
        print(grades,1111)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        grades.id = grade_id
        grades.created_at = None
        delattr(grades, 'created_at')

        obj= await get_extend_params(request)
        grades.city = obj.city
        grades.district = obj.county_id
        if obj.school_id:
            grades.school_id = int(obj.school_id)

        res = await self.grade_rule.update_grade(grades)

        return res

        # 手动进行 年级的继承
    async def put_grade_extend(self,
                  request:Request,

                  city: str  = Query('', title="", description="", example='1'),
                  district: str  = Query('', title="", description="", example='1'),
                  school_id: int   = Query(0, title="", description="", example='1'),

                  ):


        obj= await get_extend_params(request)


        res = await self.grade_rule.update_grade(None)

        return res
