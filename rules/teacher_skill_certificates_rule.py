from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_skill_certificates_dao import TeacherSkillCertificatesDAO
from models.teacher_skill_certificates import TeacherSkillCertificates
from views.models.teacher_extend import TeacherSkillCertificatesModel, TeacherSkillCertificatesUpdateModel
from daos.teacher_work_experience_dao import TeacherWorkExperienceDAO
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError, TeacherSkillNotFoundError


@dataclass_inject
class TeacherSkillCertificatesRule(object):
    teacher_skill_certificates_dao: TeacherSkillCertificatesDAO
    teachers_dao: TeachersDao

    async def get_teacher_skill_certificates_by_teacher_skill_certificates_id(self, teacher_skill_certificates_id):
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates_id)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesUpdateModel)
        return teacher_skill_certificates

    async def add_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(teacher_skill_certificates.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        teacher_skill_certificates_db = view_model_to_orm_model(teacher_skill_certificates, TeacherSkillCertificates)
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.add_teacher_skill_certificates(
            teacher_skill_certificates_db)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesUpdateModel)
        return teacher_skill_certificates

    async def delete_teacher_skill_certificates(self, teacher_skill_certificates_id):
        exists_teacher_skill_certificates = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates_id)
        if not exists_teacher_skill_certificates:
            raise TeacherSkillNotFoundError()
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.delete_teacher_skill_certificates(
            exists_teacher_skill_certificates)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesModel, exclude=[""])
        return teacher_skill_certificates

    async def update_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesUpdateModel):
        exists_teacher_skill_certificates_info = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates.teacher_skill_certificates_id)
        if not exists_teacher_skill_certificates_info:
            raise TeacherSkillNotFoundError()
        need_update_list = []
        for key, value in teacher_skill_certificates.dict().items():
            if value:
                need_update_list.append(key)
        teacher_skill_certificates = await self.teacher_skill_certificates_dao.update_teacher_skill_certificates(
            teacher_skill_certificates, *need_update_list)
        return teacher_skill_certificates

    async def get_all_teacher_skill_certificates(self, teacher_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.get_all_teacher_skill_certificates(
            teacher_id)
        teacher_skill_certificates = []
        for teacher_skill_certificate in teacher_skill_certificates_db:
            teacher_skill_certificates.append(
                orm_model_to_view_model(teacher_skill_certificate, TeacherSkillCertificatesUpdateModel))
        return teacher_skill_certificates_db
