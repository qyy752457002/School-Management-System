from datetime import datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, ApprovalStatusError, TeacherStatusError
from daos.enum_value_dao import EnumValueDAO
from daos.operation_record_dao import OperationRecordDAO
from daos.school_dao import SchoolDAO
from daos.teacher_borrow_dao import TeacherBorrowDAO
from daos.teachers_dao import TeachersDao
from models.teacher_borrow import TeacherBorrow, BorrowType
from rules.enum_value_rule import EnumValueRule
from rules.operation_record import OperationRecordRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.teachers_rule import TeachersRule
from rules.transfer_details_rule import TransferDetailsRule
from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from views.models.teacher_transaction import TeacherTransactionQuery, TeacherTransactionQueryRe, TeacherBorrowModel, \
    TeacherBorrowReModel, TeacherBorrowGetModel, TeacherBorrowQueryModel, TeacherBorrowQueryReModel
from views.models.teacher_transaction import WorkflowQueryModel
from views.models.teachers import TeacherRe, TeacherAdd


@dataclass_inject
class TeacherBorrowRule(object):
    teacher_borrow_dao: TeacherBorrowDAO
    teachers_dao: TeachersDao
    teacher_work_flow_rule: TeacherWorkFlowRule
    enum_value_dao: EnumValueDAO
    enum_value_rule: EnumValueRule
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO
    teachers_rule: TeachersRule
    school_dao: SchoolDAO

    async def get_teacher_borrow_by_teacher_borrow_id(self, teacher_borrow_id):
        teacher_borrow_db = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow_db:
            raise TeacherNotFoundError()
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        return teacher_borrow

    async def add_teacher_borrow_in_inner(self, teacher_borrow: TeacherBorrowModel, user_id):
        """
        借入
        """
        try:
            exists_teachers = await self.teachers_dao.get_teachers_by_id(teacher_borrow.teacher_id)
            if not exists_teachers:
                raise TeacherNotFoundError()
            is_approval = exists_teachers.is_approval
            if is_approval:
                raise ApprovalStatusError()
            if exists_teachers.teacher_sub_status != "active":
                raise TeacherStatusError()
            teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow, exclude=["teacher_borrow_id"])
            teacher_borrow_db.teacher_borrow_id = SnowflakeIdGenerator(1, 1).generate_id()
            teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
            teacher_borrow_work = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
            transfer_details_rule = get_injector(TransferDetailsRule)
            transfer_and_borrow_extra_model = await transfer_details_rule.get_transfer_and_borrow_extra(
                original_district_area_id=teacher_borrow_work.original_district_area_id,
                current_district_area_id=teacher_borrow_work.current_district_area_id,
                original_unit_id=teacher_borrow_work.original_unit_id,
                current_unit_id=teacher_borrow_work.current_unit_id)
            original_unit_name = transfer_and_borrow_extra_model.original_unit_name
            current_unit_name = transfer_and_borrow_extra_model.current_unit_name
            teachers = orm_model_to_view_model(exists_teachers, TeacherRe)
            model_list = [teacher_borrow_work, teachers, transfer_and_borrow_extra_model]
            params = {"process_code": "t_borrow_in_inner", "applicant_name": user_id}
            work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
            teacher_borrow_log = OperationRecord(
                action_target_id=teacher_borrow_work.teacher_id,
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.BORROW.value,
                change_detail=f"从{original_unit_name}借入到{current_unit_name}",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=work_flow_instance["process_instance_id"])
            await self.operation_record_rule.add_operation_record(teacher_borrow_log)
            await self.teachers_rule.teacher_progressing(teacher_borrow_work.teacher_id)
            return True
        except Exception as e:
            return str(e)

    async def add_teacher_borrow_in_outer(self, add_teacher: TeacherAdd, teacher_borrow: TeacherBorrowModel,
                                          user_id):

        teachers = await self.teachers_rule.add_transfer_teachers(add_teacher)
        teachers.teacher_id = int(teachers.teacher_id)
        teachers.teacher_employer = int(teachers.teacher_employer)
        teacher_borrow.teacher_id = teachers.teacher_id
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow, exclude=["teacher_borrow_id"])
        teacher_borrow_db.teacher_borrow_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
        teacher_borrow_work = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        transfer_details_rule = get_injector(TransferDetailsRule)
        transfer_and_borrow_extra_model = await transfer_details_rule.get_transfer_and_borrow_extra(
            original_district_area_id=teacher_borrow_work.original_district_area_id,
            current_district_area_id=teacher_borrow_work.current_district_area_id,
            current_unit_id=teacher_borrow.current_unit_id)
        original_unit_name = teacher_borrow_work.original_unit_name
        current_unit_name = transfer_and_borrow_extra_model.current_unit_name
        params = {"process_code": "t_borrow_in_outer", "applicant_name": user_id}
        model_list = [teacher_borrow_work, teachers, transfer_and_borrow_extra_model]
        work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
        teacher_transfer_log = OperationRecord(
            action_target_id=teacher_borrow_work.teacher_id,
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.BORROW.value,
            change_detail=f"从{original_unit_name}借入到{current_unit_name}",
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=work_flow_instance["process_instance_id"])
        await self.operation_record_rule.add_operation_record(teacher_transfer_log)
        await self.teachers_rule.teacher_progressing(teacher_borrow.teacher_id)
        return True

    async def add_teacher_borrow_out(self, teacher_borrow: TeacherBorrowModel, user_id):
        """
        借出
        """
        try:
            teachers_db = await self.teachers_dao.get_teachers_by_id(teacher_borrow.teacher_id)
            teachers = orm_model_to_view_model(teachers_db, TeacherRe)
            if teachers.teacher_sub_status != "active":
                raise TeacherStatusError()
            original_unit_id = teachers.teacher_employer
            school = await self.school_dao.get_school_by_id(original_unit_id)
            teacher_borrow.original_unit_name = school.school_name
            teacher_borrow.original_district_area_id = int(school.borough)
            teacher_borrow.borrow_type = BorrowType.OUT.value
            teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow, exclude=["teacher_borrow_id"])
            teacher_borrow_db.teacher_borrow_id = SnowflakeIdGenerator(1, 1).generate_id()
            teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
            teacher_borrow_work = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel,
                                                          exclude=["original_unit_name",
                                                                   "current_unit_name"])
            transfer_details_rule = get_injector(TransferDetailsRule)
            transfer_and_borrow_extra_model = await transfer_details_rule.get_transfer_and_borrow_extra(
                original_district_area_id=teacher_borrow_work.original_district_area_id,
                current_district_area_id=teacher_borrow_work.current_district_area_id,
                original_unit_id=original_unit_id)
            transfer_and_borrow_extra_model.current_unit_name = teacher_borrow.current_unit_name
            current_unit_name = transfer_and_borrow_extra_model.current_unit_name
            params = {"process_code": "t_borrow_out", "applicant_name": user_id}

            model_list = [teacher_borrow_work, transfer_and_borrow_extra_model, teachers]
            work_flow_instance = await self.teacher_work_flow_rule.add_work_flow_by_multi_model(model_list, params)
            # update_params = {"teacher_sub_status": "active", "teacher_main_status": "employed"}
            # await self.teacher_work_flow_rule.update_work_flow_by_param(work_flow_instance["process_instance_id"],
            #                                                             update_params)
            teacher_transfer_log = OperationRecord(
                action_target_id=teacher_borrow_work.teacher_id,
                target=OperationTarget.TEACHER.value,
                action_type=OperationType.CREATE.value,
                ip="127.0.0.1",
                change_data="",
                operation_time=datetime.now(),
                doc_upload="",
                change_module=ChangeModule.BORROW.value,
                change_detail=f"从{school.school_name}借出到{current_unit_name}",
                status="/",
                operator_id=1,
                operator_name=user_id,
                process_instance_id=work_flow_instance["process_instance_id"])
            await self.operation_record_rule.add_operation_record(teacher_transfer_log)
            await self.teachers_rule.teacher_progressing(teacher_borrow.teacher_id)
            return True
        except Exception as e:
            return str(e)

    async def delete_teacher_borrow(self, teacher_borrow_id):
        exists_teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not exists_teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow_db = await self.teacher_borrow_dao.delete_teacher_borrow(exists_teacher_borrow)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel, exclude=[""])
        return teacher_borrow

    async def update_teacher_borrow(self, teacher_borrow: TeacherBorrowReModel):
        exists_teacher_borrow_info = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(
            teacher_borrow.teacher_borrow_id)
        if not exists_teacher_borrow_info:
            raise Exception(f"编号为{teacher_borrow.teacher_borrow_id}的teacher_borrow不存在")
        need_update_list = []
        for key, value in teacher_borrow.dict().items():
            if value:
                need_update_list.append(key)
        teacher_borrow = await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, *need_update_list)
        return teacher_borrow

    async def get_all_teacher_borrow(self, teacher_id):
        """
        详情页查询单个老师所有借动信息
        """
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        query_model = WorkflowQueryModel(teacher_id=teacher_id, process_code="borrow")
        teacher_borrow = await self.teacher_work_flow_rule.get_work_flow_instance_by_query_model(query_model,
                                                                                                 TeacherBorrowGetModel)
        return teacher_borrow

    async def query_teacher_borrow(self, teacher_borrow: TeacherTransactionQuery):
        """
        查询老师是否在系统内
        """
        teacher_borrow_db = await self.teachers_dao.query_teacher_transfer(teacher_borrow)
        teacher_borrow_inner = True  # 系统内互转
        if teacher_borrow_db:
            teacher_borrow_db = orm_model_to_view_model(teacher_borrow_db, TeacherTransactionQueryRe)
            return teacher_borrow_db, teacher_borrow_inner
        else:
            teacher_borrow_inner = False
            return teacher_borrow_db, teacher_borrow_inner

    async def query_teacher_borrow_with_page(self, query_model: TeacherBorrowQueryModel, page_request: PageRequest,
                                             user_id):
        # 借入借出都要查询
        params = {"applicant_name": user_id, "process_code": "t_borrow"}

        result = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                      query_model,
                                                                                      TeacherBorrowQueryReModel,
                                                                                      params)
        return result

    # 借动管理分页查询相关
    async def query_borrow_out_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                         page_request: PageRequest, extend_param):
        params = {}  # 这个是条件参数
        if type == "launch":
            params = {"process_code": "t_borrow_out", }
            params.update(extend_param)
        elif type == "approval":
            params = {"process_code": "t_borrow_out", }
            params.update(extend_param)
        result = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                      query_model,
                                                                                      TeacherBorrowQueryReModel,
                                                                                      params)
        return result

    async def query_borrow_in_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                        page_request: PageRequest, extend_param):
        params = {}  # 这个是条件参数
        if type == "launch":
            params = {"process_code": "t_borrow_in", }
            params.update(extend_param)
        elif type == "approval":
            params = {"process_code": "t_borrow_in", }
            params.update(extend_param)
        result = await self.teacher_work_flow_rule.query_work_flow_instance_with_page(page_request,
                                                                                      query_model,
                                                                                      TeacherBorrowQueryReModel,
                                                                                      params)
        return result

    # 借动管理审批相关
    # async def submitting(self, teacher_borrow_id):
    #     teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
    #     if not teacher_borrow:
    #         raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
    #     teacher_borrow.approval_status = "submitting"
    #     return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")
    #
    # async def submitted(self, teacher_borrow_id):
    #     teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
    #     if not teacher_borrow:
    #         raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
    #     teacher_borrow.approval_status = "submitted"
    #     return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_approved(self, teacher_id, process_instance_id, user_id, reason):
        user_id = user_id
        parameters = {"user_id": user_id, "action": "approved", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id, parameters)
        if node_instance == "approved":
            result = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            process_code = result.get("process_code")
            teachers_db = await self.teachers_dao.get_teachers_by_id(teacher_id)
            if process_code == "t_borrow_out":
                """需要删除本校老师"""
                # 原本学校需要做的事情
                # 更新状态
                teachers_db.teacher_sub_status = "borrow_out"
                await self.teachers_dao.update_teachers(teachers_db, "teacher_sub_status")
                await self.teachers_rule.teacher_pending(int(teacher_id))
            elif process_code == "t_borrow_in_inner":
                """需要先修改本校老师状态，包括is_deleted和teacher_sub_status，然后再添加新的老师，以及增加老师的调入记录"""

                update_params = {"teacher_sub_status": "borrow_in"}
                await self.teacher_work_flow_rule.update_work_flow_by_param(process_instance_id, update_params)
                teachers_db.teacher_sub_status = "borrow_in"
                await self.teachers_dao.update_teachers(teachers_db, "teacher_sub_status")
                await self.teachers_rule.teacher_pending(int(teacher_id))
            elif process_code == "t_borrow_in_outer":
                """增加老师再添加新老师"""
                update_params = {"teacher_sub_status": "borrow_in"}
                await self.teacher_work_flow_rule.update_work_flow_by_param(process_instance_id, update_params)
                result_after = await self.teacher_work_flow_rule.get_work_flow_instance_by_process_instance_id(
                    process_instance_id)
                teacher = await self.teacher_work_flow_rule.create_model_from_workflow(result_after, TeacherRe)
                need_update_list = []
                for key, value in teacher.dict().items():
                    if value:
                        need_update_list.append(key)
                await self.teachers_dao.update_teachers(teacher, *need_update_list)
                await self.teachers_rule.teacher_pending(int(teacher_id))
            return "该老师借动审批已通过"

    async def borrow_rejected(self, teacher_id, process_instance_id, user_id, reason):
        user_id = user_id
        await self.teachers_rule.teacher_progressing(teacher_id)
        parameters = {"user_id": user_id, "action": "rejected", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "rejected":
            await self.teachers_rule.teacher_active(teacher_id)
            await self.teachers_rule.teacher_pending(teacher_id)
            return "该老师借动审批已拒绝"

    async def borrow_revoked(self, teacher_id, process_instance_id, user_id, reason):

        await self.teachers_rule.teacher_progressing(teacher_id)
        user_id = user_id
        parameters = {"user_id": user_id, "action": "revoke", "description": reason}
        current_node = await self.teacher_work_flow_rule.get_teacher_work_flow_current_node(process_instance_id)
        node_instance_id = current_node.get("node_instance_id")
        node_instance = await self.teacher_work_flow_rule.process_transaction_work_flow(node_instance_id,
                                                                                        parameters)
        if node_instance == "revoked":
            await self.teachers_rule.teacher_active(teacher_id)
            await self.teachers_rule.teacher_pending(teacher_id)
            return "该老师借动审批已撤回"

    async def borrow_teacher_active(self, teacher_id, process_instance_id):
        teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not teacher:
            raise TeacherNotFoundError()
        if teacher.teacher_sub_status != "active":
            teacher.teacher_main_status = "employed"
            teacher.teacher_sub_status = "active"
        await self.teachers_dao.update_teachers(teacher, "teacher_sub_status", "teacher_main_status")
        update_params = {"teacher_sub_status": "active", "teacher_main_status": "employed"}
        await self.teacher_work_flow_rule.update_work_flow_by_param(process_instance_id, update_params)
        return "该老师已恢复在职"
