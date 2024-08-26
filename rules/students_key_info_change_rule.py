from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.student import StudentNotFoundError
from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.student_key_info_change_dao import StudentKeyInfoChangeDAO
from daos.student_session_dao import StudentSessionDao
from daos.students_dao import StudentsDao
from models.students_key_info_change import StudentKeyInfoChange
from views.common.common_view import page_none_deal
# from views.models.student_inner_transaction import StudentsKeyinfo as StudentsKeyinfoModel
from views.models.students import NewBaseInfoCreate, StudentsBaseInfo, StudentsKeyinfo
from views.models.students import NewStudentsQuery, NewStudentsQueryRe


@dataclass_inject
class StudentsKeyInfoChangeRule(object):
    student_key_info_change_dao: StudentKeyInfoChangeDAO
    students_dao: StudentsDao
    student_session_dao: StudentSessionDao
    school_dao: SchoolDAO
    school_commu_dao: SchoolCommunicationDAO

    async def get_student_key_info_change_by_student_id(self, student_id):
        """
        获取单个学生信息
        """
        student_key_info_change_db = await self.student_key_info_change_dao.get_student_key_info_change_by_student_id(student_id)
        if not student_key_info_change_db:
            raise StudentNotFoundError()
        student_key_info_change = orm_model_to_view_model(student_key_info_change_db, StudentsBaseInfo, exclude=[""])
        schoolinfo = await self.school_dao.get_school_by_id(student_key_info_change_db.school_id)
        if schoolinfo:
            student_key_info_change.block = schoolinfo.block
            student_key_info_change.borough = schoolinfo.borough
        schoolcominfo = await self.school_commu_dao.get_school_communication_by_school_id(student_key_info_change_db.school_id)
        if schoolcominfo:
            student_key_info_change.loc_area = schoolcominfo.loc_area
            student_key_info_change.loc_area_pro = schoolcominfo.loc_area_pro

        return student_key_info_change

    async def get_student_key_info_change_by_id(self, students_base_id):
        """
        获取单个信息
        """
        student_key_info_change_db = await self.student_key_info_change_dao.get_student_key_info_change_by_id(students_base_id)
        if not student_key_info_change_db:
            raise StudentNotFoundError()
        student_key_info_change = orm_model_to_view_model(student_key_info_change_db, StudentsKeyinfo, exclude=[""])
        return student_key_info_change


    # 新增 基本信息变更  记录
    async def add_student_key_info_change(self, student_key_info_change: NewBaseInfoCreate):
        """
        """
        exits_student = await self.students_dao.get_students_by_id(student_key_info_change.student_id)
        if not exits_student:
            raise StudentNotFoundError()

        student_key_info_change_db = view_model_to_orm_model(student_key_info_change, StudentKeyInfoChange, exclude=["student_base_id"])

        student_key_info_change_db = await self.student_key_info_change_dao.add_student_key_info_change(student_key_info_change_db)
        student_key_info_change = orm_model_to_view_model(student_key_info_change_db, StudentsBaseInfo, exclude=[""])
        return student_key_info_change

    async def update_student_key_info_change(self, student_key_info_change):
        """
        编辑学生基本信息
        """
        exists_student_key_info_change = await self.student_key_info_change_dao.get_student_key_info_change_by_student_id(
            student_key_info_change.student_id)
        if not exists_student_key_info_change:
            raise StudentNotFoundError()
        need_update_list = []
        for key, value in student_key_info_change.dict().items():
            if value:
                need_update_list.append(key)
        student_key_info_change = await self.student_key_info_change_dao.update_student_key_info_change(student_key_info_change,
                                                                                         *need_update_list)
        return student_key_info_change

    async def delete_student_key_info_change(self, students_id):
        """
        删除学生基本信息
        """
        exists_student_key_info_change = await self.student_key_info_change_dao.get_student_key_info_change_by_student_id(students_id)
        if not exists_student_key_info_change:
            raise StudentNotFoundError()
        student_key_info_change_db = await self.student_key_info_change_dao.delete_student_key_info_change(exists_student_key_info_change)
        return student_key_info_change_db

    async def query_student_key_info_change_with_page(self, query_model: NewStudentsQuery,
                                                 page_request: PageRequest) -> PaginatedResponse:
        """
        分页查询
        """
        paging = await self.student_key_info_change_dao.query_students_with_page(query_model, page_request)

        paging_result = PaginatedResponse.from_paging(page_none_deal(paging), NewStudentsQueryRe)
        return paging_result

    async def get_student_key_info_change_count(self):
        """
        获取学生信息数量
        """
        count = await self.student_key_info_change_dao.get_student_base_info_count()
        return count
