from mini_framework.utils.http import HTTPRequest
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.annual_review_dao import AnnualReviewDAO
from models.annual_review import AnnualReview
from views.models.teacher_extend import AnnualReviewModel, AnnualReviewUpdateModel
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from daos.school_dao import SchoolDAO


@dataclass_inject
class SyncRule(object):
    teachers_info_dao: TeachersInfoDao
    school_dao: SchoolDAO

    async def query_sync_teacher_with_page(self, query_model: SupervisorSyncQueryModel, page_request: PageRequest):
        print("query_model")
        paging = await self.teachers_info_dao.query_sync_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SupervisorSyncQueryReModel)
        print(paging_result)
        return paging_result

    async def query_sync_school_with_page(self, query_model: SchoolSyncQueryModel, page_request: PageRequest):
        paging = await self.school_dao.query_sync_school_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SupervisorSyncQueryReModel)
        return paging_result

    async def get_sync_teacher(self, teacher_id_number_list):
        sync_teacher_list = []
        for item in teacher_id_number_list:
            sync_teacher = await self.teachers_info_dao.get_sync_teacher(item)
            if sync_teacher:
                sync_teacher_list.append(orm_model_to_view_model(sync_teacher, SupervisorSyncQueryReModel))
        return sync_teacher_list
