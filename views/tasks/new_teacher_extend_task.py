from mini_framework.async_task.consumers import TaskExecutor
from mini_framework.async_task.task.task_context import Task, Context
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.logging import logger

from views.models.teachers import TeacherFileStorageModel
from rules.teacher_extend_import_rule import TeacherExtendImportRule


class TeacherLearnExperienceImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_learn_experience_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_learn_experience_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_learn_experience_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_learn_experience导入失败")
            logger.error(e)
            raise e


class TeacherWorkExperienceImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task = context
            logger.info("Test")
            logger.info("Teacher work experience import begins")
            task: Task = task
            logger.info("Test2")
            if isinstance(task.payload, dict):
                teacher_work_experience_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_work_experience_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_work_experience_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")

        except Exception as e:
            logger.error(f"Teacher work experience import failed")
            logger.error(e)
            raise e


class TeacherJobAppointmentsImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_job_appointments_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_job_appointments_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_job_appointments_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_job_appointments导入失败")
            logger.error(e)
            raise e


class TeacherProfessionalTitlesImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_professional_titles_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_professional_titles_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_professional_titles_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_professional_titles导入失败")
            logger.error(e)
            raise e


class TeacherQualificationsImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_qualifications_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_qualifications_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_qualifications_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_qualifications导入失败")
            logger.error(e)
            raise e


class TeacherSkillCertificatesImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_skill_certificates_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_skill_certificates_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_skill_certificates_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_skill_certificates导入失败")
            logger.error(e)
            raise e


class TeacherEthicRecordsRewardsImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_ethic_records_rewards_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_ethic_records_rewards_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_ethic_records_rewards_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_ethic_records_rewards导入失败")
            logger.error(e)
            raise e


class TeacherEthicRecordsDisciplinaryImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                teacher_ethic_records_disciplinary_import: TeacherFileStorageModel = TeacherFileStorageModel(
                    **task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                teacher_ethic_records_disciplinary_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.teacher_ethic_records_disciplinary_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("teacher_ethic_records_disciplinary导入失败")
            logger.error(e)
            raise e


class EducationalTeachingImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                educational_teaching_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                educational_teaching_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.educational_teaching_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("educational_teaching导入失败")
            logger.error(e)
            raise e


class TalentProgramsImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                talent_programs_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                talent_programs_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.talent_programs_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("talent_programs导入失败")
            logger.error(e)
            raise e


class DomesticTrainingImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                domestic_training_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                domestic_training_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.domestic_training_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("domestic_training导入失败")
            logger.error(e)
            raise e


class OverseasStudyImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                overseas_study_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                overseas_study_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.overseas_study_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("overseas_study导入失败")
            logger.error(e)
            raise e


class AnnualReviewImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                annual_review_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                annual_review_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.annual_review_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("annual_review导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsProjectImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_project_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_project_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_project_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_project导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsBookImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_book_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_book_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_book_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_book导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsPaperImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_paper_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_paper_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_paper_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_paper导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsRewardImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_reward_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_reward_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_reward_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_reward导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsArtworkImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_artwork_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_artwork_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_artwork_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_artwork导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsPatentImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_patent_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_patent_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_patent_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_patent导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsCompetitionImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_competition_import: TeacherFileStorageModel = TeacherFileStorageModel(
                    **task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_competition_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_competition_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_competition导入失败")
            logger.error(e)
            raise e


class ResearchAchievementsMedicineImportExecutor(TaskExecutor):
    def __init__(self):
        self.teacher_extend_import_rule = get_injector(TeacherExtendImportRule)
        super().__init__()

    async def execute(self, context: "Context"):
        try:
            task: Task = context
            logger.info("Test")
            if isinstance(task.payload, dict):
                research_achievements_medicine_import: TeacherFileStorageModel = TeacherFileStorageModel(**task.payload)
            elif isinstance(task.payload, TeacherFileStorageModel):
                research_achievements_medicine_import: TeacherFileStorageModel = task.payload
            else:
                raise ValueError("Invalid payload type")
            logger.info("Test3")
            file_storage_resp = await self.teacher_extend_import_rule.research_achievements_medicine_import(task)
            task.result_file = file_storage_resp.file_name
            task.result_bucket = file_storage_resp.virtual_bucket_name
            logger.info("成功")
        except Exception as e:
            logger.error("research_achievements_medicine导入失败")
            logger.error(e)
            raise e
