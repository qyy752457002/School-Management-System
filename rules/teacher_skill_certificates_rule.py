from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_skill_certificates_dao import TeacherSkillCertificatesDAO
from models.teacher_skill_certificates import TeacherSkillCertificates
from views.models.teacher_extend import TeacherSkillCertificatesModel, TeacherSkillCertificatesUpdateModel


@dataclass_inject
class TeacherSkillCertificatesRule(object):
    teacher_skill_certificates_dao: TeacherSkillCertificatesDAO

    async def get_teacher_skill_certificates_by_teacher_skill_certificates_id(self, teacher_skill_certificates_id):
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates_id)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesModel)
        return teacher_skill_certificates

    async def add_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesModel):
        teacher_skill_certificates_db = view_model_to_orm_model(teacher_skill_certificates, TeacherSkillCertificates)
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.add_teacher_skill_certificates(
            teacher_skill_certificates_db)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesModel)
        return teacher_skill_certificates

    async def delete_teacher_skill_certificates(self, teacher_skill_certificates_id):
        exists_teacher_skill_certificates = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates_id)
        if not exists_teacher_skill_certificates:
            raise Exception(f"编号为的{teacher_skill_certificates_id}teacher_skill_certificates不存在")
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.delete_teacher_skill_certificates(
            exists_teacher_skill_certificates)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesModel, exclude=[""])
        return teacher_skill_certificates

    async def update_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesUpdateModel):
        exists_teacher_skill_certificates_info = await self.teacher_skill_certificates_dao.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates.teacher_skill_certificates_id)
        if not exists_teacher_skill_certificates_info:
            raise Exception(
                f"编号为{teacher_skill_certificates.teacher_skill_certificates_id}的teacher_skill_certificates不存在")
        need_update_list = []
        for key, value in teacher_skill_certificates.dict().items():
            if value:
                need_update_list.append(key)
        teacher_skill_certificates = await self.teacher_skill_certificates_dao.update_teacher_skill_certificates(
            teacher_skill_certificates, *need_update_list)
        return teacher_skill_certificates

    async def get_all_teacher_skill_certificates(self, teacher_id):
        teacher_skill_certificates_db = await self.teacher_skill_certificates_dao.get_all_teacher_skill_certificates(
            teacher_id)
        teacher_skill_certificates = orm_model_to_view_model(teacher_skill_certificates_db,
                                                             TeacherSkillCertificatesModel, exclude=[""])
        return teacher_skill_certificates
