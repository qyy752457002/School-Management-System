from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_job_appointments import TeacherJobAppointments


class TeacherJobAppointmentsDAO(DAOBase):

	async def add_teacherjobappointments(self, teacherjobappointments: TeacherJobAppointments):
		session = await self.master_db()
		session.add(teacherjobappointments)
		await session.commit()
		await session.refresh(teacherjobappointments)
		return teacherjobappointments

	async def get_teacherjobappointments_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherJobAppointments))
		return result.scalar()

	async def delete_teacherjobappointments(self, teacherjobappointments: TeacherJobAppointments):
		session = await self.master_db()
		await session.delete(teacherjobappointments)
		await session.commit()

	async def get_teacherjobappointments_by_teacher_job_appointments_id(self, teacher_job_appointments_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherJobAppointments).where(TeacherJobAppointments.teacher_job_appointments_id == teacher_job_appointments_id))
		return result.scalar_one_or_none()

	async def query_teacherjobappointments_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherJobAppointments)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherjobappointments(self, teacherjobappointments, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherjobappointments, *args)
		query = update(TeacherJobAppointments).where(TeacherJobAppointments.teacher_job_appointments_id == teacherjobappointments.teacher_job_appointments_id).values(**update_contents)
		return await self.update(session, query, teacherjobappointments, update_contents, is_commit=is_commit)
