from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_job_appointments_dao import TeacherJobAppointmentsDAO
from daos.teachers_dao import TeachersDao
from models.teacher_job_appointments import TeacherJobAppointments
from views.models.teacher_extend import TeacherJobAppointmentsModel, TeacherJobAppointmentsUpdateModel
from business_exceptions.teacher import TeacherNotFoundError, TeacherJobAppointmentsNotFoundError
import json


@dataclass_inject
class TeacherJobAppointmentsRule(object):
    teacher_job_appointments_dao: TeacherJobAppointmentsDAO
    teachers_dao: TeachersDao

    async def get_teacher_job_appointments_by_teacher_job_appointments_id(self, teacher_job_appointments_id):
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db,
                                                           TeacherJobAppointmentsUpdateModel,
                                                           exclude=["concurrent_position"])
        teacher_job_appointments.concurrent_position = json.loads(teacher_job_appointments_db.concurrent_position)
        return teacher_job_appointments

    async def add_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_job_appointments.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        concurrent_positions_json = json.dumps(teacher_job_appointments.concurrent_position)
        teacher_job_appointments_db = view_model_to_orm_model(teacher_job_appointments, TeacherJobAppointments,
                                                              exclude=["concurrent_position"])
        teacher_job_appointments_db.concurrent_position = concurrent_positions_json
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.add_teacher_job_appointments(
            teacher_job_appointments_db)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel,
                                                           exclude=["concurrent_position"])
        teacher_job_appointments.concurrent_position = json.loads(teacher_job_appointments_db.concurrent_position)
        return teacher_job_appointments

    async def delete_teacher_job_appointments(self, teacher_job_appointments_id):
        exists_teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not exists_teacher_job_appointments:
            raise TeacherJobAppointmentsNotFoundError()
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.delete_teacher_job_appointments(
            exists_teacher_job_appointments)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel,
                                                           exclude=["concurrent_position"])
        teacher_job_appointments.concurrent_position = json.loads(teacher_job_appointments_db.concurrent_position)
        return teacher_job_appointments

    async def update_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsUpdateModel):
        exists_teacher_job_appointments_info = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments.teacher_job_appointments_id)
        if not exists_teacher_job_appointments_info:
            raise TeacherJobAppointmentsNotFoundError()
        need_update_list = []
        for key, value in teacher_job_appointments.dict().items():
            if value:
                need_update_list.append(key)
        teacher_job_appointments.concurrent_position = json.dumps(teacher_job_appointments.concurrent_position)
        teacher_job_appointments = await self.teacher_job_appointments_dao.update_teacher_job_appointments(
            teacher_job_appointments, *need_update_list)
        teacher_job_appointments.concurrent_position = json.loads(teacher_job_appointments.concurrent_position)
        return teacher_job_appointments

    async def get_all_teacher_job_appointments(self, teacher_id):
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.get_all_teacher_job_appointments(
            teacher_id)
        if not teacher_job_appointments_db:
            raise TeacherNotFoundError()
        teacher_job_appointments = []
        for teacher_job_appointment in teacher_job_appointments_db:
            item = orm_model_to_view_model(teacher_job_appointment, TeacherJobAppointmentsUpdateModel,
                                           exclude=["concurrent_position"])
            item.concurrent_position = json.loads(teacher_job_appointment.concurrent_position)
            teacher_job_appointments.append(item)
        return teacher_job_appointments

    async def submitting(self, teacher_job_appointments_id):
        teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not teacher_job_appointments:
            raise TeacherJobAppointmentsNotFoundError()
        teacher_job_appointments.approval_status = "submitting"
        return await self.teacher_job_appointments_dao.update_teacher_job_appointments(teacher_job_appointments,
                                                                                       "approval_status")

    async def submitted(self, teacher_job_appointments_id):
        teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not teacher_job_appointments:
            raise TeacherJobAppointmentsNotFoundError()
        teacher_job_appointments.approval_status = "submitted"
        return await self.teacher_job_appointments_dao.update_teacher_job_appointments(teacher_job_appointments,
                                                                                       "approval_status")

    async def approved(self, teacher_job_appointments_id):
        teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not teacher_job_appointments:
            raise TeacherJobAppointmentsNotFoundError()
        teacher_job_appointments.approval_status = "approved"
        return await self.teacher_job_appointments_dao.update_teacher_job_appointments(teacher_job_appointments,
                                                                                       "approval_status")

    async def rejected(self, teacher_job_appointments_id):
        teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not teacher_job_appointments:
            raise TeacherJobAppointmentsNotFoundError()
        teacher_job_appointments.approval_status = "rejected"
        return await self.teacher_job_appointments_dao.update_teacher_job_appointments(teacher_job_appointments,
                                                                                       "approval_status")
