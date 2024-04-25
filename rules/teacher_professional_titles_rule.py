from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_professional_titles_dao import TeacherProfessionalTitlesDAO
from models.teacher_professional_titles import TeacherProfessionalTitles
from views.models.teacher_extend import TeacherProfessionalTitlesModel, TeacherProfessionalTitlesUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError


@dataclass_inject
class TeacherProfessionalTitlesRule(object):
    teacher_professional_titles_dao: TeacherProfessionalTitlesDAO
    teachers_dao: TeachersDao

    async def get_teacher_professional_titles_by_teacher_professional_titles_id(self, teacher_professional_titles_id):
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesModel)
        return teacher_professional_titles

    async def add_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitlesModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_professional_titles.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_professional_titles_db = view_model_to_orm_model(teacher_professional_titles, TeacherProfessionalTitles)
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.add_teacher_professional_titles(
            teacher_professional_titles_db)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesModel)
        return teacher_professional_titles

    async def delete_teacher_professional_titles(self, teacher_professional_titles_id):
        exists_teacher_professional_titles = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        if not exists_teacher_professional_titles:
            raise Exception(f"编号为的{teacher_professional_titles_id}teacher_professional_titles不存在")
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.delete_teacher_professional_titles(
            exists_teacher_professional_titles)
        teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
                                                              TeacherProfessionalTitlesModel, exclude=[""])
        return teacher_professional_titles

    async def update_teacher_professional_titles(self,
                                                 teacher_professional_titles: TeacherProfessionalTitlesUpdateModel):
        exists_teacher_professional_titles_info = await self.teacher_professional_titles_dao.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles.teacher_professional_titles_id)
        if not exists_teacher_professional_titles_info:
            raise Exception(
                f"编号为{teacher_professional_titles.teacher_professional_titles_id}的teacher_professional_titles不存在")
        need_update_list = []
        for key, value in teacher_professional_titles.dict().items():
            if value:
                need_update_list.append(key)
        teacher_professional_titles = await self.teacher_professional_titles_dao.update_teacher_professional_titles(
            teacher_professional_titles, *need_update_list)
        return teacher_professional_titles

    async def get_all_teacher_professional_titles(self, teacher_id):
        teacher_professional_titles_db = await self.teacher_professional_titles_dao.get_all_teacher_professional_titles(
            teacher_id)
        # teacher_professional_titles = orm_model_to_view_model(teacher_professional_titles_db,
        #                                                       TeacherProfessionalTitlesModel, exclude=[""])
        return teacher_professional_titles_db
