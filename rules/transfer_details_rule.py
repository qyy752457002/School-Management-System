from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.transfer_details_dao import TransferDetailsDAO
from models.transfer_details import TransferDetails
from views.models.teacher_extend import TransferDetailsModel, TransferDetailsUpdateModel


@dataclass_inject
class TransferDetailsRule(object):
    transfer_details_dao: TransferDetailsDAO

    async def get_transfer_details_by_transfer_details_id(self, transfer_details_id):
        transfer_details_db = await self.transfer_details_dao.get_transfer_details_by_transfer_details_id(
            transfer_details_id)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel)
        return transfer_details

    async def add_transfer_details(self, transfer_details: TransferDetailsModel):
        transfer_details_db = view_model_to_orm_model(transfer_details, TransferDetails)
        transfer_details_db = await self.transfer_details_dao.add_transfer_details(transfer_details_db)
        transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel)
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
        transfer_details_db = await self.transfer_details_dao.get_all_transfer_details(teacher_id)
        #          transfer_details = orm_model_to_view_model(transfer_details_db, TransferDetailsModel, exclude=[""])
        transfer_details = []
        for item in transfer_details_db:
            transfer_details.append(orm_model_to_view_model(item, TransferDetailsModel))
        return transfer_details_db
