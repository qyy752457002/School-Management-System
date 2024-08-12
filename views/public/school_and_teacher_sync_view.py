from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Depends, Body

from fastapi.params import Param
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel
from rules.common.sync_rule import SyncRule

from typing import List

from fastapi import Depends, Body, Query
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.common.sync_rule import SyncRule
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel


class SchoolTeacherView(BaseView):
    def __init__(self):
        super().__init__()
        self.sync_rule = get_injector(SyncRule)

    async def page_school(self, query_model=Depends(SchoolSyncQueryModel),
                          page_request=Depends(PageRequest)) -> PaginatedResponse:
        res = await self.sync_rule.query_sync_school_with_page(query_model, page_request)
        return res

    async def page_teachers(self, query_model=Depends(SupervisorSyncQueryModel),
                            page_request=Depends(PageRequest)) -> PaginatedResponse:
        res = await self.sync_rule.query_sync_teacher_with_page(query_model, page_request)
        return res

    async def post_sync_teacher(self,
                                teacher_id_number_list: List[str] | None = Body(None, title="",
                                                                                description="身份证件号",
                                                                                examples=['3425301994'])) -> List[
        SupervisorSyncQueryReModel]:
        res = await self.sync_rule.get_sync_teacher(teacher_id_number_list)
        print(res)
        return res

    async def post_sync_school(self, unique_code_list: List[str] | None = Body([], title="",
                                                                               description="统一社会信用代码",
                                                                               examples=['3425301994'])) -> List:
        res = await self.sync_rule.get_sync_school(unique_code_list)
        return res

    async def get_all_school(self):
        res = await self.sync_rule.get_all_school()
        return res


    async def post_school_by_school_no(self, unique_code_list: List[str] | None =Body([], title="",
                                                                             description="学校代码",
                                                                             examples=['3425301994'])) -> List:
        res = await self.sync_rule.get_school_by_school_no(unique_code_list)
        return res
