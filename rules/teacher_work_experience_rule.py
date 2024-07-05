from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_work_experience_dao import TeacherWorkExperienceDAO
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError, TeacherWorkExperienceNotFoundError
from models.teacher_work_experience import TeacherWorkExperience
from views.models.teacher_extend import TeacherWorkExperienceModel, TeacherWorkExperienceUpdateModel
# 雪花id生成器
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from views.common.common_view import convert_snowid_in_model


@dataclass_inject
class TeacherWorkExperienceRule(object):
    teacher_work_experience_dao: TeacherWorkExperienceDAO
    teachers_dao: TeachersDao

    async def get_teacher_work_experience_by_teacher_work_experience_id(self, teacher_work_experience_id):
        teacher_work_experience_db = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        if not teacher_work_experience_db:
            raise TeacherWorkExperienceNotFoundError()
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceUpdateModel)
        # teacher_work_experience = convert_snowid_in_model(teacher_work_experience,
        #                                                   extra_colums=["teacher_work_experience_id", "teacher_id"])
        return teacher_work_experience

    async def add_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_work_experience.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_work_experience_db = view_model_to_orm_model(teacher_work_experience, TeacherWorkExperience)
        teacher_work_experience_db = await self.teacher_work_experience_dao.add_teacher_work_experience(
            teacher_work_experience_db)
        teacher_work_experience_db.teacher_work_experience_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceUpdateModel)
        # teacher_work_experience = convert_snowid_in_model(teacher_work_experience,
        #                                                   extra_colums=["teacher_work_experience_id", "teacher_id"])
        return teacher_work_experience

    async def delete_teacher_work_experience(self, teacher_work_experience_id):
        exists_teacher_work_experience = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        if not exists_teacher_work_experience:
            raise TeacherWorkExperienceNotFoundError()
        teacher_work_experience_db = await self.teacher_work_experience_dao.delete_teacher_work_experience(
            exists_teacher_work_experience)
        teacher_work_experience = orm_model_to_view_model(teacher_work_experience_db, TeacherWorkExperienceModel,
                                                          exclude=[""])
        # teacher_work_experience = convert_snowid_in_model(teacher_work_experience,
        #                                                   extra_colums=["teacher_work_experience_id", "teacher_id"])
        return teacher_work_experience

    async def update_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceUpdateModel):
        exists_teacher_work_experience_info = await self.teacher_work_experience_dao.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience.teacher_work_experience_id)
        if not exists_teacher_work_experience_info:
            raise TeacherWorkExperienceNotFoundError()
        need_update_list = []
        for key, value in teacher_work_experience.dict().items():
            if value:
                need_update_list.append(key)
        teacher_work_experience = await self.teacher_work_experience_dao.update_teacher_work_experience(
            teacher_work_experience, *need_update_list)
        convert_snowid_in_model(teacher_work_experience,
                                extra_colums=["teacher_work_experience_id", "teacher_id"])
        return teacher_work_experience

    async def get_all_teacher_work_experience(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        teacher_work_experience_db = await self.teacher_work_experience_dao.get_all_teacher_work_experience(teacher_id)
        teacher_work_experience = []
        for item in teacher_work_experience_db:
            teacher_work_experience.append(orm_model_to_view_model(item, TeacherWorkExperienceUpdateModel))
        return teacher_work_experience
