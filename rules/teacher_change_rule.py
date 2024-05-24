from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_change_dao import TeacherChangeDAO
from models.teacher_change import TeacherChange
from views.models.teacher_extend import TeacherChangeModel,TeacherChangeUpdateModel


@dataclass_inject
class TeacherChangeRule(object):
    teacher_change_dao: TeacherChangeDAO

    async def get_teacher_change_by_teacher_change_id(self, teacher_change_id):
        teacher_change_db = await self.teacher_change_dao.get_teacher_change_by_teacher_change_id(teacher_change_id)
        teacher_change = orm_model_to_view_model(teacher_change_db, TeacherChangeModel)
        return teacher_change
    async def add_teacher_change(self, teacher_change:TeacherChangeModel):
        teacher_change_db = view_model_to_orm_model(teacher_change, TeacherChange)
        teacher_change_db = await self.teacher_change_dao.add_teacher_change(teacher_change_db)
        teacher_change = orm_model_to_view_model(teacher_change_db, TeacherChangeModel)
        return teacher_change
    async def delete_teacher_change(self, teacher_change_id):
        exists_teacher_change = await self.teacher_change_dao.get_teacher_change_by_teacher_change_id(teacher_change_id)
        if not exists_teacher_change:
            raise Exception(f"编号为的{teacher_change_id}teacher_change不存在")
        teacher_change_db = await self.teacher_change_dao.delete_teacher_change(exists_teacher_change)
        teacher_change = orm_model_to_view_model(teacher_change_db, TeacherChangeModel, exclude=[""])
        return teacher_change
    async def update_teacher_change(self, teacher_change:TeacherChangeUpdateModel):
        exists_teacher_change_info = await self.teacher_change_dao.get_teacher_change_by_teacher_change_id(teacher_change.teacher_change_id)
        if not exists_teacher_change_info:
            raise Exception(f"编号为{teacher_change.teacher_change_id}的teacher_change不存在")
        need_update_list = []
        for key, value in teacher_change.dict().items():
            if value:
                need_update_list.append(key)
        teacher_change = await self.teacher_change_dao.update_teacher_change(teacher_change, *need_update_list)
        return teacher_change
    async def get_all_teacher_change(self, teacher_id):
          teacher_change_db = await self.teacher_change_dao.get_all_teacher_change(teacher_id)
#          teacher_change = orm_model_to_view_model(teacher_change_db, TeacherChangeModel, exclude=[""])
          teacher_change=[]
          for item in teacher_change_db:
              teacher_change.append(orm_model_to_view_model(item, TeacherChangeModel))
          return teacher_change_db
