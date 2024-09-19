# from rules.teachers_info_rule import TeachersInfoRule
import os
from datetime import datetime
import sys
import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.logging import logger
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.school import SchoolNotFoundError
from daos.organization_dao import OrganizationDAO
from daos.school_dao import SchoolDAO
from daos.teachers_info_dao import TeachersInfoDao
from models.public_enum import OrgIdentityType, OrgIdentity
from rules.common.common_rule import excel_fields_to_enum
from rules.teachers_info_rule import TeachersInfoRule
from rules.teachers_rule import TeachersRule
# from rules.teachers_info_rule import TeachersInfoRule
from views.models.teachers import CombinedModel
from views.models.teachers import TeacherImportSaveResultModel, \
    TeacherFileStorageModel, CurrentTeacherQuery, CurrentTeacherQueryRe, \
    TeachersSaveImportCreatModel, TeacherImportResultModel, \
    TeacherInfoImportSubmit, TeachersSaveImportRegisterCreatTestModel, TeachersSaveImportRegisterCreatTestTestModel, \
    TeachersSaveImportCreatTestModel


class TeacherSyncRule:
    def __init__(self):
        self.school_dao = get_injector(SchoolDAO)
        self.organization_dao = get_injector(OrganizationDAO)
        self.teacher_rule = get_injector(TeachersRule)

    async def import_teachers_save_test(self):
        teacher_id_list = ["12345678890"]
        print(teacher_id_list)
        file_name=sys.argv[2]
        # local_file_path = os.path.join("rules", file_name)
        local_file_path = os.path.join("rules", "821.xlsx")
        teacher_id_list = []
        reader = ExcelReader()
        reader.set_data(local_file_path)
        logger.info("Test开始注册模型")
        reader.register_model("Sheet1", TeachersSaveImportRegisterCreatTestTestModel, header=1)
        logger.info("Test开始读取模型")
        data = reader.execute()["Sheet1"]
        if not isinstance(data, list):
            raise ValueError("数据格式错误")
        for idx, item in enumerate(data):
            item = item.dict()
            school = await self.school_dao.get_school_by_school_name(item["teacher_employer"])
            if school:
                school = school._asdict()['School']
                item["teacher_employer"] = school.id
                org_name = item["org_id"]
                organization = await self.organization_dao.get_organization_by_name_and_school_id(
                    org_name, school.id)
                if organization:
                    org_id = str(organization.id)
                    item["org_id"] = org_id
            else:
                raise SchoolNotFoundError()
            teacher_identity_type = OrgIdentityType.from_chinese(item["identity_type"])
            teacher_identity = OrgIdentity.from_chinese(item["identity"])
            teacher_model = TeachersSaveImportCreatTestModel(**item)
            logger.info(type(item))
            try:
                await self.teacher_rule.add_teachers_import_to_org(teacher_model, teacher_identity_type,
                                                                   teacher_identity)
            except Exception as ex:
                return ex
        return True


@dataclass_inject
class TeacherImportRule:
    school_dao: SchoolDAO
    teacher_rule: TeachersRule
    teachers_info_rule: TeachersInfoRule
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    organization_dao: OrganizationDAO
    teachers_info_dao: TeachersInfoDao

    # 导入导出相关
    async def import_teachers(self, task: Task):

        if not isinstance(task.payload, TeacherFileStorageModel):
            raise ValueError("参数错误")
        source_file = task.payload
        local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
        logger.info("Test开始注册模型")
        storage_manager.download_file(
            source_file.virtual_bucket_name, source_file.file_name, local_file_path
        )
        reader = ExcelReader()
        reader.set_data(local_file_path)
        reader.register_model("数据", CombinedModel, header=1)
        logger.info("Test开始注册模型")
        # reader.register_model("Sheet1", TeachersCreatModel)
        # reader.register_model("Sheet1", TeacherInfoCreateModel)
        logger.info("Test开始读取模型")
        data = reader.execute()["数据"]
        if not isinstance(data, list):
            raise ValueError("数据格式错误")
        results = []
        # 两个一起写
        for idx, item in enumerate(data):
            item = item.dict()
            result_dict = item.copy()
            result_dict["failed_msg"] = "成功"
            result = TeacherImportResultModel(**result_dict)
            school = await self.school_dao.get_school_by_school_name(item["teacher_employer"])
            if school:
                school = school._asdict()['School']
                item["teacher_employer"] = school.id
            else:
                raise SchoolNotFoundError()
            organization = await self.organization_dao.get_organization_by_name_and_school_id(
                item["department"], item["teacher_employer"])
            if organization:
                item["department"] = str(organization.id)
            # 这里保证生成模型
            item["org_id"] = item["department"]
            teacher_data = {key: item[key] for key in TeachersSaveImportCreatModel.__fields__.keys()}
            teacher_model = TeachersSaveImportCreatModel(**teacher_data)
            user_id = task.operator
            try:
                teachers_work, teacher_base_id = await self.teacher_rule.add_teachers_import_save(teacher_model,
                                                                                                  user_id)
                teacher_id = int(teachers_work.teacher_id)
                teacher_base_id = int(teacher_base_id)
                if teacher_id:
                    # info_data = {key: item[key] for key in TeacherInfoSubmit.__fields__.keys() if key in item}
                    # info_data["teacher_id"] = teacher_id
                    # info_data["teacher_base_id"] = teacher_base_id
                    item["teacher_id"] = teacher_id
                    item["teacher_base_id"] = teacher_base_id
                    info_data = {key: item[key] for key in TeacherInfoImportSubmit.__fields__.keys() if key in item}
                    data_dict = await excel_fields_to_enum(info_data, "import_teacher")
                    info_model = TeacherInfoImportSubmit(**data_dict)
                    await self.teachers_info_rule.update_teachers_info_import(info_model, user_id)
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
        # task_result = TaskResult()
        # task_result.task_id = task.task_id
        # task_result.result_file = file_storage_resp.file_name
        # task_result.result_bucket = file_storage_resp.virtual_bucket_name
        # task_result.result_file_id = file_storage_resp.file_id
        # task_result.last_updated = datetime.now()
        # task_result.state = TaskState.succeeded
        # task_result.result_extra = {"file_size": file_storage.file_size}
        # await self.task_dao.add_task_result(task_result)
        return file_storage_resp

    async def import_teachers_save(self, task: Task):
        if not isinstance(task.payload, TeacherFileStorageModel):
            raise ValueError("参数错误")
        source_file = task.payload
        local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
        logger.info("Test开始注册模型")
        storage_manager.download_file(
            source_file.virtual_bucket_name, source_file.file_name, local_file_path
        )
        reader = ExcelReader()
        reader.set_data(local_file_path)
        logger.info("Test开始注册模型")
        # reader.register_model("数据", TeachersSaveImportRegisterCreatModel, header=1)
        reader.register_model("沈阳市教育研究院", TeachersSaveImportRegisterCreatTestModel, header=0)
        # reader.register_model("Sheet1", TeacherInfoCreateModel)
        logger.info("Test开始读取模型")
        data = reader.execute()["沈阳市教育研究院"]
        if not isinstance(data, list):
            raise ValueError("数据格式错误")
        results = []

        for idx, item in enumerate(data):
            item = item.dict()
            # teacher_data = {key: item[key] for key in TeachersSaveImportCreatModel.__fields__.keys() if key in item}
            school = await self.school_dao.get_school_by_school_name(item["teacher_employer"])
            if school:
                school = school._asdict()['School']
                item["teacher_employer"] = school.id
            else:
                raise SchoolNotFoundError()
            logger.info(item)
            teacher_model = TeachersSaveImportCreatModel(**item)
            logger.info(type(item))
            result_dict = item.copy()
            result_dict["failed_msg"] = "成功"
            result = TeacherImportSaveResultModel(**result_dict)
            user_id = task.operator
            try:
                await self.teacher_rule.add_teachers_import_save(teacher_model, user_id)
            except Exception as ex:
                result.failed_msg = str(ex)
                logger.info(f"Failed to add teacher at index {idx}: {ex}")
                print(ex, '表内数据异常')
            results.append(result)

        local_results_path = f"/tmp/{source_file.file_name}"
        excel_writer = ExcelWriter()
        excel_writer.add_data("Sheet1", results)
        excel_writer.set_data(local_results_path)
        excel_writer.execute()

        random_file_name = shortuuid.uuid() + ".xlsx"
        file_storage = storage_manager.put_file_to_object(
            source_file.virtual_bucket_name, f"{random_file_name}", local_results_path
        )
        file_storage_resp = await storage_manager.add_file(
            self.file_storage_dao, file_storage
        )
        # task_result = TaskResult()
        # task_result.task_id = task.task_id
        # task_result.result_file = file_storage_resp.file_name
        # task_result.result_bucket = file_storage_resp.bucket_name
        # task_result.result_file_id = file_storage_resp.file_id
        # task_result.last_updated = datetime.now()
        # task_result.state = TaskState.succeeded
        # task_result.result_extra = {"file_size": file_storage.file_size}
        # await self.task_dao.add_task_result(task_result)
        return file_storage_resp

    async def import_teachers_save_test(self):
        teacher_id_list = ["12345678890"]
        print(teacher_id_list)
        # local_file_path = os.path.join("rules", "821.xlsx")
        # teacher_id_list = []
        # reader = ExcelReader()
        # reader.set_data(local_file_path)
        # logger.info("Test开始注册模型")
        # reader.register_model("Sheet1", TeachersSaveImportRegisterCreatTestTestModel, header=1)
        # logger.info("Test开始读取模型")
        # data = reader.execute()["Sheet1"]
        # if not isinstance(data, list):
        #     raise ValueError("数据格式错误")
        # for idx, item in enumerate(data):
        #     item = item.dict()
        #     school = await self.school_dao.get_school_by_school_name(item["teacher_employer"])
        #     if school:
        #         school = school._asdict()['School']
        #         item["teacher_employer"]= school.id
        #         org_name=item["org_id"]
        #         organization = await self.organization_dao.get_organization_by_name_and_school_id(
        #             org_name, school.id)
        #         if organization:
        #             org_id = str(organization.id)
        #             item["org_id"] = org_id
        #         # item["teacher_employer"] = 7225316120776019968
        #     else:
        #         raise SchoolNotFoundError()
        #     # item["org_id"] = "7228553981755265024"
        #     teacher_model = TeachersSaveImportCreatTestModel(**item)
        #     logger.info(type(item))
        #     try:
        #         teacher_id = await self.teacher_rule.add_teachers_import_save_test(teacher_model)
        #         teacher_id_list.append(teacher_id)
        #     except Exception as ex:
        #         return ex
        return teacher_id_list

    async def teachers_export(self, task: Task):
        bucket = "teachers_export"
        export_params: CurrentTeacherQuery = (
            task.payload if task.payload is CurrentTeacherQuery() else CurrentTeacherQuery()
        )
        page_request = PageRequest(page=1, per_page=10)
        random_file_name = f"teacher_export_{shortuuid.uuid()}.xlsx"
        temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)
        temp_file_path = os.path.join(temp_file_path, random_file_name)
        while True:
            paging = await self.teachers_info_dao.query_current_teacher_with_page(
                export_params, page_request
            )
            paging_result = PaginatedResponse.from_paging(
                paging, CurrentTeacherQueryRe, {"hash_password": "password"}
            )
            logger.info(paging_result.items)
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", paging_result.items)
            excel_writer.set_data(temp_file_path)
            excel_writer.execute()
            if len(paging.items) < page_request.per_page:
                break
            page_request.page += 1
        file_storage = await storage_manager.put_file_to_object(
            bucket, f"{random_file_name}.xlsx", temp_file_path
        )
        file_storage_resp = await storage_manager.add_file(
            self.file_storage_dao, file_storage
        )
        task_result = TaskResult()
        task_result.task_id = task.task_id
        task_result.result_file = file_storage_resp.file_name
        task_result.result_bucket = file_storage_resp.bucket_name
        task_result.result_file_id = file_storage_resp.file_id
        task_result.last_updated = datetime.now()
        task_result.state = TaskState.succeeded
        task_result.result_extra = {"file_size": file_storage.file_size}
        await self.task_dao.add_task_result(task_result)
        return task_result
