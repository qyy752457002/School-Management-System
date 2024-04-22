from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_qualifications_dao import TeacherQualificationsDAO
from models.teacher_qualifications import TeacherQualifications
from views.models.teacher_extend import TeacherQualificationsModel, TeacherQualificationsUpdateModel


@dataclass_inject
class TeacherQualificationsRule(object):
    teacher_qualifications_dao: TeacherQualificationsDAO

    async def get_teacher_qualifications_by_teacher_qualifications_id(self, teacher_qualifications_id):
        teacher_qualifications_db = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications_id)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsModel)
        return teacher_qualifications

    async def add_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsModel):
        teacher_qualifications_db = view_model_to_orm_model(teacher_qualifications, TeacherQualifications)
        teacher_qualifications_db = await self.teacher_qualifications_dao.add_teacher_qualifications(
            teacher_qualifications_db)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsModel)
        return teacher_qualifications

    async def delete_teacher_qualifications(self, teacher_qualifications_id):
        exists_teacher_qualifications = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications_id)
        if not exists_teacher_qualifications:
            raise Exception(f"编号为的{teacher_qualifications_id}teacher_qualifications不存在")
        teacher_qualifications_db = await self.teacher_qualifications_dao.delete_teacher_qualifications(
            exists_teacher_qualifications)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsModel,
                                                         exclude=[""])
        return teacher_qualifications

    async def update_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsUpdateModel):
        exists_teacher_qualifications_info = await self.teacher_qualifications_dao.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications.teacher_qualifications_id)
        if not exists_teacher_qualifications_info:
            raise Exception(f"编号为{teacher_qualifications.teacher_qualifications_id}的teacher_qualifications不存在")
        need_update_list = []
        for key, value in teacher_qualifications.dict().items():
            if value:
                need_update_list.append(key)
        teacher_qualifications = await self.teacher_qualifications_dao.update_teacher_qualifications(
            teacher_qualifications, *need_update_list)
        return teacher_qualifications

    async def get_all_teacher_qualifications(self, teacher_id):
        teacher_qualifications_db = await self.teacher_qualifications_dao.get_all_teacher_qualifications(teacher_id)
        teacher_qualifications = orm_model_to_view_model(teacher_qualifications_db, TeacherQualificationsModel,
                                                         exclude=[""])
        return teacher_qualifications
