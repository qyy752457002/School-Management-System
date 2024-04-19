from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_dao import TeachersDao
from models.teachers import Teacher
from views.models.teachers import Teachers as TeachersModel


@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao

    async def get_teachers_by_id(self, teachers_id):
        exists_teachers= await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise AccountNotFoundError()
        teachers_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
        # 可选 ,
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    # async def add_teachers(self, teachers: TeachersModel):
    #     # exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.id)
    #     # # if exists_teachers:
    #     # #     raise Exception(f"编号为{teachers.id}教师已存在")
    #     teachers_db = Teacher()
    #     teachers_db.teacher_name = teachers.teacher_name
    #     teachers_db.teacher_gender = teachers.teacher_gender
    #     teachers_db.teacher_id_type = teachers.teacher_id_type
    #     teachers_db.teacher_id_number = teachers.teacher_id_number
    #     teachers_db.teacher_date_of_birth = teachers.teacher_date_of_birth
    #     teachers_db.teacher_employer = teachers.teacher_employer
    #     teachers_db.teacher_avatar = teachers.teacher_avatar
    #
    #     teachers_db = await self.teachers_dao.add_teachers(teachers_db)
    #     teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
    #     return teachers
    async def add_teachers(self, teachers: TeachersModel):
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def update_teachers(self, teachers):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise Exception(f"编号为{teachers.id}教师不存在")
        need_update_list = []
        for key, value in teachers.dict().items():
            if value:
                need_update_list.append(key)
        teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return teachers

    async def delete_teachers(self, teachers_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise Exception(f"编号为{teachers_id}教师不存在")
        teachers_db = await self.teachers_dao.delete_teachers(exists_teachers)
        return teachers_db



