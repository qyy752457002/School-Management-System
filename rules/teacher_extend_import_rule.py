from views.models.teachers import IdentityType
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from datetime import datetime
from views.models.teachers import TeacherFileStorageModel

from views.models.teacher_extend import TeacherWorkExperienceModel, TeacherWorkExperienceComModel, \
    TeacherWorkExperienceResultModel

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.storage.manager import storage_manager
from mini_framework.utils.logging import logger

from rules.common.common_rule import convert_fields_to_str, excel_fields_to_enum

from rules.teachers_info_rule import TeachersInfoRule
from rules.teachers_rule import TeachersRule
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from daos.organization_dao import OrganizationDAO
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError
from rules.teacher_work_experience_rule import TeacherWorkExperienceRule
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector


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


