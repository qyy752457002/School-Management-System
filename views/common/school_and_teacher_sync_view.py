from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query, Depends, Body

from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel
from rules.common.sync_rule import SyncRule
from typing import List, Type


class SchoolTeacherView(BaseView):
    def __init__(self):
        super().__init__()
        self.sync_rule = get_injector(SyncRule)

    async def page_school(self, query_model=Depends(SchoolSyncQueryModel),
                          page_request=Depends(PageRequest)) -> PaginatedResponse:
        pass

    async def page_teachers(self, query_model=Depends(SupervisorSyncQueryModel),
                            page_request=Depends(PageRequest)) -> PaginatedResponse:
        res = await self.sync_rule.query_sync_teacher_with_page(query_model, page_request)
        return res

    async def get_sync_teacher(self, teacher_id_number_list: List[str] | None = Query([], title="", description="身份证件号",
                                                                           examples=['3425301994'])) -> List[
        SupervisorSyncQueryReModel]:
        res = await self.sync_rule.get_sync_teacher(teacher_id_number_list)
        return res
