from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.request_context import request_context_manager
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from rules.teachers_rule import TeachersRule
from rules.teacher_extend_import_rule import TeacherExtendImportRule

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

    # 根据teacher_learn_experience_id获取教师学习经验
    async def get_teacher_learn_experience(self,
                                           teacher_learn_experience_id: int = Query(...,
                                                                                    title="teacher_learn_experienceID",
                                                                                    description="teacher_learn_experienceID",
                                                                                    example=1234)
                                           ):
        # 根据teacher_learn_experience_id调用teacher_learn_experience_rule的get_teacher_learn_experience_by_teacher_learn_experience_id方法获取教师学习经验
        res = await self.teacher_learn_experience_rule.get_teacher_learn_experience_by_teacher_learn_experience_id(
            teacher_learn_experience_id)
        # 返回教师学习经验
        return res

    # 添加教师学习经验
    async def post_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceModel):
        # 调用teacher_learn_experience_rule的add_teacher_learn_experience方法添加教师学习经验
        res = await self.teacher_learn_experience_rule.add_teacher_learn_experience(teacher_learn_experience)
        # 返回添加结果
        return res

    # 根据teacher_learn_experience_id删除教师学习经验
    async def delete_teacher_learn_experience(self,
                                              teacher_learn_experience_id: int = Query(...,
                                                                                       title="teacher_learn_experienceID",
                                                                                       description="teacher_learn_experienceID",
                                                                                       example=1234)
                                              ):
        # 调用teacher_learn_experience_rule的delete_teacher_learn_experience方法删除教师学习经验
        await self.teacher_learn_experience_rule.delete_teacher_learn_experience(teacher_learn_experience_id)
        # 返回删除结果
        return str(teacher_learn_experience_id)

    # 根据teacher_learn_experience_id更新教师学习经验
    async def put_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperienceUpdateModel):
        # 调用teacher_learn_experience_rule的update_teacher_learn_experience方法更新教师学习经验
        res = await self.teacher_learn_experience_rule.update_teacher_learn_experience(teacher_learn_experience)
        # 返回更新结果
        return res

    # 根据teacher_id获取所有教师学习经验
    async def get_teacher_learn_experience_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                             description="teacher_id",
                                                                             example=1234)):
        # 将teacher_id转换为int类型
        teacher_id = int(teacher_id)
        # 调用teacher_learn_experience_rule的get_all_teacher_learn_experience方法获取所有教师学习经验
        return await self.teacher_learn_experience_rule.get_all_teacher_learn_experience(teacher_id)


class TeacherWorkExperienceView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_work_experience_rule = get_injector(TeacherWorkExperienceRule)

    async def get_teacher_work_experience(self,
                                          teacher_work_experience_id: str = Query(...,
                                                                                  title="teacher_work_experienceID",
                                                                                  description="teacher_work_experienceID",
                                                                                  example=1234)
                                          ):
        teacher_work_experience_id = int(teacher_work_experience_id)
        res = await self.teacher_work_experience_rule.get_teacher_work_experience_by_teacher_work_experience_id(
            teacher_work_experience_id)
        return res

    async def post_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceModel):
        res = await self.teacher_work_experience_rule.add_teacher_work_experience(teacher_work_experience)
        return res

    async def delete_teacher_work_experience(self,
                                             teacher_work_experience_id: str = Query(...,
                                                                                     title="teacher_work_experienceID",
                                                                                     description="teacher_work_experienceID",
                                                                                     example=1234)
                                             ):
        teacher_work_experience_id = int(teacher_work_experience_id)
        await self.teacher_work_experience_rule.delete_teacher_work_experience(teacher_work_experience_id)
        return str(teacher_work_experience_id)

    async def put_teacher_work_experience(self, teacher_work_experience: TeacherWorkExperienceUpdateModel):
        res = await self.teacher_work_experience_rule.update_teacher_work_experience(teacher_work_experience)
        return res

    async def get_teacher_work_experience_all(self, teacher_id: str = Query(..., title="teacher_id",
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

    async def get_teacher_job_appointments_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                             description="teacher_id",
                                                                             example=1234)):
        teacher_id = int(teacher_id)
        return await self.teacher_job_appointments_rule.get_all_teacher_job_appointments(teacher_id)

    """
    teacher_job_appointments提交、审核、通过、拒绝 
    """

    async def patch_job_submitting(self, teacher_job_appointments_id: int = Query(...,
                                                                                  title="teacher_job_appointmentsID",
                                                                                  description="teacher_job_appointmentsID",
                                                                                  example=1234)):
        await self.teacher_job_appointments_rule.submitting(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def patch_job_submitted(self, teacher_job_appointments_id: int = Query(...,
                                                                                 title="teacher_job_appointmentsID",
                                                                                 description="teacher_job_appointmentsID",
                                                                                 example=1234)):
        await self.teacher_job_appointments_rule.submitted(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def patch_job_approved(self, teacher_job_appointments_id: int = Query(...,
                                                                                title="teacher_job_appointmentsID",
                                                                                description="teacher_job_appointmentsID",
                                                                                example=1234)):
        await self.teacher_job_appointments_rule.approved(teacher_job_appointments_id)
        return teacher_job_appointments_id

    async def patch_job_rejected(self, teacher_job_appointments_id: int = Query(...,
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
                                                  teacher_id: int|str = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234)):
        teacher_id = int(teacher_id)
        return await self.teacher_professional_titles_rule.get_all_teacher_professional_titles(teacher_id)

    """
    teacher_professional_titles提交、审核、通过、拒绝
    """

    async def patch_professional_submitting(self, teacher_professional_titles_id: int = Query(...,
                                                                                              title="teacher_professional_titlesID",
                                                                                              description="teacher_professional_titlesID",
                                                                                              example=1234)):
        await self.teacher_professional_titles_rule.submitting(teacher_professional_titles_id)
        return teacher_professional_titles_id

    async def patch_professional_submitted(self, teacher_professional_titles_id: int = Query(...,
                                                                                             title="teacher_professional_titlesID",
                                                                                             description="teacher_professional_titlesID",
                                                                                             example=1234)):
        await self.teacher_professional_titles_rule.submitted(teacher_professional_titles_id)
        return teacher_professional_titles_id

    async def patch_professional_approved(self,
                                          teacher_professional_titles_id: int = Query(...,
                                                                                      title="teacher_professional_titlesID",
                                                                                      description="teacher_professional_titlesID",
                                                                                      example=1234)):
        await self.teacher_professional_titles_rule.approved(teacher_professional_titles_id)
        return teacher_professional_titles_id

    async def patch_professional_rejected(self,
                                          teacher_professional_titles_id: int = Query(...,
                                                                                      title="teacher_professional_titlesID",
                                                                                      description="teacher_professional_titlesID",
                                                                                      example=1234)):
        await self.teacher_professional_titles_rule.rejected(teacher_professional_titles_id)
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

    async def get_teacher_qualifications_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                           description="teacher_id",
                                                                           example=1234)):
        teacher_id = int(teacher_id)
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
                                                 teacher_id: int|str = Query(..., title="teacher_id",
                                                                         description="teacher_id",
                                                                         example=1234)):
        teacher_id = int(teacher_id)
        return await self.teacher_skill_certificates_rule.get_all_teacher_skill_certificates(teacher_id)


class TeacherEthicRecordsView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_ethic_records_rule = get_injector(TeacherEthicRecordsRule)

    async def get_teacher_ethic_records(self,
                                        teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                              description="teacher_ethic_recordsID",
                                                                              example=1234)):
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

    async def get_teacher_ethic_records_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234),
                                            ethic_type: str = Query(..., title="ethic_type", description="ethic_type",
                                                                    example="moral")):
        teacher_id = int(teacher_id)
        return await self.teacher_ethic_records_rule.get_all_teacher_ethic_records(teacher_id,ethic_type)

    """
    teacher_ethic_records提交、审核、通过、拒绝
    """

    async def patch_ethic_submitting(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                                 description="teacher_ethic_recordsID",
                                                                                 example=1234)):
        await self.teacher_ethic_records_rule.submitting(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def patch_ethic_submitted(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                                description="teacher_ethic_recordsID",
                                                                                example=1234)):
        await self.teacher_ethic_records_rule.submitted(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def patch_ethic_approved(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
                                                                               description="teacher_ethic_recordsID",
                                                                               example=1234)):
        await self.teacher_ethic_records_rule.approved(teacher_ethic_records_id)
        return teacher_ethic_records_id

    async def patch_ethic_rejected(self, teacher_ethic_records_id: int = Query(..., title="teacher_ethic_recordsID",
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

    async def get_educational_teaching_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                         description="teacher_id",
                                                                         example=1234)):
        teacher_id = int(teacher_id)
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

    async def get_domestic_training_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                      description="teacher_id", example=1234)):
        teacher_id = int(teacher_id)
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

    async def get_overseas_study_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                   description="teacher_id", example=1234)):
        teacher_id = int(teacher_id)
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

    async def get_talent_program_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                   description="teacher_id", example=1234)):
        teacher_id = int(teacher_id)
        return await self.talent_program_rule.get_all_talent_program(teacher_id)

    """
    talent_program提交、审核、通过、拒绝"""

    async def patch_talent_submitting(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                           description="talent_programID",
                                                                           example=1234)):
        await self.talent_program_rule.submitting(talent_program_id)
        return talent_program_id

    async def patch_talent_submitted(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                          description="talent_programID",
                                                                          example=1234)):
        await self.talent_program_rule.submitted(talent_program_id)
        return talent_program_id

    async def patch_talent_approved(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                         description="talent_programID", example=1234)):
        await self.talent_program_rule.approved(talent_program_id)
        return talent_program_id

    async def patch_talent_rejected(self, talent_program_id: int = Query(..., title="talent_programID",
                                                                         description="talent_programID", example=1234)):
        await self.talent_program_rule.rejected(talent_program_id)
        return talent_program_id


class AnnualReviewView(BaseView):
    def __init__(self):
        super().__init__()

        self.annual_review_rule = get_injector(AnnualReviewRule)

    # 定义一个异步函数，用于获取年度评审
    async def get_annual_review(self,
                                # 定义一个参数，类型为int，默认值为Query(..., title="annual_reviewID"，description="annual_reviewID"，example=1234)
                                annual_review_id: int = Query(..., title="annual_reviewID",
                                                              description="annual_reviewID", example=1234)
                                ):
        # 调用annual_review_rule中的get_annual_review_by_annual_review_id函数，传入annual_review_id参数，并将返回值赋给res
        res = await self.annual_review_rule.get_annual_review_by_annual_review_id(annual_review_id)
        # 返回res
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

    async def get_annual_review_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                  description="teacher_id", example=1234)):
        teacher_id = int(teacher_id)
        return await self.annual_review_rule.get_all_annual_review(teacher_id)

    """
    annual_review提交、审核、通过、拒绝
    """

    async def patch_annual_submitting(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                          description="annual_reviewID", example=1234)):
        await self.annual_review_rule.submitting(annual_review_id)
        return annual_review_id

    async def patch_annual_submitted(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                         description="annual_reviewID", example=1234)):
        await self.annual_review_rule.submitted(annual_review_id)
        return annual_review_id

    async def patch_annual_approved(self, annual_review_id: int = Query(..., title="annual_reviewID",
                                                                        description="annual_reviewID", example=1234)):
        await self.annual_review_rule.approved(annual_review_id)
        return annual_review_id

    async def patch_annual_rejected(self, annual_review_id: int = Query(..., title="annual_reviewID",
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

    async def get_research_achievements_all(self, teacher_id: int|str = Query(..., title="teacher_id",
                                                                          description="teacher_id",
                                                                          example=1234)):
        teacher_id = int(teacher_id)
        return await self.research_achievements_rule.get_all_research_achievements(teacher_id)

    # async def page(self, research_achievements=Depends(ResearchAchievementsQueryModel),
    #                page_request=Depends(PageRequest)):
    #     paging_result = await self.research_achievements_rule.query_research_achievements_with_page(
    #         research_achievements, page_request)
    #     return paging_result


class TeacherExtendImportView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_extend_experience_rule = get_injector(TeacherExtendImportRule)
        self.teacher_rule = get_injector(TeachersRule)

    async def post_teacher_work_experience_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                   example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(
            task_type="school_task_teacher_work_experience_import",
            payload=filestorage,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        # await self.teacher_extend_experience_rule.teacher_work_experience_import(file_id)
        return task

    async def post_teacher_learn_experience_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                    example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_learn_experience_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        # await self.teacher_extend_experience_rule.teacher_learn_experience_import(file_id)
        print("发生任务成功")
        return task

    async def post_teacher_job_appointments_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                    example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_job_appointments_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_job_appointments_import(file_id)
        return task

    async def post_teacher_professional_titles_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                       example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_professional_titles_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_professional_titles_import(file_id)
        return task

    async def post_teacher_qualifications_import(self,
                                                 file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_qualifications_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_qualifications_import(file_id)
        return task

    async def post_teacher_skill_certificates_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                      example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_skill_certificates_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_skill_certificates_import(file_id)
        return task

    async def post_teacher_ethic_records_rewards_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                         example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_ethic_records_rewards_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_ethic_records_rewards_import(file_id)
        return task

    async def post_teacher_ethic_records_disciplinary_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                              example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_teacher_ethic_records_disciplinary_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.teacher_ethic_records_disciplinary_import(file_id)
        return task

    async def post_educational_teaching_import(self,
                                               file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_educational_teaching_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        await self.teacher_extend_experience_rule.educational_teaching_import(file_id)
        return task

    async def post_talent_programs_import(self, file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_talent_programs_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.talent_programs_import(file_id)
        return task

    async def post_domestic_training_import(self, file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_domestic_training_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.domestic_training_import(file_id)
        return task

    async def post_overseas_study_import(self, file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_overseas_study_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.overseas_study_import(file_id)
        return task

    async def post_annual_review_import(self, file_id: int | str = Query(..., title="文件id", example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_annual_review_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.annual_review_import(file_id)
        return task

    async def post_research_achievements_project_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                         example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_project_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_project_import(file_id)
        return task

    async def post_research_achievements_book_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                      example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_book_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_book_import(file_id)
        return task

    async def post_research_achievements_paper_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                       example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_paper_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_paper_import(file_id)
        return task

    async def post_research_achievements_reward_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                        example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_reward_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_reward_import(file_id)
        return task

    async def post_research_achievements_artwork_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                         example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_artwork_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_artwork_import(file_id)
        return task

    async def post_research_achievements_patent_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                        example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_patent_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_patent_import(file_id)
        return task

    async def post_research_achievements_competition_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                             example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_competition_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_competition_import(file_id)
        return task

    async def post_research_achievements_medicine_import(self, file_id: int | str = Query(..., title="文件id",
                                                                                          example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(task_type="school_task_research_achievements_medicine_import", payload=filestorage,
                    operator=request_context_manager.current().current_login_account.account_id)
        task = await app.task_topic.send(task)
        print("发生任务成功")
        # await self.teacher_extend_experience_rule.research_achievements_medicine_import(file_id)
        return task
