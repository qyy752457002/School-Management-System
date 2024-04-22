from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_job_appointments_dao import TeacherJobAppointmentsDAO
from models.teacher_job_appointments import TeacherJobAppointments
from views.models.teacher_extend import TeacherJobAppointmentsModel, TeacherJobAppointmentsUpdateModel


@dataclass_inject
class TeacherJobAppointmentsRule(object):
    teacher_job_appointments_dao: TeacherJobAppointmentsDAO

    async def get_teacher_job_appointments_by_teacher_job_appointments_id(self, teacher_job_appointments_id):
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel)
        return teacher_job_appointments

    async def add_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsModel):
        teacher_job_appointments_db = view_model_to_orm_model(teacher_job_appointments, TeacherJobAppointments)
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.add_teacher_job_appointments(
            teacher_job_appointments_db)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel)
        return teacher_job_appointments

    async def delete_teacher_job_appointments(self, teacher_job_appointments_id):
        exists_teacher_job_appointments = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        if not exists_teacher_job_appointments:
            raise Exception(f"编号为的{teacher_job_appointments_id}teacher_job_appointments不存在")
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.delete_teacher_job_appointments(
            exists_teacher_job_appointments)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel,
                                                           exclude=[""])
        return teacher_job_appointments

    async def update_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsUpdateModel):
        exists_teacher_job_appointments_info = await self.teacher_job_appointments_dao.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments.teacher_job_appointments_id)
        if not exists_teacher_job_appointments_info:
            raise Exception(
                f"编号为{teacher_job_appointments.teacher_job_appointments_id}的teacher_job_appointments不存在")
        need_update_list = []
        for key, value in teacher_job_appointments.dict().items():
            if value:
                need_update_list.append(key)
        teacher_job_appointments = await self.teacher_job_appointments_dao.update_teacher_job_appointments(
            teacher_job_appointments, *need_update_list)
        return teacher_job_appointments

    async def get_all_teacher_job_appointments(self, teacher_id):
        teacher_job_appointments_db = await self.teacher_job_appointments_dao.get_all_teacher_job_appointments(
            teacher_id)
        teacher_job_appointments = orm_model_to_view_model(teacher_job_appointments_db, TeacherJobAppointmentsModel,
                                                           exclude=[""])
        return teacher_job_appointments
