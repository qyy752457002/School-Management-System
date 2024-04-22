from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_skill_certificates import TeacherSkillCertificates
from models.teachers import Teacher


class TeacherSkillCertificatesDAO(DAOBase):

    async def add_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificates):
        session = await self.master_db()
        session.add(teacher_skill_certificates)
        await session.commit()
        await session.refresh(teacher_skill_certificates)
        return teacher_skill_certificates

    async def get_teacher_skill_certificates_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherSkillCertificates))
        return result.scalar()

    async def delete_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificates):
        session = await self.master_db()
        await session.delete(teacher_skill_certificates)
        await session.commit()

    async def get_teacher_skill_certificates_by_teacher_skill_certificates_id(self, teacher_skill_certificates_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherSkillCertificates).where(
            TeacherSkillCertificates.teacher_skill_certificates_id == teacher_skill_certificates_id))
        return result.scalar_one_or_none()

    async def query_teacher_skill_certificates_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(TeacherSkillCertificates)

        paging = await self.query_page(query, page_request)
        return paging

    async def update_teacher_skill_certificates(self, teacher_skill_certificates, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_skill_certificates, *args)
        query = update(TeacherSkillCertificates).where(
            TeacherSkillCertificates.teacher_skill_certificates_id == teacher_skill_certificates.teacher_skill_certificates_id).values(
            **update_contents)
        return await self.update(session, query, teacher_skill_certificates, update_contents, is_commit=is_commit)

    async def get_all_teacher_skill_certificates(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherSkillCertificates).join(Teacher,
                                                      TeacherSkillCertificates.teacher_id == Teacher.teacher_id).where(
            TeacherSkillCertificates.teacher_id == teacher_id)
        result = await session.execute(query)
        return result.scalars().all()
