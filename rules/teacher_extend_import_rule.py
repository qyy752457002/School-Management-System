import shortuuid
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.logging import logger

from business_exceptions.teacher import TeacherNotFoundError
from daos.teachers_dao import TeachersDao
from rules.annual_review_rule import AnnualReviewRule
from rules.common.common_rule import excel_fields_to_enum
from rules.domestic_training_rule import DomesticTrainingRule
from rules.educational_teaching_rule import EducationalTeachingRule
from rules.overseas_study_rule import OverseasStudyRule
from rules.research_achievements_rule import ResearchAchievementsRule
from rules.talent_program_rule import TalentProgramRule
from rules.teacher_ethic_records_rule import TeacherEthicRecordsRule
from rules.teacher_job_appointments_rule import TeacherJobAppointmentsRule
from rules.teacher_learn_experience_rule import TeacherLearnExperienceRule
from rules.teacher_professional_titles_rule import TeacherProfessionalTitlesRule
from rules.teacher_qualifications_rule import TeacherQualificationsRule
from rules.teacher_skill_certificates_rule import TeacherSkillCertificatesRule
from rules.teacher_work_experience_rule import TeacherWorkExperienceRule
from views.models.teacher_extend import AnnualReviewModel, AnnualReviewComModel, AnnualReviewResultModel
from views.models.teacher_extend import DomesticTrainingModel, DomesticTrainingComModel, DomesticTrainingResultModel
from views.models.teacher_extend import EducationalTeachingModel, EducationalTeachingComModel, \
    EducationalTeachingResultModel
from views.models.teacher_extend import OverseasStudyModel, OverseasStudyComModel, OverseasStudyResultModel
from views.models.teacher_extend import ResearchAchievementsArtworkComModel, \
    ResearchAchievementsArtworkResultModel
from views.models.teacher_extend import ResearchAchievementsBookComModel, \
    ResearchAchievementsBookResultModel
from views.models.teacher_extend import ResearchAchievementsCompetitionComModel, \
    ResearchAchievementsCompetitionResultModel
from views.models.teacher_extend import ResearchAchievementsMedicineComModel, \
    ResearchAchievementsMedicineResultModel
from views.models.teacher_extend import ResearchAchievementsModel, ResearchAchievementsPaperComModel, \
    ResearchAchievementsPaperResultModel
from views.models.teacher_extend import ResearchAchievementsPatentComModel, \
    ResearchAchievementsPatentResultModel
from views.models.teacher_extend import ResearchAchievementsProjectComModel, \
    ResearchAchievementsProjectResultModel
from views.models.teacher_extend import ResearchAchievementsRewardComModel, \
    ResearchAchievementsRewardResultModel
from views.models.teacher_extend import TalentProgramModel, TalentProgramComModel, TalentProgramResultModel
from views.models.teacher_extend import TeacherEthicRecordsDisciplinaryComModel, \
    TeacherEthicRecordsDisciplinaryResultModel
from views.models.teacher_extend import TeacherEthicRecordsModel, TeacherEthicRecordsRewardsComModel, \
    TeacherEthicRecordsRewardsResultModel
from views.models.teacher_extend import TeacherEthicType
from views.models.teacher_extend import TeacherJobAppointmentsModel, TeacherJobAppointmentsComModel, \
    TeacherJobAppointmentsResultModel
from views.models.teacher_extend import TeacherLearnExperienceModel, TeacherLearnExperienceComModel, \
    TeacherLearnExperienceResultModel
from views.models.teacher_extend import TeacherProfessionalTitlesModel, TeacherProfessionalTitlesComModel, \
    TeacherProfessionalTitlesResultModel
from views.models.teacher_extend import TeacherQualificationsModel, TeacherQualificationsComModel, \
    TeacherQualificationsResultModel
from views.models.teacher_extend import TeacherSkillCertificatesModel, TeacherSkillCertificatesComModel, \
    TeacherSkillCertificatesResultModel
from views.models.teacher_extend import TeacherWorkExperienceModel, TeacherWorkExperienceComModel, \
    TeacherWorkExperienceResultModel
from views.models.teachers import IdentityType
from views.models.teachers import TeacherFileStorageModel


@dataclass_inject
class TeacherExtendImportRule:
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    teacher_dao: TeachersDao

    async def teacher_work_experience_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("参数错误")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            # local_file_path = "rules/tmp/教职工工作经历导入模版1.xlsx"
            logger.info("Test开始注册模型")
            storage_manager.download_file(
                source_file.virtual_bucket_name, source_file.file_name, local_file_path
            )
            reader = ExcelReader()
            reader.set_data(local_file_path)
            reader.register_model("数据", TeacherWorkExperienceComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherWorkExperienceResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item,
                                                           "import_teacher_work_experience")
                    teacher_work_experience_data = {key: data_dict[key] for key in
                                                    TeacherWorkExperienceModel.__fields__.keys()}
                    teacher_work_experience_model = TeacherWorkExperienceModel(**teacher_work_experience_data)

                    teacher_work_experience_rule = get_injector(TeacherWorkExperienceRule)
                    await teacher_work_experience_rule.add_teacher_work_experience(teacher_work_experience_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, '表内数据异常')
                    raise ex
            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()
            random_file_name = shortuuid.uuid()
            file_storage = storage_manager.put_file_to_object(
                source_file.virtual_bucket_name, f"{random_file_name}.xlsx", local_results_path
            )
            file_storage_resp = await storage_manager.add_file(
                self.file_storage_dao, file_storage
            )
            return file_storage_resp
        except Exception as e:
            print(e, '异常')
            raise e

    async def teacher_learn_experience_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工学习经历导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherLearnExperienceComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherLearnExperienceResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_learn_experience")
                    teacher_learn_experience_data = {key: data_dict[key] for key in
                                                     TeacherLearnExperienceModel.__fields__.keys()}
                    teacher_learn_experience_model = TeacherLearnExperienceModel(**teacher_learn_experience_data)
                    teacher_learn_experience_rule = get_injector(TeacherLearnExperienceRule)
                    await teacher_learn_experience_rule.add_teacher_learn_experience(teacher_learn_experience_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx", local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_job_appointments_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工学习经历导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherJobAppointmentsComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherJobAppointmentsResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_job_appointments")
                    teacher_job_appointments_data = {key: data_dict[key] for key in
                                                     TeacherJobAppointmentsModel.__fields__.keys()}
                    teacher_job_appointments_model = TeacherJobAppointmentsModel(**teacher_job_appointments_data)
                    teacher_job_appointments_rule = get_injector(TeacherJobAppointmentsRule)
                    await teacher_job_appointments_rule.add_teacher_job_appointments(teacher_job_appointments_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_professional_titles_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工专业技术职务聘任导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherProfessionalTitlesComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherProfessionalTitlesResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_professional_titles")
                    teacher_professional_titles_data = {key: data_dict[key] for key in
                                                        TeacherProfessionalTitlesModel.__fields__.keys()}
                    teacher_professional_titles_model = TeacherProfessionalTitlesModel(
                        **teacher_professional_titles_data)
                    teacher_professional_titles_rule = get_injector(TeacherProfessionalTitlesRule)
                    await teacher_professional_titles_rule.add_teacher_professional_titles(
                        teacher_professional_titles_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_qualifications_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工教师资格证导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherQualificationsComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherQualificationsResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_qualifications")
                    teacher_qualifications_data = {key: data_dict[key] for key in
                                                   TeacherQualificationsModel.__fields__.keys()}
                    teacher_qualifications_model = TeacherQualificationsModel(**teacher_qualifications_data)
                    teacher_qualifications_rule = get_injector(TeacherQualificationsRule)
                    await teacher_qualifications_rule.add_teacher_qualifications(teacher_qualifications_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_skill_certificates_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工技能证书导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherSkillCertificatesComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherSkillCertificatesResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_skill_certificates")
                    teacher_skill_certificates_data = {key: data_dict[key] for key in
                                                       TeacherSkillCertificatesModel.__fields__.keys()}
                    teacher_skill_certificates_model = TeacherSkillCertificatesModel(**teacher_skill_certificates_data)
                    teacher_skill_certificates_rule = get_injector(TeacherSkillCertificatesRule)
                    await teacher_skill_certificates_rule.add_teacher_skill_certificates(
                        teacher_skill_certificates_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_ethic_records_rewards_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工师德信息导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherEthicRecordsRewardsComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherEthicRecordsRewardsResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_ethic_records_rewards")
                    data_dict["ethic_type"] = TeacherEthicType.ETHIC.value
                    teacher_ethic_records_rewards_data = {key: data_dict[key] for key in
                                                          TeacherEthicRecordsModel.__fields__.keys() if
                                                          key in data_dict}
                    teacher_ethic_records_rewards_model = TeacherEthicRecordsModel(**teacher_ethic_records_rewards_data)
                    teacher_ethic_records_rewards_rule = get_injector(TeacherEthicRecordsRule)
                    await teacher_ethic_records_rewards_rule.add_teacher_ethic_records(
                        teacher_ethic_records_rewards_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def teacher_ethic_records_disciplinary_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工处分信息导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TeacherEthicRecordsDisciplinaryComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherEthicRecordsDisciplinaryResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_teacher_ethic_records_disciplinary")
                    data_dict["ethic_type"] = TeacherEthicType.PUNISH.value
                    teacher_ethic_records_disciplinary_data = {key: data_dict[key] for key in
                                                               TeacherEthicRecordsModel.__fields__.keys() if
                                                               key in data_dict}
                    teacher_ethic_records_disciplinary_model = TeacherEthicRecordsModel(
                        **teacher_ethic_records_disciplinary_data)
                    teacher_ethic_records_disciplinary_rule = get_injector(TeacherEthicRecordsRule)
                    await teacher_ethic_records_disciplinary_rule.add_teacher_ethic_records(
                        teacher_ethic_records_disciplinary_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def educational_teaching_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工学习经历导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", EducationalTeachingComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = EducationalTeachingResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_educational_teaching")
                    educational_teaching_data = {key: data_dict[key] for key in
                                                 EducationalTeachingModel.__fields__.keys()}
                    educational_teaching_model = EducationalTeachingModel(**educational_teaching_data)
                    educational_teaching_rule = get_injector(EducationalTeachingRule)
                    await educational_teaching_rule.add_educational_teaching(educational_teaching_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def talent_programs_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工人才项目导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", TalentProgramComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = TalentProgramResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_talent_programs")
                    talent_programs_data = {key: data_dict[key] for key in TalentProgramModel.__fields__.keys()}
                    talent_programs_model = TalentProgramModel(**talent_programs_data)
                    talent_programs_rule = get_injector(TalentProgramRule)
                    await talent_programs_rule.add_talent_program(talent_programs_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def domestic_training_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工学习经历导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", DomesticTrainingComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = DomesticTrainingResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_domestic_training")
                    domestic_training_data = {key: data_dict[key] for key in DomesticTrainingModel.__fields__.keys()}
                    domestic_training_model = DomesticTrainingModel(**domestic_training_data)
                    domestic_training_rule = get_injector(DomesticTrainingRule)
                    await domestic_training_rule.add_domestic_training(domestic_training_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def overseas_study_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            local_file_path = "rules/tmp/教职工海外研修导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", OverseasStudyComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = OverseasStudyResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_overseas_study")
                    overseas_study_data = {key: data_dict[key] for key in OverseasStudyModel.__fields__.keys()}
                    overseas_study_model = OverseasStudyModel(**overseas_study_data)
                    overseas_study_rule = get_injector(OverseasStudyRule)
                    await overseas_study_rule.add_overseas_study(overseas_study_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def annual_review_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工年度考核导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", AnnualReviewComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = AnnualReviewResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_annual_review")
                    annual_review_data = {key: data_dict[key] for key in AnnualReviewModel.__fields__.keys()}
                    annual_review_model = AnnualReviewModel(**annual_review_data)
                    annual_review_rule = get_injector(AnnualReviewRule)
                    await annual_review_rule.add_annual_review(annual_review_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_project_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工科研项目导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsProjectComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsProjectResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_project")
                    data_dict["research_achievement_type"] = "1"
                    research_achievements_project_data = {key: data_dict[key] for key in
                                                          ResearchAchievementsModel.__fields__.keys() if
                                                          key in data_dict}
                    research_achievements_project_model = ResearchAchievementsModel(
                        **research_achievements_project_data)
                    research_achievements_project_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_project_rule.add_research_achievements(
                        research_achievements_project_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_book_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工著作信息导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsBookComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsBookResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_book")
                    data_dict["research_achievement_type"] = "2"
                    research_achievements_book_data = {key: data_dict[key] for key in
                                                       ResearchAchievementsModel.__fields__.keys() if key in data_dict}
                    research_achievements_book_model = ResearchAchievementsModel(**research_achievements_book_data)
                    research_achievements_book_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_book_rule.add_research_achievements(research_achievements_book_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_paper_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工论文导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsPaperComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsPaperResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_paper")
                    data_dict["research_achievement_type"] = "3"
                    research_achievements_paper_data = {key: data_dict[key] for key in
                                                        ResearchAchievementsModel.__fields__.keys() if key in data_dict}
                    research_achievements_paper_model = ResearchAchievementsModel(
                        **research_achievements_paper_data)
                    research_achievements_paper_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_paper_rule.add_research_achievements(research_achievements_paper_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_reward_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工奖励导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsRewardComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsRewardResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_reward")
                    data_dict["research_achievement_type"] = "4"
                    research_achievements_reward_data = {key: data_dict[key] for key in
                                                         ResearchAchievementsModel.__fields__.keys() if
                                                         key in data_dict}
                    research_achievements_reward_model = ResearchAchievementsModel(
                        **research_achievements_reward_data)
                    research_achievements_reward_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_reward_rule.add_research_achievements(
                        research_achievements_reward_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_artwork_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工文艺作品导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsArtworkComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsArtworkResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_artwork")
                    data_dict["research_achievement_type"] = "5"
                    research_achievements_artwork_data = {key: data_dict[key] for key in
                                                          ResearchAchievementsModel.__fields__.keys() if
                                                          key in data_dict}
                    research_achievements_artwork_model = ResearchAchievementsModel(
                        **research_achievements_artwork_data)
                    research_achievements_artwork_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_artwork_rule.add_research_achievements(
                        research_achievements_artwork_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_patent_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工专利或软件著作权导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsPatentComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsPatentResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_patent")
                    data_dict["research_achievement_type"] = "6"
                    research_achievements_patent_data = {key: data_dict[key] for key in
                                                         ResearchAchievementsModel.__fields__.keys() if
                                                         key in data_dict}
                    research_achievements_patent_model = ResearchAchievementsModel(
                        **research_achievements_patent_data)
                    research_achievements_patent_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_patent_rule.add_research_achievements(
                        research_achievements_patent_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_competition_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工竞赛奖励导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsCompetitionComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsCompetitionResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_competition")
                    data_dict["research_achievement_type"] = "10"
                    research_achievements_competition_data = {key: data_dict[key] for key in
                                                              ResearchAchievementsModel.__fields__.keys() if
                                                              key in data_dict}
                    research_achievements_competition_model = ResearchAchievementsModel(
                        **research_achievements_competition_data)
                    research_achievements_competition_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_competition_rule.add_research_achievements(
                        research_achievements_competition_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e

    async def research_achievements_medicine_import(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("Invalid payload type")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(source_file.virtual_bucket_name, source_file.file_name, local_file_path)
            # local_file_path = "rules/tmp/教职工医药导入模版1.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            logger.info("Test开始注册模型")
            reader.register_model("数据", ResearchAchievementsMedicineComModel, header=1)
            logger.info("Test开始读取模型")
            data = reader.execute()["数据"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []
            for idx, item in enumerate(data):
                item = item.dict()
                result_dict = item.copy()
                result_dict["failed_msg"] = "成功"
                result = ResearchAchievementsMedicineResultModel(**result_dict)
                teacher_id_number = item.get("teacher_id_number")
                teacher_id_type = item.get("teacher_id_type")
                teacher_id_type = IdentityType.from_chinese(teacher_id_type).value
                teacher_name = item.get("teacher_name")
                try:
                    teacher_db = await self.teacher_dao.get_teacher_by_params(teacher_id_number, teacher_id_type,
                                                                              teacher_name)
                    if not teacher_db:
                        raise TeacherNotFoundError()
                    item["teacher_id"] = teacher_db.teacher_id
                    data_dict = await excel_fields_to_enum(item, "import_research_achievements_medicine")
                    data_dict["research_achievement_type"] = "8"
                    research_achievements_medicine_data = {key: data_dict[key] for key in
                                                           ResearchAchievementsModel.__fields__.keys() if
                                                           key in data_dict}
                    research_achievements_medicine_model = ResearchAchievementsModel(
                        **research_achievements_medicine_data)
                    research_achievements_medicine_rule = get_injector(ResearchAchievementsRule)
                    await research_achievements_medicine_rule.add_research_achievements(
                        research_achievements_medicine_model)
                except Exception as ex:
                    result.failed_msg = str(ex)
                    results.append(result)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, "表内数据异常")
                    raise ex

            local_results_path = f"/tmp/{source_file.file_name}"
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", results)
            excel_writer.set_data(local_results_path)
            excel_writer.execute()

            random_file_name = shortuuid.uuid() + ".xlsx"
            file_storage = storage_manager.put_file_to_object(source_file.virtual_bucket_name,
                                                              f"{random_file_name}.xlsx",
                                                              local_results_path)
            file_storage_resp = await storage_manager.add_file(self.file_storage_dao, file_storage)

            return file_storage_resp
        except Exception as e:
            print(e, "异常")
            raise e
