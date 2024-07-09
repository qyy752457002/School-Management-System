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
from views.models.teachers import TeachersCreatModel, TeacherInfoSaveModel, TeacherCreateResultModel, \
    TeacherFileStorageModel, CurrentTeacherQuery, CurrentTeacherQueryRe, \
    NewTeacherApprovalCreate
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from views.models.teacher_transaction import TeacherAddModel, TeacherAddReModel
# from rules.teachers_info_rule import TeachersInfoRule
from views.models.teachers import TeacherApprovalQuery, TeacherApprovalQueryRe, TeacherChangeLogQueryModel, \
    CurrentTeacherInfoSaveModel, TeacherRe, TeacherAdd

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter, ExcelReader
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.logging import logger
from daos.teacher_entry_dao import TeacherEntryApprovalDao
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from daos.teacher_key_info_approval_dao import TeacherKeyInfoApprovalDao
from daos.teacher_change_dao import TeacherChangeLogDAO
from rules.teacher_change_rule import TeacherChangeRule
from daos.teacher_approval_log_dao import TeacherApprovalLogDao

from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO
from views.common.common_view import compare_modify_fields
from models.teachers_info import TeacherInfo
from mini_framework.utils.snowflake import SnowflakeIdGenerator

import os


@dataclass_inject
class TeachersRule(object):
    teachers_dao: TeachersDao
    teachers_info_dao: TeachersInfoDao
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    # teachers_info_rule: TeachersInfoRule
    teacher_entry_approval_dao: TeacherEntryApprovalDao
    teacher_work_flow_rule: TeacherWorkFlowRule
    teacher_key_info_approval_dao: TeacherKeyInfoApprovalDao
    teacher_change_log: TeacherChangeLogDAO
    teacher_change_detail: TeacherChangeRule
    teacher_approval_log: TeacherApprovalLogDao
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO

    async def get_teachers_by_id(self, teachers_id):
        teachers_id = int(teachers_id)
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

    async def add_teachers(self, teachers: TeachersCreatModel, user_id):
        teacher_id_number = teachers.teacher_id_number
        teacher_id_type = teachers.teacher_id_type
        teacher_name = teachers.teacher_name
        teacher_gender = teachers.teacher_gender
        length = await self.teachers_dao.get_teachers_info_by_prams(teacher_id_number, teacher_id_type,
                                                                    teacher_name, teacher_gender)
        if length > 0:
            raise TeacherExistsError()
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[])
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()
        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        teachers_work = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        params = {"process_code": "t_entry", "applicant_name": user_id}
        await self.teacher_work_flow_rule.delete_teacher_save_work_flow_instance(
            teachers_work.teacher_id)
        work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teachers_work, params)
        # update_params = {"teacher_sub_status": "submitted"}
        # await self.teacher_work_flow_rule.update_work_flow_by_param(work_flow_instance["process_instance_id"],
        #                                                             update_params)
        teacher_entry_log = OperationRecord(
            action_target_id=int(teachers_work.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.NEW_ENTRY.value,
            change_detail="入职登记",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=int(work_flow_instance["process_instance_id"]))
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        teachers_info = TeacherInfoSaveModel(teacher_id=teachers_work.teacher_id)
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=["teacher_base_id"])
        teachers_inf_db.teacher_base_id = SnowflakeIdGenerator(1, 1).generate_id()
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, CurrentTeacherInfoSaveModel, exclude=[""])
        teacher_base_id = teachers_info.teacher_base_id
        return teachers_work, teacher_base_id

    async def query_teacher_operation_record_with_page(self, query_model: TeacherChangeLogQueryModel,
                                                       page_request: PageRequest):
        """
        查询教师操作记录
        """
        paging = await self.operation_record_dao.query_teacher_operation_record_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, OperationRecord)
        return paging_result

    async def add_transfer_teachers(self, teachers: TeacherAdd):
        """
        系统外调入系统内时使用
        """
        teachers.teacher_main_status = "employed"
        teachers.teacher_sub_status = "submitted"
        teachers_db = view_model_to_orm_model(teachers, Teacher, exclude=[""])
        teachers_db.teacher_id = SnowflakeIdGenerator(1, 1).generate_id()
        if teachers_db.teacher_id_type == 'resident_id_card':
            idstatus = check_id_number(teachers_db.teacher_id_number)
            if not idstatus:
                raise IdCardError()

        teachers_db = await self.teachers_dao.add_teachers(teachers_db)
        # 获取老师信息
        teachers = orm_model_to_view_model(teachers_db, TeacherRe, exclude=[""])
        return teachers

    async def update_teachers(self, teachers, user_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        old_teachers = orm_model_to_view_model(exists_teachers, TeachersModel, exclude=["hash_password"])
        teachers_main_status = exists_teachers.teacher_main_status
        if teachers_main_status == "employed":
            # teacher_info_db= await self.teachers_info_dao.get_teachers_info_by_teacher_id(teachers.teacher_id)
            # teacher_info = orm_model_to_view_model(teacher_info_db, CurrentTeacherInfoSaveModel, exclude=[""])
            # model_list=[teachers,teacher_info]

            # teacher_entry_approval_db = await self.teachers_info_dao.get_teacher_approval(teachers.teacher_id)
            # teacher_entry_approval = orm_model_to_view_model(teacher_entry_approval_db, NewTeacherApprovalCreate,
            #                                                  exclude=[""])
            res = compare_modify_fields(teachers, old_teachers)
            params = {"process_code": "t_keyinfo", "teacher_id": teachers.teacher_id, "applicant_name": user_id}
            work_flow_instance = await self.teacher_work_flow_rule.add_teacher_work_flow(teachers, params)
            update_params = {"teacher_main_status": "employed", "teacher_sub_status": "active"}
            await self.teacher_work_flow_rule.update_work_flow_by_param(work_flow_instance["process_instance_id"],
                                                                        update_params)
            await self.teacher_progressing(teachers.teacher_id)
            teacher_change_log = OperationRecord(
                action_target_id=int(teachers.teacher_id),
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.MODIFY.value,
                ip="127.0.0.1",
                change_data=str(res),
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.KEY_INFO_CHANGE.value,
                change_detail="详情",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=int(work_flow_instance["process_instance_id"]))
            await self.operation_record_rule.add_operation_record(teacher_change_log)

        elif teachers_main_status == "unemployed":
            need_update_list = []
            for key, value in teachers.dict().items():
                if value:
                    need_update_list.append(key)
            teachers = await self.teachers_dao.update_teachers(teachers, *need_update_list)
        return str(teachers.teacher_id)

    async def delete_teachers(self, teachers_id, user_id):
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        teachers_db = await self.teachers_dao.delete_teachers(exists_teachers)
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=[""])
        teacher_entry_log = OperationRecord(
            action_target_id=int(teachers.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.DELETE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.NEW_ENTRY.value,
            change_detail="删除",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=0)
        await self.operation_record_rule.add_operation_record(teacher_entry_log)
        return teachers

    async def get_all_teachers(self):
        teachers_db = await self.teachers_dao.get_all_teachers()
        teachers = orm_model_to_view_model(teachers_db, TeachersModel, exclude=["hash_password"])
        return teachers

    async def get_teachers_count(self):
        teachers_count = await self.teachers_dao.get_teachers_count()
        return teachers_count

    # async def submitting(self, teachers_id):
    #     teachers = await self.teacher_entry_approval_dao.get_teacher_entry_by_teacher_id(teachers_id)
    #     if not teachers:
    #         raise TeacherNotFoundError()
    #     teachers.approval_status = "submitting"
    #     return await self.teacher_entry_approval_dao.update_teachers(teachers, "approval_status")
    #

    async def entry_approved(self, teachers_id, process_instance_id, user_id, reason):
        await self.teacher_progressing(teachers_id)
        user_id = user_id
        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            teachers_db = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teachers_db.teacher_main_status = "employed"
            teachers_db.teacher_sub_status = "active"
            teachers_db.is_approval = False
            params = {"teacher_main_status": "employed", "teacher_sub_status": "active"}
            await self.teacher_work_flow_rule.update_work_flow_by_param(process_instance_id, params)
            await self.teachers_dao.update_teachers(teachers_db, "teacher_main_status", "teacher_sub_status",
                                                    "is_approval")
            return "该老师入职审批已通过"

    async def entry_rejected(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            teacher = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teacher.teacher_sub_status = "unsubmitted"
            teacher.teacher_main_status = "unemployed"
            teacher.is_approval = False
            await self.teachers_dao.update_teachers(teacher, "teacher_main_status ", "teacher_sub_status",
                                                    "is_approval")
            return "该老师入职审批已拒绝"

    async def entry_revoked(self, teachers_id, process_instance_id, user_id):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke"}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "revoked":
            teacher = await self.teachers_dao.get_teachers_by_id(teachers_id)
            teacher.teacher_sub_status = "unsubmitted"
            teacher.is_approval = False
            await self.teachers_dao.update_teachers(teacher, "teacher_sub_status", "is_approval")
            return "该老师入职审批已撤回"

    # 关键信息审批相关
    async def teacher_info_change_approved(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id

        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            result = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result, TeachersModel)
            need_update_list = []
            for key, value in teacher.dict().items():
                if value:
                    need_update_list.append(key)
            await self.teachers_dao.update_teachers(teacher, *need_update_list)
            await self.teacher_pending(teachers_id)
            await self.teacher_active(teachers_id)
            return "该老师关键信息变更审批已通过"

    async def teacher_info_change_rejected(self, teachers_id, process_instance_id, user_id, reason):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            await self.teacher_active(teachers_id)
            await self.teacher_pending(teachers_id)
            return "该老师关键信息变更审批已拒绝"

    async def teacher_info_change_revoked(self, teachers_id, process_instance_id, user_id):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke"}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "revoked":
            await self.teacher_active(teachers_id)
            await self.teacher_pending(teachers_id)
            return "该老师关键信息变更审批已撤回"

    # 导入导出相关

    async def import_teachers(self, task: Task):
        try:
            if not isinstance(task.payload, TeacherFileStorageModel):
                raise ValueError("参数错误")
            source_file = task.payload
            local_file_path = "/tmp/" + source_file.file_name.replace("/", "-")
            storage_manager.download_file(
                source_file.bucket_name, source_file.file_name, local_file_path
            )
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
                user_id = "asdfasdf"
                try:
                    await self.add_teachers(teacher_model, user_id)

                except Exception as ex:
                    result.failed_msg = str(ex)
                    logger.info(f"Failed to add teacher at index {idx}: {ex}")
                    print(ex, '表内数据异常')
                    raise ex
                results.append(result)

            # local_results_path = f"/tmp/c.xlsx"
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
            # task_result.result_extra = {"file_size": file_storage.file_size}
            #
            # await self.task_dao.add_task_result(task_result)
            # return task_result
        except Exception as e:
            print(e, '异常')
            raise e

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

    async def query_teacher_approval_with_page(self, type, query_model: TeacherApprovalQuery,
                                               page_request: PageRequest, user_id):
        if type == "launch":
            params = {"applicant_name": user_id, "process_code": "t_entry", "teacher_sub_status": "submitted"}
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        elif type == "approval":
            params = {"applicant_name": user_id, "process_code": "t_entry", "teacher_sub_status": "submitted"}
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        return paging

    async def query_teacher_info_change_approval(self, type, query_model: TeacherApprovalQuery,
                                                 page_request: PageRequest, user_id):
        if type == "launch":
            params = {"applicant_name": user_id, "process_code": "t_keyinfo", "teacher_main_status": "employed"}
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        elif type == "approval":
            params = {"applicant_name": user_id, "process_code": "t_keyinfo", "teacher_main_status": "employed"}
            paging = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request, query_model,
                                                                                          TeacherApprovalQueryRe,
                                                                                          params)
        return paging

    async def get_teacher_approval_by_teacher_id(self, teacher_id):
        teacher_approval_db = await self.teachers_info_dao.get_teacher_approval(teacher_id)
        teacher_approval = orm_model_to_view_model(teacher_approval_db, NewTeacherApprovalCreate)
        return teacher_approval

    async def teacher_progressing(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if not teachers.is_approval:
            teachers.is_approval = True
        else:
            return
        return await self.teachers_dao.update_teachers(teachers, "is_approval")

    async def teacher_submitted(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        teachers.teacher_sub_status = "submitted"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")

    async def teacher_pending(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.is_approval:
            teachers.is_approval = False
        else:
            return
        return await self.teachers_dao.update_teachers(teachers, "is_approval")

    async def teacher_active(self, teachers_id):
        teachers = await self.teachers_dao.get_teachers_by_id(teachers_id)
        if not teachers:
            raise TeacherNotFoundError()
        if teachers.teacher_sub_status != "active":
            teachers.teacher_sub_status = "active"
        return await self.teachers_dao.update_teachers(teachers, "teacher_sub_status")
