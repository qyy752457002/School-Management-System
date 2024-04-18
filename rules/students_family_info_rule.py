from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.students_family_info_dao import StudentsFamilyInfoDao
from models.students_family_info import StudentFamilyInfo
from views.models.students import StudentsFamilyInfo as StudentsFamilyInfoModel

@dataclass_inject
class StudentsFamilyInfoRule(object):
    students_family_info_dao: StudentsFamilyInfoDao
    async def get_students_family_info_by_id(self, students_id):
        """
        获取单个学生家庭信息
        """
        students_family_info_db = await self.students_family_info_dao.get_students_family_info_by_id(students_id)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def add_students_family_info(self, students_family_info: StudentsFamilyInfoModel):
        """
        新增学生家庭信息
        """
        students_family_info_db = view_model_to_orm_model(students_family_info, StudentFamilyInfo, exclude=[""])
        students_family_info_db = await self.students_family_info_dao.add_students_family_info(students_family_info_db)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def update_students_family_info(self, students_family_info):
        """
        编辑学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(students_family_info.student_id)
        if not exists_students_family_info:
            raise Exception(f"编号为{students_family_info.student_id}学生不存在")
        need_update_list = []
        for key, value in students_family_info.dict().items():
            if value:
                need_update_list.append(key)
        students_family_info = await self.students_family_info_dao.update_students_family_info(students_family_info, *need_update_list)
        return students_family_info

    async def delete_students_family_info(self, students_id):
        """
        删除学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(students_id)
        if not exists_students_family_info:
            raise Exception(f"编号为{students_id}学生不存在")
        students_family_info_db = await self.students_family_info_dao.delete_students_family_info(exists_students_family_info)
        return students_family_info_db
