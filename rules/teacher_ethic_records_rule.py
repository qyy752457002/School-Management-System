from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_ethic_records_dao import TeacherEthicRecordsDAO
from models.teacher_ethic_records import TeacherEthicRecords
from views.models.teacher_extend import TeacherEthicRecordsModel, TeacherEthicRecordsUpdateModel


@dataclass_inject
class TeacherEthicRecordsRule(object):
    teacher_ethic_records_dao: TeacherEthicRecordsDAO

    async def get_teacher_ethic_records_by_teacher_ethic_records_id(self, teacher_ethic_records_id):
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsModel)
        return teacher_ethic_records

    async def add_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsModel):
        teacher_ethic_records_db = view_model_to_orm_model(teacher_ethic_records, TeacherEthicRecords)
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.add_teacher_ethic_records(
            teacher_ethic_records_db)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsModel)
        return teacher_ethic_records

    async def delete_teacher_ethic_records(self, teacher_ethic_records_id):
        exists_teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not exists_teacher_ethic_records:
            raise Exception(f"编号为的{teacher_ethic_records_id}teacher_ethic_records不存在")
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.delete_teacher_ethic_records(
            exists_teacher_ethic_records)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsModel,
                                                        exclude=[""])
        return teacher_ethic_records

    async def update_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsUpdateModel):
        exists_teacher_ethic_records_info = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records.teacher_ethic_records_id)
        if not exists_teacher_ethic_records_info:
            raise Exception(f"编号为{teacher_ethic_records.teacher_ethic_records_id}的teacher_ethic_records不存在")
        need_update_list = []
        for key, value in teacher_ethic_records.dict().items():
            if value:
                need_update_list.append(key)
        teacher_ethic_records = await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                                  *need_update_list)
        return teacher_ethic_records

    async def get_all_teacher_ethic_records(self, teacher_id):
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.get_all_teacher_ethic_records(teacher_id)
        teacher_ethic_records = []
        for teacher_ethic_record in teacher_ethic_records_db:
            teacher_ethic_records.append(orm_model_to_view_model(teacher_ethic_record, TeacherEthicRecordsModel,
                                                                 exclude=[""]))
        return teacher_ethic_records
