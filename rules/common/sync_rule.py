from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model

from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.school_eduinfo_dao import SchoolEduinfoDAO
from daos.teachers_info_dao import TeachersInfoDao
from views.models.school import School as SchoolModel
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel, SchoolSyncQueryReModel
from views.models.school_communications import SchoolCommunications as SchoolCommunicationModel
from views.models.school_eduinfo import SchoolEduInfo as SchoolEduInfoModel


@dataclass_inject
class SyncRule(object):
    teachers_info_dao: TeachersInfoDao
    school_dao: SchoolDAO
    school_eduinfo_dao: SchoolEduinfoDAO
    school_communication_dao: SchoolCommunicationDAO

    async def query_sync_teacher_with_page(self, query_model: SupervisorSyncQueryModel, page_request: PageRequest):
        print("query_model")
        paging = await self.teachers_info_dao.query_sync_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SupervisorSyncQueryReModel)
        print(paging_result)
        return paging_result

    async def query_sync_school_with_page(self, query_model: SchoolSyncQueryModel, page_request: PageRequest):
        paging = await self.school_dao.query_sync_school_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SchoolSyncQueryReModel)
        return paging_result

    async def get_sync_teacher(self, teacher_id_number_list):
        sync_teacher_list = []
        for item in teacher_id_number_list:
            sync_teacher = await self.teachers_info_dao.get_sync_teacher(item)
            if sync_teacher:
                sync_teacher_list.append(orm_model_to_view_model(sync_teacher, SupervisorSyncQueryReModel))
        return sync_teacher_list

    async def get_sync_school(self, social_credit_code_list):
        sync_school_list = []
        for item in social_credit_code_list:
            school_info = {}
            sync_school = await self.school_dao.get_sync_school(item)
            if sync_school:
                school = orm_model_to_view_model(sync_school, SchoolModel)
                school_info["school"] = school
                school_id = school.id
                school_edu_info_db = await self.school_eduinfo_dao.get_school_eduinfo_by_school_id(school_id)
                school_edu_info = orm_model_to_view_model(school_edu_info_db, SchoolEduInfoModel)
                school_info["school_edu_info"] = school_edu_info
                school_communication_db = await self.school_communication_dao.get_school_communication_by_school_id(
                    school_id)
                school_communication = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel)
                school_info["school_communication"] = school_communication
                sync_school_list.append(school_info)
        return sync_school_list
