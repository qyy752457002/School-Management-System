from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from datetime import datetime
from business_exceptions.common import IdCardError
from daos.teachers_dao import TeachersDao
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers import Teacher
from views.common.common_view import check_id_number
from views.models.teachers import Teachers as TeachersModel
from views.models.teachers import TeachersCreatModel, TeacherInfoCreateModel, TeacherCreateResultModel, CombinedModel, \
    TeacherInfoCreateResultModel, TeacherFileStorageModel
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from views.models.teacher_transaction import TeacherAddModel, TeacherAddReModel
from rules.teachers_info_rule import TeachersInfoRule

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.storage.view_model import FileStorageModel
from mini_framework.utils.logging import logger


@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao
    teachers_info_dao: TeachersInfoDao
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    teachers_info_rule: TeachersInfoRule

    async def get_teachers_by_id(self, teachers_id):
        teacher_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teacher_db:
            raise TeacherNotFoundError()
        # 可选 ,
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        return teachers

    # async def get_teachers_by_username(self, username):
    #     teacher_db = await self.teachers_dao.get_teachers_by_username(username)
    #     teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
    #     return teachers
    async def get_teachers_by_teacher_id_number(self, teacher_id_number):
        teacher_db = await self.teachers_dao.get_teachers_by_teacher_id_number(teacher_id_number)
        if not teacher_db:
            raise TeacherNotFoundError()
        teachers = orm_model_to_view_model(teacher_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def add_teachers(self, teachers: TeachersCreatModel):
        teacher_id_number = teachers.teacher_id_number
        teacher_id_type = teachers.teacher_id_type
        teacher_name = teachers.teacher_name
        teacher_gender = teachers.teacher_gender
        length = await self.teachers_info_dao.get_teachers_info_by_prams(teacher_id_number, teacher_id_type,
                                                                         teacher_name, teacher_gender)
        if length > 0:
            raise TeacherExistsError()
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def add_transfer_teachers(self, teachers: TeacherAddModel):
        """
        系统外调入系统内时使用，增加老师
        """
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers = orm_model_to_view_model(teachers_db, TeacherAddReModel, exclude=[""])
        return teachers

    async def update_teachers(self, teachers):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        need_update_list = []
        for key, value in teachers.dict().items():
            if value:
                need_update_list.append(key)
        teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return teachers

    async def delete_teachers(self, teachers_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        teachers_db = await self.teachers_dao.delete_teachers(exists_teachers)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        return teachers

    async def get_all_teachers(self):
        teachers_db = await self.teachers_dao.get_all_teachers()
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def get_teachers_count(self):
        teachers_count = await self.teachers_dao.get_teachers_count()
        return teachers_count

    async def submitting(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "submitting"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def submitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "submitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def approved(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "approved"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def rejected(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_approval_status = "rejected"
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def recall(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_approval_status == "submitted":
            teachers.teacher_approval_status = "submitting"
        else:
            raise Exception("只有待审核的教师信息才能撤回")
        return await self.teachers_dao.update_teachers(teachers, "teacher_approval_status")

    async def teacher_active(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "active":
            teachers.teacher_sub_status = "active"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")

    # 导入相关
    async def import_teachers(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("参数错误")
            # source_file = task.payload
            # local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            # storage_manager.download_file(
            #     source_file.bucket_name, source_file.file_name, local_file_path
            # )
            local_file_path = "c.xlsx"
            reader = ExcelReader()
            reader.set_data(local_file_path)
            # reader.register_model("Sheet1", CombinedModel)
            logger.info("Test开始注册模型")
            reader.register_model("Sheet1", TeachersCreatModel)
            # reader.register_model("Sheet1", TeacherInfoCreateModel)
            logger.info("Test开始读取模型")
            data = reader.execute()["Sheet1"]
            if not isinstance(data, list):
                raise ValueError("数据格式错误")
            results = []

            # 两个一起写
            # for idx, item in enumerate(data):
            #     teacher_data = {key: item[key] for key in TeachersCreatModel.__fields__.keys() if key in item}
            #     teacher_model = TeachersCreatModel(**teacher_data)
            #
            #     result_dict = teacher_data.copy()
            #     result_dict["failed_msg"] = "成功"
            #     result = TeacherCreateResultModel(**result_dict)
            #     try:
            #         teacher = await self.add_teachers(teacher_model)
            #         teacher_id = teacher.teacher_id
            #     except Exception as ex:
            #         result.failed_msg = str(ex)
            #     results.append(result)
            #
            #     if teacher_id:
            #         info_data = {key: item[key] for key in TeacherInfoCreateModel.__fields__.keys()}
            #         info_data["teacher_id"] = teacher_id
            #         info_model = TeacherInfoCreateModel(**info_data)
            #
            #         info_result_dict = info_data.copy()
            #         info_result_dict["failed_msg"] = "成功"
            #         info_result = TeacherInfoCreateResultModel(**info_result_dict)
            #
            #         try:
            #             await self.teachers_info_rule.add_teachers_info_import(info_model)
            #         except Exception as ex:
            #             info_result.failed_msg = str(ex)
            #
            #         results.append(info_result)

            for idx, item in enumerate(data):
                item = item.dict()
                teacher_data = {key: item[key] for key in TeachersCreatModel.__fields__.keys() if key in item}
                logger.info(teacher_data)
                teacher_model = TeachersCreatModel(**teacher_data)
                logger.info(type(teacher_data))

                result_dict = teacher_data.copy()
                result_dict["failed_msg"] = "成功"
                result = TeacherCreateResultModel(**result_dict)
                try:
                    await self.add_teachers(teacher_model)

                except Exception as ex:
                    result.failed_msg = str(ex)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, '表内数据异常')
                    raise ex
                results.append(result)

            # local_results_path = f"/tmp/{source_file.file_name}"
            # excel_writer = ExcelWriter()
            # excel_writer.add_data("Sheet1", results)
            # excel_writer.set_data(local_results_path)
            # excel_writer.execute()
            #
            # random_file_name = shortuuid.uuid() + ".xlsx"
            # file_storage = await storage_manager.put_file_to_object(
            #     source_file.bucket_name, f"{random_file_name}.xlsx", local_results_path
            # )
            # file_storage_resp = await storage_manager.add_file(
            #     self.file_storage_dao, file_storage
            # )
            #
            # task_result = TaskResult()
            # task_result.task_id = task.task_id
            # task_result.result_file = file_storage_resp.file_name
            # task_result.result_bucket = file_storage_resp.bucket_name
            # task_result.result_file_id = file_storage_resp.file_id
            # task_result.last_updated = datetime.now()
            # task_result.state = TaskState.succeeded
            # task_result.result_extra = {"file_size": 123}
            #
            # await self.task_dao.add_task_result(task_result)
            # return task_result
        except Exception as e:
            print(e, '异常')
            raise e

