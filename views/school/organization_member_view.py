from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from common.decorators import require_role_permission
from rules.organization_memebers_rule import OrganizationMembersRule
from rules.organization_rule import OrganizationRule
# from views.models.organization import Organization
from views.models.grades import Grades

from fastapi import Query, Depends

from views.models.organization import Organization, OrganizationMembers


# from rules.organization_rule import OrganizationRule


class OrganizationMemberView(BaseView):
    def __init__(self):
        super().__init__()
        self.organization_rule = get_injector(OrganizationRule)
        self.organization_members_rule = get_injector(OrganizationMembersRule)
    # 新增成员
    @require_role_permission("organization", "add")

    async def post(self, organization_members: OrganizationMembers):
        # print(organization)
        res = await  self.organization_members_rule.add_organization_members(organization_members)

        return res
    # 分页 成员列表
    @require_role_permission("organization", "view")

    async def page(self,
                   page_request=Depends(PageRequest),
                   school_id: int|str = Query(0, title="学校ID", description="学校ID", examples=[1]),

                   parent_id: int |str= Query(0, title="", description="表示要查询的部门ID", examples=[1]),
                   org_ids: str = Query('', title="", description="", examples=[1]),
                    teacher_name: str = Query('', title=" ", description=" ", examples=['']),
                    teacher_no: str = Query('', alias='teacher_number', title=" ", description=" ", examples=['']),
                    mobile: str = Query('', alias='teacher_mobile',title=" ", description=" ", examples=['']),
                   birthday: str = Query('', alias='teacher_date_of_birth',title=" ", description=" ", examples=['']),

                   ):
        print(page_request)
        items = []
        res = await self.organization_members_rule.query_organization_members_with_page(page_request, parent_id , school_id,teacher_name,teacher_no,mobile,birthday,org_ids  )
        return res

    # 删除
    @require_role_permission("organization", "delete")

    async def delete(self,
                     id: int |str= Query(0, title="", description="", examples=[1]),
                     # org_id: int = Query(0, title="", description="", examples=[1]),
                     ):
        res = await self.organization_members_rule.delete_organization_members(id)

        return res

    # 修改
    @require_role_permission("organization", "edit")

    async def put(self,
                                       organization_members: OrganizationMembers

                  ):
        # print(planning_school)
        res = await self.organization_members_rule.update_organization_members(organization_members)

        return res