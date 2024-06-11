from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query, Depends

from views.models.teacher_transaction import TransferDetailsModel, TransferDetailsUpdateModel
from rules.transfer_details_rule import TransferDetailsRule

from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQuery,TeacherTransferQueryModel, TeacherTransactionQueryModel
from views.models.teacher_transaction import TeacherAddModel
from rules.teacher_transaction_rule import TeacherTransactionRule
from rules.teachers_rule import TeachersRule
from mini_framework.web.std_models.page import PageRequest
from typing import Optional


class TransferDetailsView(BaseView):
    def __init__(self):
        super().__init__()
        self.transfer_details_rule = get_injector(TransferDetailsRule)
        self.teacher_rule = get_injector(TeachersRule)

    async def get_transfer_details(self,
                                   transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                    description="transfer_detailsID", example=1234)
                                   ):
        """
        审批时仅查看调动信息，无日志信息
        """
        res = await self.transfer_details_rule.get_transfer_details_by_transfer_details_id(transfer_details_id)
        return res

    async def post_transfer_in_details(self, transfer_details: TransferDetailsModel,
                                       add_teacher: Optional[TeacherAddModel] = None,
                                       transfer_inner: bool = Query(True, title="transfer_status",
                                                                    description="transfer_status",
                                                                    example=True),
                                       ):
        """
        调入
        """
        if not transfer_inner:  # 如果是系统外转系统内
            if add_teacher != None:
                await self.teacher_rule.add_teachers(add_teacher)
            else:
                raise Exception("请填写老师信息")
            if transfer_details.original_position == "":
                raise Exception("原岗位不能为空")
        res = await self.transfer_details_rule.add_transfer_in_details(transfer_details)
        return res

    async def post_transfer_out_details(self, transfer_details: TransferDetailsModel):
        """
        调出
        """
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

    async def get_transfer_details_all(self, teacher_id: int = Query(None, title="transfer_ID",
                                                                     description="transfer_ID", example=1234)):
        """
        查询单个老师所有调动信息,是教师详情页中的调动明细
        """
        return await self.transfer_details_rule.get_all_transfer_details(teacher_id)

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        """
        查询系统内有没有此人
        """
        res, transfer_inner = await self.transfer_details_rule.query_teacher_transfer(teacher_transaction)
        return res, transfer_inner

    #调动管理查询
    async def page_transfer_launch(self, transfer_details=Depends(TeacherTransferQueryModel),
                                   page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.transfer_details_rule.query_transfer_with_page(transfer_details, page_request)
        return paging_result


    #调动审批
    async def patch_transfer_submitting(self,
                                        transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                        description="transfer_detailsID", example=1234)):
        res = await self.transfer_details_rule.submitting(transfer_details_id)
        return res

    async def patch_transfer_submitted(self,
                                      transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                      description="transfer_detailsID", example=1234)):
        res = await self.transfer_details_rule.submitted(transfer_details_id)
        return res

    async def patch_transfer_approved(self,
                                     transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                     description="transfer_detailsID", example=1234)):
        res = await self.transfer_details_rule.approved(transfer_details_id)
        return res

    async def patch_transfer_rejected(self,
                                     transfer_details_id: int = Query(None, title="transfer_detailsID",
                                                                     description="transfer_detailsID", example=1234)):
        res = await self.transfer_details_rule.rejected(transfer_details_id)
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
        # 异动审批中查询单个教师单个异动信息
        res = await self.teacher_transaction_rule.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        return res

    async def post_teacher_transaction(self, teacher_transaction: TeacherTransactionModel):
        res = await self.teacher_transaction_rule.add_teacher_transaction(teacher_transaction)
        return res

    # async def put_teacher_transaction(self, teacher_transaction: TeacherTransactionUpdateModel):
    #     res = await self.teacher_transaction_rule.update_teacher_transaction(teacher_transaction)
    #     return res

    async def get_teacher_transaction_all(self, teacher_id: int = Query(None, title="teacher_transactionID",
                                                                        description="teacher_transactionID",
                                                                        example=1234)):
        """
        单个老师获取该老师的所有异动信息
        """
        return await self.teacher_transaction_rule.get_all_teacher_transaction(teacher_id)

    async def page_transaction_launch(self, teacher_transaction=Depends(TeacherTransactionQueryModel),
                                      page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.teacher_transaction_rule.query_transaction_with_page(teacher_transaction,
                                                                                        page_request)
        return paging_result

    # 异动审批
    async def patch_transaction_submitting(self,
                                           teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                               description="teacher_transactionID",
                                                                               example=1234)):
        res = await self.teacher_transaction_rule.submitting(teacher_transaction_id)
        return res

    async def patch_transaction_submitted(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                                    description="teacher_transactionID",
                                                                                    example=1234)):
        res = await self.teacher_transaction_rule.submitted(teacher_transaction_id)
        return res

    async def patch_transaction_approved(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                                   description="teacher_transactionID",
                                                                                   example=1234)):
        res = await self.teacher_transaction_rule.approved(teacher_transaction_id)
        return res

    async def patch_transaction_rejected(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
                                                                                   description="teacher_transactionID",
                                                                                   example=1234)):
        res = await self.teacher_transaction_rule.rejected(teacher_transaction_id)
        return res
