from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError
from daos.educational_teaching_dao import EducationalTeachingDAO
from daos.teachers_dao import TeachersDao
from models.educational_teaching import EducationalTeaching
from views.models.teacher_extend import EducationalTeachingModel, EducationalTeachingUpdateModel


@dataclass_inject
class EducationalTeachingRule(object):
    educational_teaching_dao: EducationalTeachingDAO
    teachers_dao: TeachersDao

    async def get_educational_teaching_by_educational_teaching_id(self, educational_teaching_id):
        educational_teaching_db = await self.educational_teaching_dao.get_educational_teaching_by_educational_teaching_id(
            educational_teaching_id)
        educational_teaching = orm_model_to_view_model(educational_teaching_db, EducationalTeachingUpdateModel)
        return educational_teaching

    async def add_educational_teaching(self, educational_teaching: EducationalTeachingModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(educational_teaching.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        educational_teaching_db = view_model_to_orm_model(educational_teaching, EducationalTeaching)
        educational_teaching_db.educational_teaching_id = SnowflakeIdGenerator(1, 1).generate_id()
        educational_teaching_db = await self.educational_teaching_dao.add_educational_teaching(educational_teaching_db)
        educational_teaching = orm_model_to_view_model(educational_teaching_db, EducationalTeachingUpdateModel)
        return educational_teaching

    async def delete_educational_teaching(self, educational_teaching_id):
        exists_educational_teaching = await self.educational_teaching_dao.get_educational_teaching_by_educational_teaching_id(
            educational_teaching_id)
        if not exists_educational_teaching:
            raise TeacherInfoNotFoundError()
        educational_teaching_db = await self.educational_teaching_dao.delete_educational_teaching(
            exists_educational_teaching)
        educational_teaching = orm_model_to_view_model(educational_teaching_db, EducationalTeachingUpdateModel,
                                                       exclude=[""])
        return educational_teaching

    async def update_educational_teaching(self, educational_teaching: EducationalTeachingUpdateModel):
        exists_educational_teaching_info = await self.educational_teaching_dao.get_educational_teaching_by_educational_teaching_id(
            educational_teaching.educational_teaching_id)
        if not exists_educational_teaching_info:
            raise TeacherInfoNotFoundError()
        need_update_list = []
        for key, value in educational_teaching.dict().items():
            if value:
                need_update_list.append(key)
        educational_teaching = await self.educational_teaching_dao.update_educational_teaching(educational_teaching,
                                                                                               *need_update_list)
        return educational_teaching

    async def get_all_educational_teaching(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        educational_teaching_db = await self.educational_teaching_dao.get_all_educational_teaching(teacher_id)
        educational_teaching = []
        for i in educational_teaching_db:
            educational_teaching.append(orm_model_to_view_model(i, EducationalTeachingUpdateModel, exclude=[""]))
        return educational_teaching
