from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.multi_tenant.registry import tenant_registry
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from starlette.requests import Request

from common.decorators import require_role_permission
# from rules.subject_memebers_rule import SubjectMembersRule
from rules.subject_rule import  SubjectRule
from views.common.common_view import get_extend_params, get_tenant_current
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
    @require_role_permission("subject", "add")
    async def post(self, subject: Subject):
        print(subject)
        subject.id=None
        res = await  self.subject_rule.add_subject(subject)

        return res
    # 分页
    @require_role_permission("subject", "view")

    async def page(self,
                   request:Request,
                   page_request=Depends(PageRequest),
                   school_id: int |str= Query(0, title="学校ID", description="学校ID", examples=[1]),
                   subject_name: str = Query('', title=" ", description=" ", examples=[''])
                   ):
        print(page_request)
        obj =  await get_extend_params(request)
        items = []
        res = await self.subject_rule.query_subject_with_page(page_request,   school_id,subject_name, obj )
        print(2222,tenant_registry,vars(tenant_registry), )
        return res

    # 删除
    @require_role_permission("subject", "delete")

    async def delete(self,
                     id: int|str = Query(0, title="", description="", examples=[1]),
                       ):
        res = await self.subject_rule.delete_subject(id)

        return res

    # 修改
    @require_role_permission("subject", "edit")

    async def put(self,
                  orginization: Subject,
                  ):
        print(orginization)
        res = await self.subject_rule.update_subject(orginization)

        return res
#     todo  成员的curd
