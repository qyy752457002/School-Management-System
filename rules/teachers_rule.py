from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.common import IdCardError
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers import Teacher
from views.common.common_view import check_id_number
from views.models.teachers import Teachers as TeachersModel
from views.models.teachers import TeachersCreatModel, TeacherInfoSaveModel
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from views.models.teacher_transaction import TeacherAddModel, TeacherAddReModel


@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao
    teachers_info_dao: TeachersInfoDao

    async def get_teachers_by_id(self, teachers_id):
        teacher_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teacher_db:
            raise TeacherNotFoundError()
        # 可选 ,
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        return teachers

    # async def get_teachers_by_username(self, username):
    #     teacher_db = await self.teachers_dao.get_teachers_by_username(username)
    #     teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
    #     return teachers

    async def add_teachers(self, teachers: TeachersCreatModel):
        teacher_id_number = teachers.teacher_id_number
        teacher_id_type = teachers.teacher_id_type
        teacher_name = teachers.teacher_name
        teacher_gender = teachers.teacher_gender
        length = await self.teachers_info_dao.get_teachers_info_by_prams(teacher_id_number, teacher_id_type,
                                                                         teacher_name, teacher_gender)
        if length > 0:
            raise TeacherExistsError()
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def add_transfer_teachers(self, teachers: TeacherAddModel):
        """
        系统外调入系统内时使用，增加老师
        """
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeacherAddReModel, exclude=[""])
        return teachers

    async def update_teachers(self, teachers):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        need_update_list = []
        for key, value in teachers.dict().items():
            if value:
                need_update_list.append(key)
        teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return teachers

    async def delete_teachers(self, teachers_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
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

    async def submitting(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "submitting"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def submitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "submitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def approved(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "approved"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def rejected(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "rejected"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def recall(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_approval_status == "submitted":
            teachers.teacher_approval_status = "submitting"
        else:
            raise Exception("只有待审核的教师信息才能撤回")
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def teacher_active(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "active":
            teachers.teacher_sub_status = "active"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")
