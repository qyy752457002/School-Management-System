from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_learn_experience_dao import TeacherLearnExperienceDAO
from daos.teachers_dao import TeachersDao
from models.teacher_learn_experience import TeacherLearnExperience
from views.models.teacher_extend import TeacherLearnExperienceModel


@dataclass_inject
class TeacherLearnExperienceRule(object):
    teacher_learn_experience_dao: TeacherLearnExperienceDAO
    teachers_dao: TeachersDao

    async def get_teacher_learn_experience_by_teacher_learn_experience_id(self, teacher_learn_experience_id):
        teacher_learn_experience_db = await self.teacher_learn_experience_dao.get_teacher_learn_experience_by_teacher_learn_experience_id(
            teacher_learn_experience_id)
        teacher_learn_experience = orm_model_to_view_model(teacher_learn_experience_db, TeacherLearnExperienceModel)
        return teacher_learn_experience

    async def add_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceModel):
        teacher_learn_experience_db = view_model_to_orm_model(teacher_learn_experience, TeacherLearnExperience)
        teacher_learn_experience_db = await self.teacher_learn_experience_dao.add_teacher_learn_experience(
            teacher_learn_experience_db)
        teacher_learn_experience = orm_model_to_view_model(teacher_learn_experience_db, TeacherLearnExperienceModel)
        return teacher_learn_experience

    async def delete_teacher_learn_experience(self, teacher_learn_experience_id):
        exists_teacher_learn_experience = await self.teacher_learn_experience_dao.get_teacher_learn_experience_by_teacher_learn_experience_id(
            teacher_learn_experience_id)
        print(exists_teacher_learn_experience.is_deleted)
        if not exists_teacher_learn_experience:
            raise Exception(f"编号为的{teacher_learn_experience_id}teacher_learn_experience不存在")
        teacher_learn_experience_db = await self.teacher_learn_experience_dao.delete_teacher_learn_experience(
            exists_teacher_learn_experience)
        teacher_learn_experience = orm_model_to_view_model(teacher_learn_experience_db, TeacherLearnExperienceModel,
                                                           exclude=[""])
        return teacher_learn_experience

    async def update_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceModel):
        exists_teacher_learn_experience_info = await self.teacher_learn_experience_dao.get_teacher_learn_experience_by_teacher_learn_experience_id(
            teacher_learn_experience.teacher_learn_experience_id)
        if not exists_teacher_learn_experience_info:
            raise Exception(
                f"编号为{teacher_learn_experience.teacher_learn_experience_id}的teacher_learn_experience不存在")
        need_update_list = []
        for key, value in teacher_learn_experience.dict().items():
            if value:
                need_update_list.append(key)
        teacher_learn_experience = await self.teacher_learn_experience_dao.update_teacher_learn_experience(
            teacher_learn_experience, *need_update_list)
        return teacher_learn_experience

    async def get_all_teacher_learn_experience(self, teacher_id):
        teacher_learn_experience_db = await self.teacher_learn_experience_dao.get_all_teacher_learn_experience(
            teacher_id)
        teacher_learn_experience = []
        for teacher_learn_experience_db in teacher_learn_experience_db:
            teacher_learn_experience.append(
                orm_model_to_view_model(teacher_learn_experience_db, TeacherLearnExperienceModel, exclude=[""]))
        return teacher_learn_experience
