from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from starlette.requests import Request

# from rules.subject_memebers_rule import SubjectMembersRule
from rules.subject_rule import  SubjectRule
from views.common.common_view import get_extend_params
# from views.models.subject import Subject
from views.models.grades import Grades

from fastapi import Query, Depends

# from views.models.subject import Subject, SubjectMembers
from views.models.subject import Subject


# from rules.subject_rule import SubjectRule


class SubjectView(BaseView):
    def __init__(self):
        super().__init__()
        self.subject_rule = get_injector(SubjectRule)
    #  添加时过滤 删除态
    async def post(self, subject: Subject):
        print(subject)
        res = await  self.subject_rule.add_subject(subject)

        return res
    # 分页
    async def page(self,
                   request:Request,
                   page_request=Depends(PageRequest),
                   school_id: int = Query(0, title="学校ID", description="学校ID", examples=[1]),
                   subject_name: str = Query('', title=" ", description=" ", examples=[''])
                   ):
        print(page_request)
        obj =  await get_extend_params(request)
        items = []
        res = await self.subject_rule.query_subject_with_page(page_request,   school_id,subject_name, obj )
        return res

    # 删除  自动级联删除下层的部门
    async def delete(self,
                     org_id: int = Query(0, title="", description="", examples=[1]),
                       ):
        print(org_id)
        res = await self.subject_rule.delete_subject(org_id)

        return res

    # 修改
    async def put(self,
                  orginization: Subject,
                  # org_id: int = Query(0, title="", description="", examples=[1]),
                  # parent_id: int = Query(0, title="", description="", examples=[1]),
                  # org_name: str = Query('', title=" ", description=" ", examples=[''])
                  ):
        print(orginization)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        # subject= Subject(id=org_id, org_name=org_name,parent_id=parent_id)
        res = await self.subject_rule.update_subject(orginization)

        return res
#     todo  成员的curd
