from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_dao import TeachersDao
from daos.teacher_borrow_dao import TeacherBorrowDAO
from models.teacher_borrow import TeacherBorrow
from mini_framework.design_patterns.depend_inject import get_injector
from rules.transfer_details_rule import TransferDetailsRule

from business_exceptions.teacher import TeacherNotFoundError, ApprovalStatusError
from views.models.teacher_transaction import TeacherTransactionQuery, TeacherTransactionQueryRe, TeacherBorrowModel, \
    TeacherBorrowReModel, TeacherBorrowGetModel, TeacherBorrowQueryModel, TeacherBorrowQueryReModel

from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO

from views.models.teachers import TeachersCreatModel, TeacherRe
from datetime import datetime
from daos.school_dao import SchoolDAO

from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from daos.enum_value_dao import EnumValueDAO
from rules.enum_value_rule import EnumValueRule

from rules.teachers_rule import TeachersRule


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
        exists_teachers = await self.teachers_dao.get_teachers_by_id(teacher_borrow.teacher_id)
        if not exists_teachers:
            raise TeacherNotFoundError()
        is_approval = exists_teachers.is_approval
        if is_approval:
            raise ApprovalStatusError()
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow)
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
        return teacher_borrow

    async def add_teacher_borrow_in_outer(self, add_teacher: TeachersCreatModel, teacher_borrow: TeacherBorrowModel,
                                          user_id):
        pass


    async def add_teacher_borrow_out(self, teacher_borrow: TeacherBorrowModel):
        """
        借出
        """
        # todo 需要增加获取调出流程实例id
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow)
        teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        return teacher_borrow

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
        teacher_borrow_db = await self.teacher_borrow_dao.get_all_teacher_borrow(teacher_id)
        teacher_borrow = []
        for item in teacher_borrow_db:
            teacher_borrow.append(orm_model_to_view_model(item, TeacherBorrowGetModel))
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

    # 借动管理分页查询相关
    async def query_borrow_out_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                         page_request: PageRequest):
        if type == "launch":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_out_launch_with_page(query_model,
                                                                                                page_request)
        elif type == "approval":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_out_approval_with_page(query_model,
                                                                                                  page_request)
        paging_result = PaginatedResponse.from_paging(teacher_borrow_db, TeacherBorrowQueryReModel)
        return paging_result

    async def query_borrow_in_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                        page_request: PageRequest):
        if type == "launch":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_in_launch_with_page(query_model,
                                                                                               page_request)
        elif type == "approval":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_in_approval_with_page(query_model,
                                                                                                 page_request)
        paging_result = PaginatedResponse.from_paging(teacher_borrow_db, TeacherBorrowQueryReModel)
        return paging_result

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

    async def borrow_approved(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "approved"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_rejected(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "rejected"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_revoked(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "revoked"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")
