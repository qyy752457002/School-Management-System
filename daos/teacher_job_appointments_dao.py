from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_job_appointments import TeacherJobAppointments
from models.teachers import Teacher


class TeacherJobAppointmentsDAO(DAOBase):

    async def add_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointments):
        session = await self.master_db()
        session.add(teacher_job_appointments)
        await session.commit()
        await session.refresh(teacher_job_appointments)
        return teacher_job_appointments

    async def get_teacher_job_appointments_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherJobAppointments))
        return result.scalar()

    async def delete_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointments):
        session = await self.master_db()
        await session.delete(teacher_job_appointments)
        await session.commit()

    async def get_teacher_job_appointments_by_teacher_job_appointments_id(self, teacher_job_appointments_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherJobAppointments).where(
            TeacherJobAppointments.teacher_job_appointments_id == teacher_job_appointments_id))
        return result.scalar_one_or_none()

    async def query_teacher_job_appointments_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherJobAppointments)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_job_appointments(self, teacher_job_appointments, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_job_appointments, *args)
        query = update(TeacherJobAppointments).where(
            TeacherJobAppointments.teacher_job_appointments_id == teacher_job_appointments.teacher_job_appointments_id).values(
            **update_contents)
        return await self.update(session, query, teacher_job_appointments, update_contents, is_commit=is_commit)

    async def get_all_teacher_job_appointments(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherJobAppointments).join(Teacher,
                                                    TeacherJobAppointments.teacher_id == Teacher.teacher_id).where(
            TeacherJobAppointments.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()



