from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.organization_memebers_rule import OrganizationMembersRule
from rules.organization_rule import OrganizationRule
# from views.models.organization import Organization
from views.models.grades import Grades

from fastapi import Query, Depends

from views.models.organization import Organization, OrganizationMembers


# from rules.organization_rule import OrganizationRule


class OrganizationView(BaseView):
    def __init__(self):
        super().__init__()
        self.organization_rule = get_injector(OrganizationRule)
        self.organization_members_rule = get_injector(OrganizationMembersRule)

    async def post(self, organization: Organization):
        print(organization)
        res = await  self.organization_rule.add_organization(organization)

        return res
    # 分页 支持查询 一级类目下面的二三级类目
    async def page(self,
                   page_request=Depends(PageRequest),
                   school_id: int = Query(0, title="学校ID", description="学校ID", examples=[1]),

                   parent_id: int = Query(0, title="", description="表示要查询的部门ID ", examples=[1]),
                   ):
        print(page_request)
        items = []
        res = await self.organization_rule.query_organization_with_page(page_request, parent_id , school_id,  )
        return res

    # 删除
    async def delete(self,
                     org_id: int = Query(0, title="", description="", examples=[1]),
                       ):
        print(org_id)
        res = await self.organization_rule.delete_organization(org_id)

        return res

    # 修改
    async def put(self,

                  org_id: int = Query(0, title="", description="", examples=[1]),
                  parent_id: int = Query(0, title="", description="", examples=[1]),

                  org_name: str = Query('', title=" ", description=" ", examples=[''])
                  ):
        # print(planning_school)
        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        organization= Organization(id=org_id, org_name=org_name,parent_id=parent_id)
        res = await self.organization_rule.update_organization(organization)

        return res
#     todo  成员的curd

    async def post_organization_members(self, organization_members: OrganizationMembers):
        # print(organization)
        res = await  self.organization_members_rule.add_organization_members(organization_members)

        return res
    # 分页 成员列表
    async def page_organization_members(self,
                   page_request=Depends(PageRequest),
                   school_id: int = Query(0, title="学校ID", description="学校ID", examples=[1]),

                   parent_id: int = Query(0, title="", description="表示要查询的部门ID", examples=[1]),
                    teacher_name: str = Query('', title=" ", description=" ", examples=['']),
                    teacher_no: str = Query('', title=" ", description=" ", examples=['']),
                    mobile: str = Query('', title=" ", description=" ", examples=['']),
                    birthday: str = Query('', title=" ", description=" ", examples=['']),

                   ):
        print(page_request)
        items = []
        res = await self.organization_members_rule.query_organization_members_with_page(page_request, parent_id , school_id,teacher_name,teacher_no,mobile,birthday  )
        return res
