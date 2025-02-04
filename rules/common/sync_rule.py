from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model

from daos.campus_communication_dao import CampusCommunicationDAO
from daos.campus_dao import CampusDAO
from daos.campus_eduinfo_dao import CampusEduinfoDAO
from daos.planning_school_communication_dao import PlanningSchoolCommunicationDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.planning_school_eduinfo_dao import PlanningSchoolEduinfoDAO
from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.school_eduinfo_dao import SchoolEduinfoDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.teachers_info_dao import TeachersInfoDao
from rules.leader_info_rule import LeaderInfoRule
from views.models.campus import Campus as CampusModel
from views.models.campus_communications import CampusCommunications as CampusCommunicationModel
from views.models.campus_eduinfo import CampusEduInfo as CampusEduInfoModel
from views.models.planning_school import PlanningSchoolSyncModel
from views.models.planning_school_communications import PlanningSchoolCommunications as PlanningSchoolCommunicationModel
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo as PlanningSchoolEduInfoModel
from views.models.school import SchoolSyncModel
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel, SchoolSyncQueryReModel, SchoolInfoSyncModel, StudentSyncModel, TeacherSyncToArtModel
from views.models.school_communications import SchoolCommunications as SchoolCommunicationModel
from views.models.school_eduinfo import SchoolEduInfo as SchoolEduInfoModel


@dataclass_inject
class SyncRule(object):
    teachers_info_dao: TeachersInfoDao
    school_dao: SchoolDAO
    school_eduinfo_dao: SchoolEduinfoDAO
    school_communication_dao: SchoolCommunicationDAO
    campus_dao: CampusDAO
    campus_eduinfo_dao: CampusEduinfoDAO
    campus_communication_dao: CampusCommunicationDAO
    planning_school_dao: PlanningSchoolDAO
    planning_school_eduinfo_dao: PlanningSchoolEduinfoDAO
    planning_school_communication_dao: PlanningSchoolCommunicationDAO
    students_base_info_dao: StudentsBaseInfoDao

    async def query_sync_teacher_with_page(self, query_model: SupervisorSyncQueryModel, page_request: PageRequest):
        print("query_model")
        paging = await self.teachers_info_dao.query_sync_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SupervisorSyncQueryReModel)
        print(paging_result)
        return paging_result

    async def query_sync_school_with_page(self, query_model: SchoolSyncQueryModel, page_request: PageRequest):
        if query_model.type == "planning_school":
            paging = await self.planning_school_dao.query_sync_planning_school_with_page(query_model, page_request)
        elif query_model.type == "school":
            paging = await self.school_dao.query_sync_school_with_page(query_model, page_request)
        else:
            paging = await self.campus_dao.query_sync_campus_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, SchoolSyncQueryReModel)
        return paging_result

    async def get_sync_teacher(self, teacher_id_number_list):
        sync_teacher_list = []
        for item in teacher_id_number_list:
            sync_teacher = await self.teachers_info_dao.get_sync_teacher(item)
            if sync_teacher:
                sync_teacher_list.append(orm_model_to_view_model(sync_teacher, SupervisorSyncQueryReModel))
        return sync_teacher_list

    async def get_sync_school(self, unique_code_list):
        sync_school_list = []
        leader_info_rule = get_injector(LeaderInfoRule)
        for item in unique_code_list:
            school_info = {}
            sync_planing_school = await self.planning_school_dao.get_sync_school(item)
            sync_school = await self.school_dao.get_sync_school(item)
            sync_campus = await self.campus_dao.get_sync_campus(item)
            if sync_planing_school:
                school = orm_model_to_view_model(sync_planing_school, PlanningSchoolSyncModel)
                school_info["school"] = school
                planning_school_id = school.id
                school_edu_info_db = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_planning_school_id(
                    planning_school_id)
                school_edu_info = orm_model_to_view_model(school_edu_info_db, PlanningSchoolEduInfoModel)
                school_info["school_edu_info"] = school_edu_info
                school_communication_db = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(
                    planning_school_id)
                school_communication = orm_model_to_view_model(school_communication_db,
                                                               PlanningSchoolCommunicationModel)
                school_info["school_communication"] = school_communication
                leader_info_list = await leader_info_rule.get_all_leader_info(planning_school_id, None)
                school_info["leader_info"] = leader_info_list
                sync_school_list.append(school_info)
                continue
            if sync_school:
                school = orm_model_to_view_model(sync_school, SchoolSyncModel)
                school_info["school"] = school
                school_id = school.id
                school_edu_info_db = await self.school_eduinfo_dao.get_school_eduinfo_by_school_id(school_id)
                school_edu_info = orm_model_to_view_model(school_edu_info_db, SchoolEduInfoModel)
                school_info["school_edu_info"] = school_edu_info
                school_communication_db = await self.school_communication_dao.get_school_communication_by_school_id(
                    school_id)
                school_communication = orm_model_to_view_model(school_communication_db, SchoolCommunicationModel)
                school_info["school_communication"] = school_communication
                leader_info_list = await leader_info_rule.get_all_leader_info(None, school_id)
                school_info["leader_info"] = leader_info_list
                sync_school_list.append(school_info)
                continue
            if sync_campus:
                campus = orm_model_to_view_model(sync_campus, CampusModel,
                                                 exclude=["primary_campus_system", "junior_middle_campus_system",
                                                          "senior_middle_planning_school_system"])
                school_info["school"] = campus
                campus_id = campus.id
                school_id = campus.school_id
                campus_edu_info_db = await self.campus_eduinfo_dao.get_campus_eduinfo_by_campus_id(campus_id)
                campus_edu_info = orm_model_to_view_model(campus_edu_info_db, CampusEduInfoModel)
                school_info["school_edu_info"] = campus_edu_info
                campus_communication_db = await self.campus_communication_dao.get_campus_communication_by_campus_id(
                    campus_id)
                campus_communication = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel)
                school_info["school_communication"] = campus_communication
                leader_info_list = await leader_info_rule.get_all_leader_info(None, school_id)
                school_info["leader_info"] = leader_info_list
                sync_school_list.append(school_info)
        return sync_school_list

    async def get_all_school(self):
        sync_school_list = []
        result = await self.school_dao.get_all_school()
        for item in result:
            sync_school_list.append(orm_model_to_view_model(item, SchoolInfoSyncModel))
        return sync_school_list

    async def get_school_by_school_no(self, unique_code_list):
        sync_school_list = []
        for school_no in unique_code_list:
            sync_school = await self.school_dao.get_school_by_school_no(school_no)
            sync_planning_school = await self.planning_school_dao.get_planning_school_by_school_no(school_no)
            sync_campus = await self.campus_dao.get_campus_by_school_no(school_no)
            if sync_school:
                sync_school_list.append(orm_model_to_view_model(sync_school, SchoolInfoSyncModel))
                continue
            if sync_planning_school:
                sync_school_list.append(orm_model_to_view_model(sync_planning_school, SchoolInfoSyncModel))
                continue
            if sync_campus:
                sync_school_list.append(orm_model_to_view_model(sync_campus, SchoolInfoSyncModel))
                continue
        return sync_school_list

    async def get_sync_student_by_school_no(self, school_no):
        sync_school = await self.school_dao.get_school_by_school_no(school_no)
        sync_planning_school = await self.planning_school_dao.get_planning_school_by_school_no(school_no)
        sync_campus = await self.campus_dao.get_campus_by_school_no(school_no)
        school_type = ""
        if sync_planning_school:
            school_type = "planning_school"
        elif sync_school:
            school_type = "school"
        elif sync_campus:
            school_type = "campus"
        else:
            raise Exception("未找到该学校")
        result = await self.students_base_info_dao.get_sync_student_by_school_no(school_no, school_type)
        sync_student_list = []
        for item in result:
            sync_student_list.append(orm_model_to_view_model(item, StudentSyncModel))
        return sync_student_list

    async def get_sync_teacher_to_art(self, school_no):
        result = await self.teachers_info_dao.get_sync_teacher_by_school_no(school_no)
        sync_sync_list = []
        for item in result:
            sync_sync_list.append(orm_model_to_view_model(item, TeacherSyncToArtModel))
        return sync_sync_list
