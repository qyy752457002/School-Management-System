from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query

from views.models.teacher_transaction import TransferDetailsModel, TransferDetailsUpdateModel
from rules.transfer_details_rule import TransferDetailsRule

from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQuery
from rules.teacher_transaction_rule import TeacherTransactionRule


class TransferDetailsView(BaseView):
    def __init__(self):
        super().__init__()

        self.transfer_details_rule = get_injector(TransferDetailsRule)

    async def get_transfer_details(self,
                                   transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                    description="transfer_detailsID", example=1234)
                                   ):
        res = await self.transfer_details_rule.get_transfer_details_by_transfer_details_id(transfer_details_id)
        return res

    async def post_transfer_in_details(self, transfer_details: TransferDetailsModel):
        res = await self.transfer_details_rule.add_transfer_in_details(transfer_details)
        return res

    async def post_transfer_out_details(self, transfer_details: TransferDetailsModel):
        res = await self.transfer_details_rule.add_transfer_out_details(transfer_details)
        return res

    async def delete_transfer_details(self,
                                      transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                       description="transfer_detailsID", example=1234)
                                      ):
        await self.transfer_details_rule.delete_transfer_details(transfer_details_id)

    async def put_transfer_details(self, transfer_details: TransferDetailsUpdateModel):
        res = await self.transfer_details_rule.update_transfer_details(transfer_details)
        return res

    async def get_transfer_details_all(self, teacher_id: int = Query(None, title="transfer_detailsID",
                                                                     description="transfer_detailsID", example=1234)):
        return await self.transfer_details_rule.get_all_transfer_details(teacher_id)

    async def query_teacher(self, teacher_transaction: TeacherTransactionQuery):

        res = await self.transfer_details_rule.query_teacher(teacher_transaction)
        return res


class TeacherTransactionView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_transaction_rule = get_injector(TeacherTransactionRule)

    async def get_teacher_transaction(self,
                                      teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                          description="teacher_transactionID",
                                                                          example=1234)
                                      ):
        res = await self.teacher_transaction_rule.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        return res

    async def post_teacher_transaction(self, teacher_transaction: TeacherTransactionModel):
        res = await self.teacher_transaction_rule.add_teacher_transaction(teacher_transaction)
        return res

    async def delete_teacher_transaction(self,
                                         teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                             description="teacher_transactionID",
                                                                             example=1234)
                                         ):
        await self.teacher_transaction_rule.delete_teacher_transaction(teacher_transaction_id)

    async def put_teacher_transaction(self, teacher_transaction: TeacherTransactionUpdateModel):
        res = await self.teacher_transaction_rule.update_teacher_transaction(teacher_transaction)
        return res

    async def get_teacher_transaction_all(self, teacher_id: int = Query(None, title="teacher_transactionID",
                                                                        description="teacher_transactionID",
                                                                        example=1234)):
        return await self.teacher_transaction_rule.get_all_teacher_transaction(teacher_id)


