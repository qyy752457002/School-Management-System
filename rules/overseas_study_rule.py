from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.overseas_study_dao import OverseasStudyDAO
from models.overseas_study import OverseasStudy
from views.models.teacher_extend import OverseasStudyModel,OverseasStudyUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError



@dataclass_inject
class OverseasStudyRule(object):
    overseas_study_dao: OverseasStudyDAO
    teachers_dao: TeachersDao

    async def get_overseas_study_by_overseas_study_id(self, overseas_study_id):
        overseas_study_db = await self.overseas_study_dao.get_overseas_study_by_overseas_study_id(overseas_study_id)
        overseas_study = orm_model_to_view_model(overseas_study_db, OverseasStudyModel)
        return overseas_study
    async def add_overseas_study(self, overseas_study:OverseasStudyModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(overseas_study.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        overseas_study_db = view_model_to_orm_model(overseas_study, OverseasStudy)
        overseas_study_db = await self.overseas_study_dao.add_overseas_study(overseas_study_db)
        overseas_study = orm_model_to_view_model(overseas_study_db, OverseasStudyModel)
        return overseas_study
    async def delete_overseas_study(self, overseas_study_id):
        exists_overseas_study = await self.overseas_study_dao.get_overseas_study_by_overseas_study_id(overseas_study_id)
        if not exists_overseas_study:
            raise Exception(f"编号为的{overseas_study_id}overseas_study不存在")
        overseas_study_db = await self.overseas_study_dao.delete_overseas_study(exists_overseas_study)
        overseas_study = orm_model_to_view_model(overseas_study_db, OverseasStudyModel, exclude=[""])
        return overseas_study
    async def update_overseas_study(self, overseas_study:OverseasStudyUpdateModel):
        exists_overseas_study_info = await self.overseas_study_dao.get_overseas_study_by_overseas_study_id(overseas_study.overseas_study_id)
        if not exists_overseas_study_info:
            raise Exception(f"编号为{overseas_study.overseas_study_id}的overseas_study不存在")
        need_update_list = []
        for key, value in overseas_study.dict().items():
            if value:
                need_update_list.append(key)
        overseas_study = await self.overseas_study_dao.update_overseas_study(overseas_study, *need_update_list)
        return overseas_study
    async def get_all_overseas_study(self, teacher_id):
          overseas_study_db = await self.overseas_study_dao.get_all_overseas_study(teacher_id)
#          overseas_study = orm_model_to_view_model(overseas_study_db, OverseasStudyModel, exclude=[""])
          overseas_study=[]
          for item in overseas_study_db:
              overseas_study.append(orm_model_to_view_model(item, OverseasStudyModel))
          return overseas_study_db
