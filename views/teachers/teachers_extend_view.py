from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query

from views.models.teacher_extend import TeacherLearnExperienceModel, TeacherLearnExperienceUpdateModel
from rules.teacher_learn_experience_rule import TeacherLearnExperienceRule

from views.models.teacher_extend import TeacherWorkExperienceModel, TeacherWorkExperienceUpdateModel
from rules.teacher_work_experience_rule import TeacherWorkExperienceRule

from views.models.teacher_extend import TeacherJobAppointmentsModel, TeacherJobAppointmentsUpdateModel
from rules.teacher_job_appointments_rule import TeacherJobAppointmentsRule

from views.models.teacher_extend import TeacherProfessionalTitlesModel, TeacherProfessionalTitlesUpdateModel
from rules.teacher_professional_titles_rule import TeacherProfessionalTitlesRule

from views.models.teacher_extend import TeacherQualificationsModel, TeacherQualificationsUpdateModel
from rules.teacher_qualifications_rule import TeacherQualificationsRule

from views.models.teacher_extend import TeacherSkillCertificatesModel, TeacherSkillCertificatesUpdateModel
from rules.teacher_skill_certificates_rule import TeacherSkillCertificatesRule

from views.models.teacher_extend import TeacherEthicRecordsModel, TeacherEthicRecordsUpdateModel
from rules.teacher_ethic_records_rule import TeacherEthicRecordsRule

from views.models.teacher_extend import EducationalTeachingModel, EducationalTeachingUpdateModel
from rules.educational_teaching_rule import EducationalTeachingRule


class TeacherLearnExperienceView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_learn_experience_rule = get_injector(TeacherLearnExperienceRule)

    async def get_teacher_learn_experience(self,
                                           teacher_learn_experience_id: int = Query(None,
                                                                                    title="teacher_learn_experienceID",
                                                                                    description="teacher_learn_experienceID",
                                                                                    example=1234)
                                           ):
        res = await self.teacher_learn_experience_rule.get_teacher_learn_experience_by_teacher_learn_experience_id(
            teacher_learn_experience_id)
        return res

    async def post_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceModel):
        res = await self.teacher_learn_experience_rule.add_teacher_learn_experience(teacher_learn_experience)
        return res

    async def delete_teacher_learn_experience(self,
                                              teacher_learn_experience_id: int = Query(None,
                                                                                       title="teacher_learn_experienceID",
                                                                                       description="teacher_learn_experienceID",
                                                                                       example=1234)
                                              ):
        await self.teacher_learn_experience_rule.delete_teacher_learn_experience(teacher_learn_experience_id)

    async def put_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceUpdateModel):
        res = await self.teacher_learn_experience_rule.update_teacher_learn_experience(teacher_learn_experience)
        return res

    async def get_teacher_learn_experience_all(self, teacher_id: int = Query(None, title="teacher_learn_experienceID",
                                                                             description="teacher_learn_experienceID",
                                                                             example=1234)):
        return await self.teacher_learn_experience_rule.get_all_teacher_learn_experience(teacher_id)


class TeacherWorkExperienceView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_work_experience_rule = get_injector(TeacherWorkExperienceRule)

    async def get_teacher_work_experience(self,
                                          teacher_work_experience_id: int = Query(None,
                                                                                  title="teacher_work_experienceID",
                                                                                  description="teacher_work_experienceID",
                                                                                  example=1234)
                                          ):
        res = await self.teacher_work_experience_rule.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        return res

    async def post_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceModel):
        res = await self.teacher_work_experience_rule.add_teacher_work_experience(teacher_work_experience)
        return res

    async def delete_teacher_work_experience(self,
                                             teacher_work_experience_id: int = Query(None,
                                                                                     title="teacher_work_experienceID",
                                                                                     description="teacher_work_experienceID",
                                                                                     example=1234)
                                             ):
        await self.teacher_work_experience_rule.delete_teacher_work_experience(teacher_work_experience_id)

    async def put_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceUpdateModel):
        res = await self.teacher_work_experience_rule.update_teacher_work_experience(teacher_work_experience)
        return res

    async def get_teacher_work_experience_all(self, teacher_id: int = Query(None, title="teacher_work_experienceID",
                                                                            description="teacher_work_experienceID",
                                                                            example=1234)):
        return await self.teacher_work_experience_rule.get_all_teacher_work_experience(teacher_id)


class TeacherJobAppointmentsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_job_appointments_rule = get_injector(TeacherJobAppointmentsRule)

    async def get_teacher_job_appointments(self,
                                           teacher_job_appointments_id: int = Query(None,
                                                                                    title="teacher_job_appointmentsID",
                                                                                    description="teacher_job_appointmentsID",
                                                                                    example=1234)
                                           ):
        res = await self.teacher_job_appointments_rule.get_teacher_job_appointments_by_teacher_job_appointments_id(
            teacher_job_appointments_id)
        return res

    async def post_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsModel):
        res = await self.teacher_job_appointments_rule.add_teacher_job_appointments(teacher_job_appointments)
        return res

    async def delete_teacher_job_appointments(self,
                                              teacher_job_appointments_id: int = Query(None,
                                                                                       title="teacher_job_appointmentsID",
                                                                                       description="teacher_job_appointmentsID",
                                                                                       example=1234)
                                              ):
        await self.teacher_job_appointments_rule.delete_teacher_job_appointments(teacher_job_appointments_id)

    async def put_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsUpdateModel):
        res = await self.teacher_job_appointments_rule.update_teacher_job_appointments(teacher_job_appointments)
        return res

    async def get_teacher_job_appointments_all(self, teacher_id: int = Query(None, title="teacher_job_appointmentsID",
                                                                             description="teacher_job_appointmentsID",
                                                                             example=1234)):
        return await self.teacher_job_appointments_rule.get_all_teacher_job_appointments(teacher_id)


class TeacherProfessionalTitlesView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_professional_titles_rule = get_injector(TeacherProfessionalTitlesRule)

    async def get_teacher_professional_titles(self,
                                              teacher_professional_titles_id: int = Query(None,
                                                                                          title="teacher_professional_titlesID",
                                                                                          description="teacher_professional_titlesID",
                                                                                          example=1234)
                                              ):
        res = await self.teacher_professional_titles_rule.get_teacher_professional_titles_by_teacher_professional_titles_id(
            teacher_professional_titles_id)
        return res

    async def post_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitlesModel):
        res = await self.teacher_professional_titles_rule.add_teacher_professional_titles(teacher_professional_titles)
        return res

    async def delete_teacher_professional_titles(self,
                                                 teacher_professional_titles_id: int = Query(None,
                                                                                             title="teacher_professional_titlesID",
                                                                                             description="teacher_professional_titlesID",
                                                                                             example=1234)
                                                 ):
        await self.teacher_professional_titles_rule.delete_teacher_professional_titles(teacher_professional_titles_id)

    async def put_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitlesUpdateModel):
        res = await self.teacher_professional_titles_rule.update_teacher_professional_titles(
            teacher_professional_titles)
        return res

    async def get_teacher_professional_titles_all(self,
                                                  teacher_id: int = Query(None, title="teacher_professional_titlesID",
                                                                          description="teacher_professional_titlesID",
                                                                          example=1234)):
        return await self.teacher_professional_titles_rule.get_all_teacher_professional_titles(teacher_id)


class TeacherQualificationsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_qualifications_rule = get_injector(TeacherQualificationsRule)

    async def get_teacher_qualifications(self,
                                         teacher_qualifications_id: int = Query(None, title="teacher_qualificationsID",
                                                                                description="teacher_qualificationsID",
                                                                                example=1234)
                                         ):
        res = await self.teacher_qualifications_rule.get_teacher_qualifications_by_teacher_qualifications_id(
            teacher_qualifications_id)
        return res

    async def post_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsModel):
        res = await self.teacher_qualifications_rule.add_teacher_qualifications(teacher_qualifications)
        return res

    async def delete_teacher_qualifications(self,
                                            teacher_qualifications_id: int = Query(None,
                                                                                   title="teacher_qualificationsID",
                                                                                   description="teacher_qualificationsID",
                                                                                   example=1234)
                                            ):
        await self.teacher_qualifications_rule.delete_teacher_qualifications(teacher_qualifications_id)

    async def put_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsUpdateModel):
        res = await self.teacher_qualifications_rule.update_teacher_qualifications(teacher_qualifications)
        return res

    async def get_teacher_qualifications_all(self, teacher_id: int = Query(None, title="teacher_qualificationsID",
                                                                           description="teacher_qualificationsID",
                                                                           example=1234)):
        return await self.teacher_qualifications_rule.get_all_teacher_qualifications(teacher_id)


class TeacherSkillCertificatesView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_skill_certificates_rule = get_injector(TeacherSkillCertificatesRule)

    async def get_teacher_skill_certificates(self,
                                             teacher_skill_certificates_id: int = Query(None,
                                                                                        title="teacher_skill_certificatesID",
                                                                                        description="teacher_skill_certificatesID",
                                                                                        example=1234)
                                             ):
        res = await self.teacher_skill_certificates_rule.get_teacher_skill_certificates_by_teacher_skill_certificates_id(
            teacher_skill_certificates_id)
        return res

    async def post_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesModel):
        res = await self.teacher_skill_certificates_rule.add_teacher_skill_certificates(teacher_skill_certificates)
        return res

    async def delete_teacher_skill_certificates(self,
                                                teacher_skill_certificates_id: int = Query(None,
                                                                                           title="teacher_skill_certificatesID",
                                                                                           description="teacher_skill_certificatesID",
                                                                                           example=1234)
                                                ):
        await self.teacher_skill_certificates_rule.delete_teacher_skill_certificates(teacher_skill_certificates_id)

    async def put_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesUpdateModel):
        res = await self.teacher_skill_certificates_rule.update_teacher_skill_certificates(teacher_skill_certificates)
        return res

    async def get_teacher_skill_certificates_all(self,
                                                 teacher_id: int = Query(None, title="teacher_skill_certificatesID",
                                                                         description="teacher_skill_certificatesID",
                                                                         example=1234)):
        return await self.teacher_skill_certificates_rule.get_all_teacher_skill_certificates(teacher_id)


class TeacherEthicRecordsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_ethic_records_rule = get_injector(TeacherEthicRecordsRule)

    async def get_teacher_ethic_records(self,
                                        teacher_ethic_records_id: int = Query(None, title="teacher_ethic_recordsID",
                                                                              description="teacher_ethic_recordsID",
                                                                              example=1234)
                                        ):
        res = await self.teacher_ethic_records_rule.get_teacher_ethic_records_by_teacher_ethic_records_id(
            teacher_ethic_records_id)
        return res

    async def post_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsModel):
        res = await self.teacher_ethic_records_rule.add_teacher_ethic_records(teacher_ethic_records)
        return res

    async def delete_teacher_ethic_records(self,
                                           teacher_ethic_records_id: int = Query(None, title="teacher_ethic_recordsID",
                                                                                 description="teacher_ethic_recordsID",
                                                                                 example=1234)
                                           ):
        await self.teacher_ethic_records_rule.delete_teacher_ethic_records(teacher_ethic_records_id)

    async def put_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsUpdateModel):
        res = await self.teacher_ethic_records_rule.update_teacher_ethic_records(teacher_ethic_records)
        return res

    async def get_teacher_ethic_records_all(self, teacher_id: int = Query(None, title="teacher_ethic_recordsID",
                                                                          description="teacher_ethic_recordsID",
                                                                          example=1234)):
        return await self.teacher_ethic_records_rule.get_all_teacher_ethic_records(teacher_id)


class EducationalTeachingView(BaseView):
    def __init__(self):
        super().__init__()

        self.educational_teaching_rule = get_injector(EducationalTeachingRule)

    async def get_educational_teaching(self,
                                       educational_teaching_id: int = Query(None, title="educational_teachingID",
                                                                            description="educational_teachingID",
                                                                            example=1234)
                                       ):
        res = await self.educational_teaching_rule.get_educational_teaching_by_educational_teaching_id(
            educational_teaching_id)
        return res

    async def post_educational_teaching(self, educational_teaching: EducationalTeachingModel):
        res = await self.educational_teaching_rule.add_educational_teaching(educational_teaching)
        return res

    async def delete_educational_teaching(self,
                                          educational_teaching_id: int = Query(None, title="educational_teachingID",
                                                                               description="educational_teachingID",
                                                                               example=1234)
                                          ):
        await self.educational_teaching_rule.delete_educational_teaching(educational_teaching_id)

    async def put_educational_teaching(self, educational_teaching: EducationalTeachingUpdateModel):
        res = await self.educational_teaching_rule.update_educational_teaching(educational_teaching)
        return res

    async def get_educational_teaching_all(self, teacher_id: int = Query(None, title="educational_teachingID",
                                                                         description="educational_teachingID",
                                                                         example=1234)):
        return await self.educational_teaching_rule.get_all_educational_teaching(teacher_id)
