from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, TeacherProfessionalTitleNotFoundError
from daos.teacher_professional_titles_dao import TeacherProfessionalTitlesDAO
from daos.teachers_dao import TeachersDao
from models.teacher_professional_titles import TeacherProfessionalTitles
from views.models.teacher_extend import TeacherProfessionalTitlesModel, TeacherProfessionalTitlesUpdateModel


@dataclass_inject
class TeacherProfessionalTitlesRule(object):
    teacher_professional_titles_dao: TeacherProfessionalTitlesDAO
    teachers_dao: TeachersDao

    async def get_teacher_professional_titles_by_teacher_professional_titles_id(self, teacher_professional_titles_id):
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesUpdateModel)
        return teacher_professional_titles

    async def add_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitlesModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_professional_titles.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_professional_titles_db = view_model_to_orm_model(teacher_professional_titles, TeacherProfessionalTitles)
        teacher_professional_titles_db.teacher_professional_titles_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.add_teacher_professional_titles(
            teacher_professional_titles_db)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesUpdateModel)
        return teacher_professional_titles

    async def delete_teacher_professional_titles(self, teacher_professional_titles_id):
        exists_teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not exists_teacher_professional_titles:
            raise TeacherProfessionalTitleNotFoundError()
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.delete_teacher_professional_titles(
            exists_teacher_professional_titles)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesUpdateModel, exclude=[""])
        return teacher_professional_titles

    async def update_teacher_professional_titles(self,
                                                 teacher_professional_titles: TeacherProfessionalTitlesUpdateModel):
        exists_teacher_professional_titles_info = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles.teacher_professional_titles_id)
        if not exists_teacher_professional_titles_info:
            raise TeacherProfessionalTitleNotFoundError()
        need_update_list = []
        for key, value in teacher_professional_titles.dict().items():
            if value:
                need_update_list.append(key)
        teacher_professional_titles = await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles, *need_update_list)
        return teacher_professional_titles

    async def get_all_teacher_professional_titles(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.get_all_teacher_professional_titles(
            teacher_id)
        teacher_professional_titles = []
        for teacher_professional_title in teacher_professional_titles_db:
            teacher_professional_titles.append(
                orm_model_to_view_model(teacher_professional_title, TeacherProfessionalTitlesUpdateModel))
        return teacher_professional_titles

    async def submitting(self, teacher_professional_titles_id):
        teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not teacher_professional_titles:
            raise TeacherProfessionalTitleNotFoundError()
        teacher_professional_titles.approval_status = "submitting"
        return await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles,
            "approval_status")

    async def submitted(self, teacher_professional_titles_id):
        teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not teacher_professional_titles:
            raise TeacherProfessionalTitleNotFoundError()
        teacher_professional_titles.approval_status = "submitted"
        return await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles,
            "approval_status")

    async def approved(self, teacher_professional_titles_id):
        teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not teacher_professional_titles:
            raise TeacherProfessionalTitleNotFoundError()
        teacher_professional_titles.approval_status = "approved"
        return await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles,
            "approval_status")

    async def rejected(self, teacher_professional_titles_id):
        teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not teacher_professional_titles:
            raise TeacherProfessionalTitleNotFoundError()
        teacher_professional_titles.approval_status = "rejected"
        return await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles,
            "approval_status")
