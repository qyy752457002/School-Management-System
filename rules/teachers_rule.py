from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers import Teacher
from views.models.teachers import Teachers as TeachersModel
from views.models.teachers import TeachersCreatModel

import hashlib

import shortuuid
def hash_password(password):
    salt = shortuuid.uuid()
    password = password + "mini_framework" + "web_test" + "123456"
    password = salt + "|" + password
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return salt + "|" + sha256.hexdigest()

@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao
    teachers_info_dao: TeachersInfoDao

    async def get_teachers_by_id(self, teachers_id):
        teacher_db= await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teacher_db:
            raise Exception(f"编号为{teachers_id}教师不存在")
        # 可选 ,
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        return teachers

    # async def get_teachers_by_username(self, username):
    #     teacher_db = await self.teachers_dao.get_teachers_by_username(username)
    #     teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
    #     return teachers


    async def add_teachers(self, teachers: TeachersCreatModel):
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def update_teachers(self, teachers):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise Exception(f"编号为{teachers.teacher_id}教师不存在")
        need_update_list = []
        for key, value in teachers.dict().items():
            if value:
                need_update_list.append(key)
        teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return teachers

    async def delete_teachers(self, teachers_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        print(exists_teachers.is_deleted)
        if not exists_teachers:
            raise Exception(f"编号为{teachers_id}教师不存在")
        teachers_db = await self.teachers_dao.delete_teachers(exists_teachers)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def get_all_teachers(self):
        teachers_db = await self.teachers_dao.get_all_teachers()
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def get_teachers_count(self):
        teachers_count = await self.teachers_dao.get_teachers_count()
        return teachers_count

    # async def query_teacher_with_page(self, username, page_request: PageRequest):
    #     paging = await self.teachers_dao.query_teacher_with_page(username, page_request)
    #     teachers = orm_model_to_view_model(paging.items, TeachersModel, exclude=["hash_password"])
    #     return PaginatedResponse(items=teachers, total=paging.total, page=page_request.page, page_size=page_request.page_size)


