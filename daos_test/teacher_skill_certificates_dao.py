from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_skill_certificates import TeacherSkillCertificates


class TeacherSkillCertificatesDAO(DAOBase):

	async def add_teacherskillcertificates(self, teacherskillcertificates: TeacherSkillCertificates):
		session = await self.master_db()
		session.add(teacherskillcertificates)
		await session.commit()
		await session.refresh(teacherskillcertificates)
		return teacherskillcertificates

	async def get_teacherskillcertificates_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TeacherSkillCertificates))
		return result.scalar()

	async def delete_teacherskillcertificates(self, teacherskillcertificates: TeacherSkillCertificates):
		session = await self.master_db()
		await session.delete(teacherskillcertificates)
		await session.commit()

	async def get_teacherskillcertificates_by_teacher_skill_certificates_id(self, teacher_skill_certificates_id):
		session = await self.slave_db()
		result = await session.execute(select(TeacherSkillCertificates).where(TeacherSkillCertificates.teacher_skill_certificates_id == teacher_skill_certificates_id))
		return result.scalar_one_or_none()

	async def query_teacherskillcertificates_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TeacherSkillCertificates)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_teacherskillcertificates(self, teacherskillcertificates, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(teacherskillcertificates, *args)
		query = update(TeacherSkillCertificates).where(TeacherSkillCertificates.teacher_skill_certificates_id == teacherskillcertificates.teacher_skill_certificates_id).values(**update_contents)
		return await self.update(session, query, teacherskillcertificates, update_contents, is_commit=is_commit)
