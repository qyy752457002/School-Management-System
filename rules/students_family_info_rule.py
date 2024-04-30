from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.students_family_info_dao import StudentsFamilyInfoDao
from daos.students_dao import StudentsDao
from models.students_family_info import StudentFamilyInfo
from views.models.students import StudentsFamilyInfo as StudentsFamilyInfoModel
from business_exceptions.student import StudentFamilyInfoNotFoundError, StudentNotFoundError, \
    StudentFamilyInfoExistsError
from views.models.students import StudentsFamilyInfoCreate


@dataclass_inject
class StudentsFamilyInfoRule(object):
    students_family_info_dao: StudentsFamilyInfoDao
    students_dao: StudentsDao

    async def get_students_family_info_by_id(self, student_family_info_id):
        """
        获取单个学生家庭信息
        """
        students_family_info_db = await self.students_family_info_dao.get_students_family_info_by_id(
            student_family_info_id)
        if not students_family_info_db:
            raise StudentFamilyInfoNotFoundError()
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def add_students_family_info(self, students_family_info: StudentsFamilyInfoCreate):
        """
        新增学生家庭信息
        """
        exits_student = await self.students_dao.get_students_by_id(students_family_info.student_id)
        if not exits_student:
            raise StudentNotFoundError()
        #  去重  根据 姓名  性别  关系
        kdict = {"name": students_family_info.name, "gender":  students_family_info.gender, "relationship":  students_family_info.relationship}
        exist = await self.students_family_info_dao.get_student_family_info_by_param( **kdict)

        # print(exist)

        if exist:
            # print(exist)
            raise StudentFamilyInfoExistsError()

        students_family_info_db = view_model_to_orm_model(students_family_info, StudentFamilyInfo, exclude=[""])
        students_family_info_db = await self.students_family_info_dao.add_students_family_info(students_family_info_db)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def update_students_family_info(self, students_family_info):
        """
        编辑学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(
            students_family_info.student_family_info_id)
        if not exists_students_family_info:
            raise StudentFamilyInfoNotFoundError()
        need_update_list = []
        for key, value in students_family_info.dict().items():
            if value:
                need_update_list.append(key)
        students_family_info = await self.students_family_info_dao.update_students_family_info(students_family_info,
                                                                                               *need_update_list)
        return students_family_info

    async def delete_students_family_info(self, students_family_info_id):
        """
        删除学生家庭信息
        """
        exists_students_family_info = await self.students_family_info_dao.get_students_family_info_by_id(
            students_family_info_id)
        if not exists_students_family_info:
            raise StudentFamilyInfoNotFoundError()
        students_family_info_db = await self.students_family_info_dao.delete_students_family_info(
            exists_students_family_info)
        students_family_info = orm_model_to_view_model(students_family_info_db, StudentsFamilyInfoModel, exclude=[""])
        return students_family_info

    async def get_all_students_family_info(self, student_id):

        exits_student = await self.students_dao.get_students_by_id(student_id)
        if not exits_student:
            raise StudentFamilyInfoNotFoundError()
        student_family_info_db = await self.students_family_info_dao.get_all_students_family_info(student_id)
        student_family_info = []
        for item in student_family_info_db:
            student_family_info.append(orm_model_to_view_model(item, StudentsFamilyInfoModel))
        return student_family_info
