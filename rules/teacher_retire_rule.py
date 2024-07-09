from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from views.models.teachers import TeacherInfo as TeachersInfoModel
from views.models.teachers import NewTeacher, NewTeacherRe, TeacherInfoSaveModel, TeacherInfoSubmit, \
    CurrentTeacherQuery, CurrentTeacherQueryRe, CurrentTeacherInfoSaveModel, NewTeacherInfoSaveModel, \
    TeacherInfoCreateModel, NewTeacherApprovalCreate
from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError, TeacherInfoExitError, QueryError
from daos.teachers_dao import TeachersDao
from rules.organization_memebers_rule import OrganizationMembersRule
from daos.teacher_key_info_approval_dao import TeacherKeyInfoApprovalDao
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from datetime import datetime
from views.models.operation_record import OperationRecord, OperationTarget, ChangeModule, OperationType
from rules.operation_record import OperationRecordRule
from daos.operation_record_dao import OperationRecordDAO
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from daos.teacher_retire_dao import TeachersRetireDao
from views.models.teacher_transaction import TeacherRetireQueryRe, TeacherRetireQuery, TeacherRetireCreateModel, \
    TeacherRetireUpdateModel
from models.teacher_retire import TeacherRetire
from business_exceptions.teacher_transction import TransactionError
from views.models.teachers import TeacherMainStatus


@dataclass_inject
class TeacherRetireRule(object):
    teachers_info_dao: TeachersInfoDao
    teachers_dao: TeachersDao
    organization_members_rule: OrganizationMembersRule
    teacher_work_flow_rule: TeacherWorkFlowRule
    teacher_key_info_approval_dao: TeacherKeyInfoApprovalDao
    teacher_work_flow_rule: TeacherWorkFlowRule
    operation_record_rule: OperationRecordRule
    operation_record_dao: OperationRecordDAO
    teacher_retire_dao: TeachersRetireDao

    async def query_retire_teacher_with_page(self, query_model: TeacherRetireQuery, page_request: PageRequest):
        print(query_model)
        paging = await self.teacher_retire_dao.query_retire_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, TeacherRetireQueryRe)
        return paging_result

    async def add_teacher_retire(self, teacher_retire: TeacherRetireCreateModel, user_id):
        """
        添加教师异动
        """
        teacher_db = await self.teachers_dao.get_teachers_by_id(teacher_retire.teacher_id)
        teacher_main_status = teacher_db.teacher_main_status
        if not teacher_db:
            raise TeacherNotFoundError()
        if teacher_main_status != "employed":
            raise TransactionError()
        teacher_db.teacher_sub_status = teacher_retire.transaction_type
        teacher_db.teacher_main_status = TeacherMainStatus.RETIRED.value
        await self.teachers_dao.update_teachers(teacher_db, "teacher_sub_status", "teacher_main_status")

        teacher_transaction_db = view_model_to_orm_model(teacher_retire, TeacherRetire)
        teacher_transaction_db.teacher_retire_id = SnowflakeIdGenerator(1, 1).generate_id()
        teacher_transaction_db = await self.teacher_retire_dao.add_teacher_retire(teacher_transaction_db)
        teacher_transaction = orm_model_to_view_model(teacher_transaction_db, TeacherRetireUpdateModel)
        teacher_transaction_log = OperationRecord(
            action_target_id=int(teacher_transaction.teacher_id),
            target=OperationTarget.TEACHER.value,
            action_type=OperationType.CREATE.value,
            ip="127.0.0.1",
            change_data="",
            operation_time=datetime.now(),
            doc_upload="",
            change_module=ChangeModule.RETIREMENT.value,
            change_detail=f'{teacher_transaction.transaction_type}',
            status="/",
            operator_id=1,
            operator_name=user_id,
            process_instance_id=0)
        await self.operation_record_rule.add_operation_record(teacher_transaction_log)
        return teacher_transaction
