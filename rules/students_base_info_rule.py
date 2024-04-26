from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.students_base_info import StudentBaseInfo
from views.common.common_view import page_none_deal
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel
from views.models.students import NewBaseInfoCreate,NewBaseInfoUpdate,StudentsBaseInfo
from views.models.students import StudentsBaseInfo as StudentsBaseInfoModel
from views.models.students import NewStudentsQuery, NewStudentsQueryRe
from business_exceptions.student import StudentNotFoundError,StudentExistsError


@dataclass_inject
class StudentsBaseInfoRule(object):
    students_base_info_dao: StudentsBaseInfoDao
    students_dao: StudentsDao

    async def get_students_base_info_by_student_id(self, student_id):
        """
        获取单个学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_students_base_info_by_student_id(student_id)
        if not students_base_info_db:
            raise StudentNotFoundError()
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        return students_base_info

    async def get_students_base_info_by_id(self, students_base_id):
        """
        获取单个学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_students_base_info_by_id(students_base_id)
        if not students_base_info_db:
            raise StudentNotFoundError()
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        return students_base_info



    async def add_students_base_info(self, students_base_info: NewBaseInfoCreate):
        """
        新增学生基本信息
        """
        exits_student = await self.students_dao.get_students_by_id(students_base_info.student_id)
        if not exits_student:
            raise StudentNotFoundError()
        exits_student_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(
            students_base_info.student_id)
        if exits_student_base_info:
            raise StudentExistsError()
        students_base_info_db = view_model_to_orm_model(students_base_info, StudentBaseInfo, exclude=[""])
        students_base_info_db = await self.students_base_info_dao.add_students_base_info(students_base_info_db)
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsBaseInfo, exclude=[""])
        return students_base_info

    async def update_students_base_info(self, students_base_info):
        """
        编辑学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(
            students_base_info.student_id)
        if not exists_students_base_info:
            raise StudentNotFoundError()
        need_update_list = []
        for key, value in students_base_info.dict().items():
            if value:
                need_update_list.append(key)
        students_base_info = await self.students_base_info_dao.update_students_base_info(students_base_info,
                                                                                         *need_update_list)
        return students_base_info

    async def update_students_class_division(self, class_id, student_ids):
        """
        编辑学生基本信息
        """

        students_base_info = await self.students_base_info_dao.update_students_class_division(class_id, student_ids)
        # 写入分班记录表
        await self.students_dao.add_students_class_division(class_id, student_ids)
        return students_base_info

    async def delete_students_base_info(self, students_id):
        """
        删除学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_student_id(students_id)
        if not exists_students_base_info:
            raise StudentNotFoundError()
        students_base_info_db = await self.students_base_info_dao.delete_students_base_info(exists_students_base_info)
        return students_base_info_db

    async def query_students_base_info_with_page(self, query_model: NewStudentsQuery,
                                                 page_request: PageRequest) -> PaginatedResponse:
        """
        分页查询
        """
        paging = await self.students_base_info_dao.query_students_with_page(query_model, page_request)

        paging_result = PaginatedResponse.from_paging(page_none_deal(paging), NewStudentsQueryRe)
        return paging_result

    async def get_students_base_info_count(self):
        """
        获取学生信息数量
        """
        count = await self.students_base_info_dao.get_student_base_info_count()
        return count
