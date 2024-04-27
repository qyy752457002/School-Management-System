from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_qualifications_dao import TeacherQualificationsDAO
from models.teacher_qualifications import TeacherQualifications
from views.models.teacher_extend import TeacherQualificationsModel, TeacherQualificationsUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError, TeacherQualificationsNotFoundError


@dataclass_inject
class TeacherQualificationsRule(object):
    teacher_qualifications_dao: TeacherQualificationsDAO
    teachers_dao: TeachersDao

    async def get_teacher_qualifications_by_teacher_qualifications_id(self, teacher_qualifications_id):
        teacher_qualifications_db = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications_id)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsUpdateModel)
        return teacher_qualifications

    async def add_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_qualifications.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_qualifications_db = view_model_to_orm_model(teacher_qualifications, TeacherQualifications)
        teacher_qualifications_db = await self.teacher_qualifications_dao.add_teacher_qualifications(
            teacher_qualifications_db)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsUpdateModel)
        return teacher_qualifications

    async def delete_teacher_qualifications(self, teacher_qualifications_id):
        exists_teacher_qualifications = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications_id)
        if not exists_teacher_qualifications:
            raise TeacherQualificationsNotFoundError()
        teacher_qualifications_db = await self.teacher_qualifications_dao.delete_teacher_qualifications(
            exists_teacher_qualifications)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsUpdateModel,
                                                         exclude=[""])
        return teacher_qualifications

    async def update_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsUpdateModel):
        exists_teacher_qualifications_info = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications.teacher_qualifications_id)
        if not exists_teacher_qualifications_info:
            raise TeacherQualificationsNotFoundError()
        need_update_list = []
        for key, value in teacher_qualifications.dict().items():
            if value:
                need_update_list.append(key)
        teacher_qualifications = await self.teacher_qualifications_dao.update_teacher_qualifications(
            teacher_qualifications, *need_update_list)
        return teacher_qualifications

    async def get_all_teacher_qualifications(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        teacher_qualifications_db = await self.teacher_qualifications_dao.get_all_teacher_qualifications(
            teacher_id)
        teacher_qualifications = []
        for teacher_qualification in teacher_qualifications_db:
            teacher_qualifications.append(orm_model_to_view_model(teacher_qualification, TeacherQualificationsUpdateModel))
        return teacher_qualifications

