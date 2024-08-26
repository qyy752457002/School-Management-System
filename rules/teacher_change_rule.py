from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from daos.teacher_change_dao import TeacherChangeLogDAO
from drop.teacher_change_detail import TeacherChangeDetail
from drop.teacher_change_log import TeacherChangeLog
from views.models.teacher_change import TeacherChangeLogModel, TeacherChangeLogReModel, TeacherChangeDetailReModel, \
    TeacherChangeDetailModel


@dataclass_inject
class TeacherChangeRule(object):
    teacher_change_dao: TeacherChangeLogDAO

    async def get_teacher_change_detail_by_teacher_id(self, teacher_id, teacher_change_id):
        teacher_change_db = await self.teacher_change_dao.get_teacher_change_detail_by_teacher_id(teacher_id,
                                                                                                  teacher_change_id)
        teacher_change = []
        for item in teacher_change_db:
            teacher_change.append(orm_model_to_view_model(item, TeacherChangeDetailReModel))

        return teacher_change

    async def add_teacher_change(self, teacher_change_log: TeacherChangeLogModel):
        teacher_change_db = view_model_to_orm_model(teacher_change_log, TeacherChangeLog)
        teacher_change_db = await self.teacher_change_dao.add_teacher_change(teacher_change_db)
        teacher_change = orm_model_to_view_model(teacher_change_db, TeacherChangeLogReModel)
        return teacher_change

    async def add_teacher_change_detail(self, teacher_change_detail: TeacherChangeDetailModel):
        teacher_change_detail_db = view_model_to_orm_model(teacher_change_detail, TeacherChangeDetail)
        teacher_change_detail_db = await self.teacher_change_dao.add_teacher_change_detail(teacher_change_detail_db)
        teacher_change_detail = orm_model_to_view_model(teacher_change_detail_db, TeacherChangeDetailReModel)
        return teacher_change_detail

    async def get_all_teacher_change(self, teacher_id):
        teacher_change_db = await self.teacher_change_dao.get_all_teacher_change(teacher_id)
        teacher_change = []
        for item in teacher_change_db:
            teacher_change.append(orm_model_to_view_model(item, TeacherChangeLogReModel))
        return teacher_change_db

    async def teacher_change_detail(self, old_model, new_model, teacher_change_id, change_module):
        changes = []
        old_dic = old_model.dict()
        teacher_id = old_dic.get("teacher_id")
        new_dic = new_model.dict()
        for field, old_value in old_dic.items():
            new_value = new_dic.get(field)
            if old_value != new_value:
                changes.append({
                    "teacher_change_id": teacher_change_id,
                    "teacher_id": teacher_id,
                    "change_module": change_module,
                    "changed_field": field,
                    "before_change": old_value,
                    "after_change": new_value
                })
        teacher_change_detail_list=[TeacherChangeDetailModel(**change) for change in changes]
        for item in teacher_change_detail_list:
            await self.add_teacher_change_detail(item)



