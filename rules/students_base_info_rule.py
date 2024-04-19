from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.students_base_info_dao import StudentsBaseInfoDao
from models.students_base_info import StudentBaseInfo
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel


@dataclass_inject
class StudentsBaseInfoRule(object):
    students_base_info_dao: StudentsBaseInfoDao

    async def get_students_base_info_by_id(self, students_id):
        """
        获取单个学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_students_base_info_by_id(students_id)
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsKeyinfoModel, exclude=[""])
        return students_base_info

    async def add_students_base_info(self, students_base_info: StudentsKeyinfoModel):
        """
        新增学生基本信息
        """
        students_base_info_db = view_model_to_orm_model(students_base_info, StudentBaseInfo, exclude=[""])
        students_base_info_db = await self.students_base_info_dao.add_students_base_info(students_base_info_db)
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsKeyinfoModel, exclude=[""])
        return students_base_info

    async def update_students_base_info(self, students_base_info):
        """
        编辑学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_id(
            students_base_info.student_id)
        if not exists_students_base_info:
            raise Exception(f"编号为{students_base_info.student_id}学生不存在")
        need_update_list = []
        for key, value in students_base_info.dict().items():
            if value:
                need_update_list.append(key)
        students_base_info = await self.students_base_info_dao.update_students_base_info(students_base_info,
                                                                                         *need_update_list)
        return students_base_info

    async def delete_students_base_info(self, students_id):
        """
        删除学生基本信息
        """
        exists_students_base_info = await self.students_base_info_dao.get_students_base_info_by_id(students_id)
        if not exists_students_base_info:
            raise Exception(f"编号为{students_id}学生不存在")
        students_base_info_db = await self.students_base_info_dao.delete_students_base_info(exists_students_base_info)
        return students_base_info_db

    async def query_students_base_info_with_page(self, page_request: PageRequest, condition) -> PaginatedResponse:
        """
        分页查询
        """
        paging = await self.students_base_info_dao.query_students_with_page(page_request, condition)
        paging_result = PaginatedResponse.from_paging(paging, StudentsKeyinfoModel)
        return paging_result

    async def get_all_students_base_info(self):
        """
        获取所有学生信息
        """
        students_base_info_db = await self.students_base_info_dao.get_all_students_base_info()
        students_base_info = orm_model_to_view_model(students_base_info_db, StudentsKeyinfoModel, exclude=[""])
        return students_base_info

    async def get_students_base_info_count(self):
        """
        获取学生信息数量
        """
        count = await self.students_base_info_dao.get_student_base_info_count()
        return count
