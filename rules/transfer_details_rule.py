from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.transfer_details_dao import TransferDetailsDAO
from daos.teachers_dao import TeachersDao
from models.transfer_details import TransferDetails
from views.models.teacher_transaction import TransferDetailsModel, TransferDetailsUpdateModel
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQuery, TeacherTransactionQueryRe, TransferDetailsCreateReModel, \
    TransferDetailsReModel, TransferDetailsGetModel
from business_exceptions.teacher import TeacherNotFoundError


@dataclass_inject
class TransferDetailsRule(object):
    transfer_details_dao: TransferDetailsDAO
    teachers_dao: TeachersDao

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        transfer_details_db = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel)
        return transfer_details

    async def add_transfer_in_details(self, transfer_details: TransferDetailsModel):
        """
        调入
        """
        # todo 需要增加获取调入流程实例id
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
        return transfer_details

    async def add_transfer_out_details(self, transfer_details: TransferDetailsModel):
        """
        调出
        """
        # todo 需要增加获取调出流程实例id
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsReModel)
        return transfer_details

    async def delete_transfer_details(self, transfer_details_id):
        exists_transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not exists_transfer_details:
            raise Exception(f"编号为的{transfer_details_id}transfer_details不存在")
        transfer_details_db = await self.transfer_details_dao.delete_transfer_details(exists_transfer_details)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel, exclude=[""])
        return transfer_details

    async def update_transfer_details(self, transfer_details: TransferDetailsUpdateModel):
        exists_transfer_details_info = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details.transfer_details_id)
        if not exists_transfer_details_info:
            raise Exception(f"编号为{transfer_details.transfer_details_id}的transfer_details不存在")
        need_update_list = []
        for key, value in transfer_details.dict().items():
            if value:
                need_update_list.append(key)
        transfer_details = await self.transfer_details_dao.update_transfer_details(transfer_details, *need_update_list)
        return transfer_details

    async def get_all_transfer_details(self, teacher_id):
        """
        详情页查询单个老师所有调动信息
        """
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        transfer_details_db = await self.transfer_details_dao.get_all_transfer_details(teacher_id)
        transfer_details = []
        for item in transfer_details_db:
            transfer_details.append(orm_model_to_view_model(item, TransferDetailsGetModel))
        return transfer_details

    async def query_teacher(self, teacher_transaction: TeacherTransactionQuery):
        teacher_transaction_db = await self.transfer_details_dao.query_teacher(teacher_transaction)
        teacher_transaction = []
        for item in teacher_transaction_db.items:
            teacher_transaction.append(orm_model_to_view_model(item, TeacherTransactionQueryRe))
        return teacher_transaction

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        """
        查询老师是否在系统内
        """
        teacher_transaction_db = await self.transfer_details_dao.query_teacher_transfer(teacher_transaction)
        transfer_inner = True  # 系统内互转
        if teacher_transaction_db:
            teacher_transaction_db = orm_model_to_view_model(teacher_transaction_db, TeacherTransactionQueryRe)
            return teacher_transaction_db, transfer_inner
        else:
            transfer_inner = False
            return teacher_transaction_db, transfer_inner

    async def submitting(self, transfer_details_id):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        transfer_details.approval_status = "submitting"
        return await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")

    async def submitted(self, transfer_details_id):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        transfer_details.approval_status = "submitted"
        return await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")

    async def approved(self, transfer_details_id):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        transfer_details.approval_status = "approved"
        return await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")

    async def rejected(self, transfer_details_id):
        transfer_details = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        if not transfer_details:
            raise Exception(f"编号为{transfer_details_id}的transfer_details不存在")
        transfer_details.approval_status = "rejected"
        return await self.transfer_details_dao.update_transfer_details(transfer_details, "approval_status")
