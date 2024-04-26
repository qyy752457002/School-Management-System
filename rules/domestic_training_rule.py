from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.domestic_training_dao import DomesticTrainingDAO
from models.domestic_training import DomesticTraining
from views.models.teacher_extend import DomesticTrainingModel, DomesticTrainingUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError,DomesticTrainingNotFoundError


@dataclass_inject
class DomesticTrainingRule(object):
    domestic_training_dao: DomesticTrainingDAO
    teachers_dao: TeachersDao

    async def get_domestic_training_by_domestic_training_id(self, domestic_training_id):
        domestic_training_db = await self.domestic_training_dao.get_domestic_training_by_domestic_training_id(
            domestic_training_id)
        domestic_training = orm_model_to_view_model(domestic_training_db, DomesticTrainingUpdateModel)
        return domestic_training

    async def add_domestic_training(self, domestic_training: DomesticTrainingModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(domestic_training.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        domestic_training_db = view_model_to_orm_model(domestic_training, DomesticTraining)
        domestic_training_db = await self.domestic_training_dao.add_domestic_training(domestic_training_db)
        domestic_training = orm_model_to_view_model(domestic_training_db, DomesticTrainingUpdateModel)
        return domestic_training

    async def delete_domestic_training(self, domestic_training_id):
        exists_domestic_training = await self.domestic_training_dao.get_domestic_training_by_domestic_training_id(
            domestic_training_id)
        if not exists_domestic_training:
            raise DomesticTrainingNotFoundError()
        domestic_training_db = await self.domestic_training_dao.delete_domestic_training(exists_domestic_training)
        domestic_training = orm_model_to_view_model(domestic_training_db, DomesticTrainingModel, exclude=[""])
        return domestic_training

    async def update_domestic_training(self, domestic_training: DomesticTrainingUpdateModel):
        exists_domestic_training_info = await self.domestic_training_dao.get_domestic_training_by_domestic_training_id(
            domestic_training.domestic_training_id)
        if not exists_domestic_training_info:
            raise DomesticTrainingNotFoundError()
        need_update_list = []
        for key, value in domestic_training.dict().items():
            if value:
                need_update_list.append(key)
        domestic_training = await self.domestic_training_dao.update_domestic_training(domestic_training,
                                                                                      *need_update_list)
        return domestic_training

    async def get_all_domestic_training(self, teacher_id):
        domestic_training_db = await self.domestic_training_dao.get_all_domestic_training(teacher_id)
        if not domestic_training_db:
            raise DomesticTrainingNotFoundError()
        domestic_training = []
        for item in domestic_training_db:
            domestic_training.append(orm_model_to_view_model(item, DomesticTrainingUpdateModel))
        return domestic_training_db
