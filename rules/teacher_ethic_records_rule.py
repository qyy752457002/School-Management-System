from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, TeacherEthicRecordsNotFoundError
from daos.teacher_ethic_records_dao import TeacherEthicRecordsDAO
from daos.teachers_dao import TeachersDao
from models.teacher_ethic_records import TeacherEthicRecords
from views.models.teacher_extend import TeacherEthicRecordsModel, TeacherEthicRecordsUpdateModel


@dataclass_inject
class TeacherEthicRecordsRule(object):
    teacher_ethic_records_dao: TeacherEthicRecordsDAO
    teachers_dao: TeachersDao

    async def get_teacher_ethic_records_by_teacher_ethic_records_id(self, teacher_ethic_records_id):
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsUpdateModel)
        return teacher_ethic_records

    async def add_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_ethic_records.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_ethic_records_db = view_model_to_orm_model(teacher_ethic_records, TeacherEthicRecords)
        teacher_ethic_records_db.teacher_ethic_records_id = SnowflakeIdGenerator(1,1).generate_id()
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.add_teacher_ethic_records(
            teacher_ethic_records_db)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsUpdateModel)
        return teacher_ethic_records

    async def delete_teacher_ethic_records(self, teacher_ethic_records_id):
        exists_teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not exists_teacher_ethic_records:
            raise TeacherEthicRecordsNotFoundError()
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.delete_teacher_ethic_records(
            exists_teacher_ethic_records)
        teacher_ethic_records = orm_model_to_view_model(teacher_ethic_records_db, TeacherEthicRecordsUpdateModel,
                                                        exclude=[""])
        return teacher_ethic_records

    async def update_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsUpdateModel):
        exists_teacher_ethic_records_info = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records.teacher_ethic_records_id)
        if not exists_teacher_ethic_records_info:
            raise TeacherEthicRecordsNotFoundError()
        need_update_list = []
        for key, value in teacher_ethic_records.dict().items():
            if value:
                need_update_list.append(key)
        teacher_ethic_records = await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                                  *need_update_list)
        return teacher_ethic_records

    async def get_all_teacher_ethic_records(self, teacher_id,ethic_type):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        teacher_ethic_records_db = await self.teacher_ethic_records_dao.get_all_teacher_ethic_records(teacher_id,ethic_type)
        teacher_ethic_records = []
        for teacher_ethic_record in teacher_ethic_records_db:
            teacher_ethic_records.append(orm_model_to_view_model(teacher_ethic_record, TeacherEthicRecordsUpdateModel,
                                                                 exclude=[""]))
        return teacher_ethic_records

    async def submitting(self, teacher_ethic_records_id):
        teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not teacher_ethic_records:
            raise TeacherEthicRecordsNotFoundError()
        teacher_ethic_records.approval_status = "submitting"
        return await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                 "approval_status")

    async def submitted(self, teacher_ethic_records_id):
        teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not teacher_ethic_records:
            raise TeacherEthicRecordsNotFoundError()
        teacher_ethic_records.approval_status = "submitted"
        return await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                 "approval_status")

    async def approved(self, teacher_ethic_records_id):
        teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not teacher_ethic_records:
            raise TeacherEthicRecordsNotFoundError()
        teacher_ethic_records.approval_status = "approved"
        return await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                 "approval_status")

    async def rejected(self, teacher_ethic_records_id):
        teacher_ethic_records = await self.teacher_ethic_records_dao.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        if not teacher_ethic_records:
            raise TeacherEthicRecordsNotFoundError()
        teacher_ethic_records.approval_status = "rejected"
        return await self.teacher_ethic_records_dao.update_teacher_ethic_records(teacher_ethic_records,
                                                                                 "approval_status")
