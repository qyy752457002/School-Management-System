from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse

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

from views.models.teacher_extend import DomesticTrainingModel, DomesticTrainingUpdateModel
from rules.domestic_training_rule import DomesticTrainingRule

from views.models.teacher_extend import OverseasStudyModel, OverseasStudyUpdateModel
from rules.overseas_study_rule import OverseasStudyRule

from views.models.teacher_extend import TalentProgramModel, TalentProgramUpdateModel
from rules.talent_program_rule import TalentProgramRule

from views.models.teacher_extend import AnnualReviewModel, AnnualReviewUpdateModel
from rules.annual_review_rule import AnnualReviewRule

from views.models.teacher_extend import ResearchAchievementsModel, ResearchAchievementsUpdateModel, \
    ResearchAchievementsQueryModel, ResearchAchievementsQueryReModel
from rules.research_achievements_rule import ResearchAchievementsRule


class TeacherLearnExperienceView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_learn_experience_rule = get_injector(TeacherLearnExperienceRule)

    async def get_teacher_learn_experience(self,
                                           teacher_learn_experience_id: int = Query(...,
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
                                              teacher_learn_experience_id: int = Query(...,
                                                                                       title="teacher_learn_experienceID",
                                                                                       description="teacher_learn_experienceID",
                                                                                       example=1234)
                                              ):
        await self.teacher_learn_experience_rule.delete_teacher_learn_experience(teacher_learn_experience_id)
        return str(teacher_learn_experience_id)

    async def put_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceUpdateModel):
        res = await self.teacher_learn_experience_rule.update_teacher_learn_experience(teacher_learn_experience)
        return res

    async def get_teacher_learn_experience_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                             description="teacher_id",
                                                                             example=1234)):
        return await self.teacher_learn_experience_rule.get_all_teacher_learn_experience(teacher_id)


class TeacherWorkExperienceView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_work_experience_rule = get_injector(TeacherWorkExperienceRule)

    async def get_teacher_work_experience(self,
                                          teacher_work_experience_id: int = Query(...,
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
                                             teacher_work_experience_id: int = Query(...,
                                                                                     title="teacher_work_experienceID",
                                                                                     description="teacher_work_experienceID",
                                                                                     example=1234)
                                             ):
        await self.teacher_work_experience_rule.delete_teacher_work_experience(teacher_work_experience_id)
        return str(teacher_work_experience_id)

    async def put_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceUpdateModel):
        res = await self.teacher_work_experience_rule.update_teacher_work_experience(teacher_work_experience)
        return res

    async def get_teacher_work_experience_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                            description="teacher_id",
                                                                            example=1234)):
        return await self.teacher_work_experience_rule.get_all_teacher_work_experience(teacher_id)


class TeacherJobAppointmentsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_job_appointments_rule = get_injector(TeacherJobAppointmentsRule)

    async def get_teacher_job_appointments(self,
                                           teacher_job_appointments_id: int = Query(...,
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
                                              teacher_job_appointments_id: int = Query(...,
                                                                                       title="teacher_job_appointmentsID",
                                                                                       description="teacher_job_appointmentsID",
                                                                                       example=1234)
                                              ):
        await self.teacher_job_appointments_rule.delete_teacher_job_appointments(teacher_job_appointments_id)
        return str(teacher_job_appointments_id)

    async def put_teacher_job_appointments(self, teacher_job_appointments: TeacherJobAppointmentsUpdateModel):
        res = await self.teacher_job_appointments_rule.update_teacher_job_appointments(teacher_job_appointments)
        return res

    async def get_teacher_job_appointments_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                             description="teacher_id",
                                                                             example=1234)):
        return await self.teacher_job_appointments_rule.get_all_teacher_job_appointments(teacher_id)

    """
    teacher_job_appointments提交、审核、通过、拒绝 
    """

    async def pacth_submitting(self, teacher_job_appointments_id: int = Query(...,
                                                                              title="teacher_job_appointmentsID",
                                                                              description="teacher_job_appointmentsID",
                                                                              example=1234)):
        await self.teacher_job_appointments_rule.submitting(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def pacth_submitted(self, teacher_job_appointments_id: int = Query(...,
                                                                             title="teacher_job_appointmentsID",
                                                                             description="teacher_job_appointmentsID",
                                                                             example=1234)):
        await self.teacher_job_appointments_rule.submitted(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def pacth_approved(self, teacher_job_appointments_id: int = Query(...,
                                                                            title="teacher_job_appointmentsID",
                                                                            description="teacher_job_appointmentsID",
                                                                            example=1234)):
        await self.teacher_job_appointments_rule.approved(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def pacth_rejected(self, teacher_job_appointments_id: int = Query(...,
                                                                            title="teacher_job_appointmentsID",
                                                                            description="teacher_job_appointmentsID",

                                                                            example=1234)):
        await self.teacher_job_appointments_rule.rejected(teacher_job_appointments_id)
        return teacher_job_appointments_id


class TeacherProfessionalTitlesView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_professional_titles_rule = get_injector(TeacherProfessionalTitlesRule)

    async def get_teacher_professional_titles(self,
                                              teacher_professional_titles_id: int = Query(...,
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
                                                 teacher_professional_titles_id: int = Query(...,
                                                                                             title="teacher_professional_titlesID",
                                                                                             description="teacher_professional_titlesID",
                                                                                             example=1234)
                                                 ):
        await self.teacher_professional_titles_rule.delete_teacher_professional_titles(teacher_professional_titles_id)
        return str(teacher_professional_titles_id)

    async def put_teacher_professional_titles(self, teacher_professional_titles: TeacherProfessionalTitlesUpdateModel):
        res = await self.teacher_professional_titles_rule.update_teacher_professional_titles(
            teacher_professional_titles)
        return res

    async def get_teacher_professional_titles_all(self,
                                                  teacher_id: int = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234)):
        return await self.teacher_professional_titles_rule.get_all_teacher_professional_titles(teacher_id)

    """
    teacher_professional_titles提交、审核、通过、拒绝
    """

    async def pacth_submitting(self, teacher_professional_titles_id: int = Query(...,
                                                                                 title="teacher_professional_titlesID",
                                                                                 description="teacher_professional_titlesID",
                                                                                 example=1234)):
        await self.teacher_professional_titles_rule.submitting(teacher_professional_titles_id)
        return teacher_professional_titles_id

    async def pacth_submitted(self, teacher_professional_titles_id: int = Query(...,
                                                                                title="teacher_professional_titlesID",
                                                                                description="teacher_professional_titlesID",
                                                                                example=1234)):
        await self.teacher_professional_titles_rule.submitted(teacher_professional_titles_id)
        return teacher_professional_titles_id

    async def pacth_approved(self,
                             teacher_professional_titles_id: int = Query(..., title="teacher_professional_titlesID",
                                                                         description="teacher_professional_titlesID",
                                                                         example=1234)):
        await self.teacher_professional_titles_rule.approved(teacher_professional_titles_id)
        return teacher_professional_titles_id


class TeacherQualificationsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_qualifications_rule = get_injector(TeacherQualificationsRule)

    async def get_teacher_qualifications(self,
                                         teacher_qualifications_id: int = Query(..., title="teacher_qualificationsID",
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
                                            teacher_qualifications_id: int = Query(...,
                                                                                   title="teacher_qualificationsID",
                                                                                   description="teacher_qualificationsID",
                                                                                   example=1234)
                                            ):
        await self.teacher_qualifications_rule.delete_teacher_qualifications(teacher_qualifications_id)
        return str(teacher_qualifications_id)

    async def put_teacher_qualifications(self, teacher_qualifications: TeacherQualificationsUpdateModel):
        res = await self.teacher_qualifications_rule.update_teacher_qualifications(teacher_qualifications)
        return res

    async def get_teacher_qualifications_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                           description="teacher_id",
                                                                           example=1234)):
        return await self.teacher_qualifications_rule.get_all_teacher_qualifications(teacher_id)


class TeacherSkillCertificatesView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_skill_certificates_rule = get_injector(TeacherSkillCertificatesRule)

    async def get_teacher_skill_certificates(self,
                                             teacher_skill_certificates_id: int = Query(...,
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
                                                teacher_skill_certificates_id: int = Query(...,
                                                                                           title="teacher_skill_certificatesID",
                                                                                           description="teacher_skill_certificatesID",
                                                                                           example=1234)
                                                ):
        await self.teacher_skill_certificates_rule.delete_teacher_skill_certificates(teacher_skill_certificates_id)
        return str(teacher_skill_certificates_id)

    async def put_teacher_skill_certificates(self, teacher_skill_certificates: TeacherSkillCertificatesUpdateModel):
        res = await self.teacher_skill_certificates_rule.update_teacher_skill_certificates(teacher_skill_certificates)
        return res

    async def get_teacher_skill_certificates_all(self,
                                                 teacher_id: int = Query(..., title="teacher_id",
                                                                         description="teacher_id",
                                                                         example=1234)):
        return await self.teacher_skill_certificates_rule.get_all_teacher_skill_certificates(teacher_id)


class TeacherEthicRecordsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_ethic_records_rule = get_injector(TeacherEthicRecordsRule)

    async def get_teacher_ethic_records(self,
                                        teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
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
                                           teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                                 description="teacher_ethic_recordsID",
                                                                                 example=1234)
                                           ):
        await self.teacher_ethic_records_rule.delete_teacher_ethic_records(teacher_ethic_records_id)
        return str(teacher_ethic_records_id)

    async def put_teacher_ethic_records(self, teacher_ethic_records: TeacherEthicRecordsUpdateModel):
        res = await self.teacher_ethic_records_rule.update_teacher_ethic_records(teacher_ethic_records)
        return res

    async def get_teacher_ethic_records_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234)):
        return await self.teacher_ethic_records_rule.get_all_teacher_ethic_records(teacher_id)

    """
    teacher_ethic_records提交、审核、通过、拒绝
    """

    async def pacth_submitting(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                           description="teacher_ethic_recordsID",
                                                                           example=1234)):
        await self.teacher_ethic_records_rule.submitting(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def pacth_submitted(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                          description="teacher_ethic_recordsID",
                                                                          example=1234)):
        await self.teacher_ethic_records_rule.submitted(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def pacth_approved(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                         description="teacher_ethic_recordsID",
                                                                         example=1234)):
        await self.teacher_ethic_records_rule.approved(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def pacth_rejected(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                         description="teacher_ethic_recordsID",
                                                                         example=1234)):
        await self.teacher_ethic_records_rule.rejected(teacher_ethic_records_id)
        return teacher_ethic_records_id


class EducationalTeachingView(BaseView):
    def __init__(self):
        super().__init__()

        self.educational_teaching_rule = get_injector(EducationalTeachingRule)

    async def get_educational_teaching(self,
                                       educational_teaching_id: int = Query(..., title="educational_teachingID",
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
                                          educational_teaching_id: int = Query(..., title="educational_teachingID",
                                                                               description="educational_teachingID",
                                                                               example=1234)
                                          ):
        await self.educational_teaching_rule.delete_educational_teaching(educational_teaching_id)
        return str(educational_teaching_id)

    async def put_educational_teaching(self, educational_teaching: EducationalTeachingUpdateModel):
        res = await self.educational_teaching_rule.update_educational_teaching(educational_teaching)
        return res

    async def get_educational_teaching_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                         description="teacher_id",
                                                                         example=1234)):
        return await self.educational_teaching_rule.get_all_educational_teaching(teacher_id)


class DomesticTrainingView(BaseView):
    def __init__(self):
        super().__init__()

        self.domestic_training_rule = get_injector(DomesticTrainingRule)

    async def get_domestic_training(self,
                                    domestic_training_id: int = Query(..., title="domestic_trainingID",
                                                                      description="domestic_trainingID", example=1234)
                                    ):
        res = await self.domestic_training_rule.get_domestic_training_by_domestic_training_id(domestic_training_id)
        return res

    async def post_domestic_training(self, domestic_training: DomesticTrainingModel):
        res = await self.domestic_training_rule.add_domestic_training(domestic_training)
        return res

    async def delete_domestic_training(self,
                                       domestic_training_id: int = Query(..., title="domestic_trainingID",
                                                                         description="domestic_trainingID",
                                                                         example=1234)
                                       ):
        await self.domestic_training_rule.delete_domestic_training(domestic_training_id)
        return str(domestic_training_id)

    async def put_domestic_training(self, domestic_training: DomesticTrainingUpdateModel):
        res = await self.domestic_training_rule.update_domestic_training(domestic_training)
        return res

    async def get_domestic_training_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                      description="teacher_id", example=1234)):
        return await self.domestic_training_rule.get_all_domestic_training(teacher_id)


class OverseasStudyView(BaseView):
    def __init__(self):
        super().__init__()

        self.overseas_study_rule = get_injector(OverseasStudyRule)

    async def get_overseas_study(self,
                                 overseas_study_id: int = Query(..., title="overseas_studyID",
                                                                description="overseas_studyID", example=1234)
                                 ):
        res = await self.overseas_study_rule.get_overseas_study_by_overseas_study_id(overseas_study_id)
        return res

    async def post_overseas_study(self, overseas_study: OverseasStudyModel):
        res = await self.overseas_study_rule.add_overseas_study(overseas_study)
        return res

    async def delete_overseas_study(self,
                                    overseas_study_id: int = Query(..., title="overseas_studyID",
                                                                   description="overseas_studyID", example=1234)
                                    ):
        await self.overseas_study_rule.delete_overseas_study(overseas_study_id)
        return str(overseas_study_id)

    async def put_overseas_study(self, overseas_study: OverseasStudyUpdateModel):
        res = await self.overseas_study_rule.update_overseas_study(overseas_study)
        return res

    async def get_overseas_study_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                   description="teacher_id", example=1234)):
        return await self.overseas_study_rule.get_all_overseas_study(teacher_id)


class TalentProgramView(BaseView):
    def __init__(self):
        super().__init__()

        self.talent_program_rule = get_injector(TalentProgramRule)

    async def get_talent_program(self,
                                 talent_program_id: int = Query(..., title="talent_programID",
                                                                description="talent_programID", example=1234)
                                 ):
        res = await self.talent_program_rule.get_talent_program_by_talent_program_id(talent_program_id)
        return res

    async def post_talent_program(self, talent_program: TalentProgramModel):
        res = await self.talent_program_rule.add_talent_program(talent_program)
        return res

    async def delete_talent_program(self,
                                    talent_program_id: int = Query(..., title="talent_programID",
                                                                   description="talent_programID", example=1234)
                                    ):
        await self.talent_program_rule.delete_talent_program(talent_program_id)
        return str(talent_program_id)

    async def put_talent_program(self, talent_program: TalentProgramUpdateModel):
        res = await self.talent_program_rule.update_talent_program(talent_program)
        return res

    async def get_talent_program_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                   description="teacher_id", example=1234)):
        return await self.talent_program_rule.get_all_talent_program(teacher_id)

    """
    talent_program提交、审核、通过、拒绝"""

    async def pacth_submitting(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                    description="talent_programID", example=1234)):
        await self.talent_program_rule.submitting(talent_program_id)
        return talent_program_id

    async def pacth_submitted(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                   description="talent_programID", example=1234)):
        await self.talent_program_rule.submitted(talent_program_id)
        return talent_program_id

    async def pacth_approved(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                  description="talent_programID", example=1234)):
        await self.talent_program_rule.approved(talent_program_id)
        return talent_program_id

    async def pacth_rejected(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                  description="talent_programID", example=1234)):
        await self.talent_program_rule.rejected(talent_program_id)
        return talent_program_id


class AnnualReviewView(BaseView):
    def __init__(self):
        super().__init__()

        self.annual_review_rule = get_injector(AnnualReviewRule)

    async def get_annual_review(self,
                                annual_review_id: int = Query(..., title="annual_reviewID",
                                                              description="annual_reviewID", example=1234)
                                ):
        res = await self.annual_review_rule.get_annual_review_by_annual_review_id(annual_review_id)
        return res

    async def post_annual_review(self, annual_review: AnnualReviewModel):
        res = await self.annual_review_rule.add_annual_review(annual_review)
        return res

    async def delete_annual_review(self,
                                   annual_review_id: int = Query(..., title="annual_reviewID",
                                                                 description="annual_reviewID", example=1234)
                                   ):
        await self.annual_review_rule.delete_annual_review(annual_review_id)
        return str(annual_review_id)

    async def put_annual_review(self, annual_review: AnnualReviewUpdateModel):
        res = await self.annual_review_rule.update_annual_review(annual_review)
        return res

    async def get_annual_review_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                  description="teacher_id", example=1234)):
        return await self.annual_review_rule.get_all_annual_review(teacher_id)

    """
    annual_review提交、审核、通过、拒绝
    """

    async def pacth_submitting(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                   description="annual_reviewID", example=1234)):
        await self.annual_review_rule.submitting(annual_review_id)
        return annual_review_id

    async def pacth_submitted(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                  description="annual_reviewID", example=1234)):
        await self.annual_review_rule.submitted(annual_review_id)
        return annual_review_id

    async def pacth_approved(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                 description="annual_reviewID", example=1234)):
        await self.annual_review_rule.approved(annual_review_id)
        return annual_review_id

    async def pacth_rejected(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                 description="annual_reviewID", example=1234)):
        await self.annual_review_rule.rejected(annual_review_id)
        return annual_review_id


class ResearchAchievementsView(BaseView):
    def __init__(self):
        super().__init__()

        self.research_achievements_rule = get_injector(ResearchAchievementsRule)

    async def get_research_achievements(self,
                                        research_achievements_id: int = Query(..., title="research_achievementsID",
                                                                              description="research_achievementsID",
                                                                              example=1234)
                                        ):
        res = await self.research_achievements_rule.get_research_achievements_by_research_achievements_id(
            research_achievements_id)
        return res

    async def post_research_achievements(self, research_achievements: ResearchAchievementsModel):
        res = await self.research_achievements_rule.add_research_achievements(research_achievements)
        return res

    async def delete_research_achievements(self,
                                           research_achievements_id: int = Query(..., title="research_achievementsID",
                                                                                 description="research_achievementsID",
                                                                                 example=1234)
                                           ):
        await self.research_achievements_rule.delete_research_achievements(research_achievements_id)
        return str(research_achievements_id)

    async def put_research_achievements(self, research_achievements: ResearchAchievementsUpdateModel):
        res = await self.research_achievements_rule.update_research_achievements(research_achievements)
        return res

    async def get_research_achievements_all(self, teacher_id: int = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234)):
        return await self.research_achievements_rule.get_all_research_achievements(teacher_id)

    # async def page(self, research_achievements=Depends(ResearchAchievementsQueryModel),
    #                page_request=Depends(PageRequest)):
    #     paging_result = await self.research_achievements_rule.query_research_achievements_with_page(
    #         research_achievements, page_request)
    #     return paging_result
