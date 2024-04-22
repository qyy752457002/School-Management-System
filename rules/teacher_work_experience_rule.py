from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_work_experience_dao import TeacherWorkExperienceDAO
from models.teacher_work_experience import TeacherWorkExperience
from views.models.teacher_extend import TeacherWorkExperienceModel, TeacherWorkExperienceUpdateModel


@dataclass_inject
class TeacherWorkExperienceRule(object):
    teacher_work_experience_dao: TeacherWorkExperienceDAO

    async def get_teacher_work_experience_by_teacher_work_experience_id(self, teacher_work_experience_id):
        teacher_work_experience_db = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceModel)
        return teacher_work_experience

    async def add_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceModel):
        teacher_work_experience_db = view_model_to_orm_model(teacher_work_experience, TeacherWorkExperience)
        teacher_work_experience_db = await self.teacher_work_experience_dao.add_teacher_work_experience(
            teacher_work_experience_db)
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceModel)
        return teacher_work_experience

    async def delete_teacher_work_experience(self, teacher_work_experience_id):
        exists_teacher_work_experience = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        if not exists_teacher_work_experience:
            raise Exception(f"编号为的{teacher_work_experience_id}teacher_work_experience不存在")
        teacher_work_experience_db = await self.teacher_work_experience_dao.delete_teacher_work_experience(
            exists_teacher_work_experience)
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceModel,
                                                          exclude=[""])
        return teacher_work_experience

    async def update_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceUpdateModel):
        exists_teacher_work_experience_info = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience.teacher_work_experience_id)
        if not exists_teacher_work_experience_info:
            raise Exception(
                f"编号为{teacher_work_experience.teacher_work_experience_id}的teacher_work_experience不存在")
        need_update_list = []
        for key, value in teacher_work_experience.dict().items():
            if value:
                need_update_list.append(key)
        teacher_work_experience = await self.teacher_work_experience_dao.update_teacher_work_experience(
            teacher_work_experience, *need_update_list)
        return teacher_work_experience

    async def get_all_teacher_work_experience(self, teacher_id):
        teacher_work_experience_db = await self.teacher_work_experience_dao.get_all_teacher_work_experience(teacher_id)
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceModel,
                                                          exclude=[""])
        return teacher_work_experience
