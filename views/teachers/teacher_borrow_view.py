from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query, Depends

from views.models.teacher_borrow import TeacherBorrowModel, TeacherBorrowUpdateModel
from rules.teacher_borrow_rule import TeacherBorrowRule
from mini_framework.web.std_models.page import PageRequest


class TeacherBorrowView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_borrow_rule = get_injector(TeacherBorrowRule)
        self.teacher_rule = get_injector(TeachersRule)

    async def get_teacher_borrow(self,
                                 teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                description="teacher_borrowID", example=1234)
                                 ):
        """
        审批时仅查看调动信息，无日志信息
        """
        res = await self.teacher_borrow_rule.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        return res

    async def post_teacher_borrow_in(self, teacher_borrow: TeacherBorrowModel,
                                     add_teacher: Optional[TeacherAddModel] = None,
                                     teacher_borrow_inner: bool = Query(True, title="transfer_status",
                                                                        description="transfer_status",
                                                                        example=True)):
        """
        借入
        """
        if not teacher_borrow_inner:
            if add_teacher != None:
                await self.teacher_rule.add_teachers(add_teacher)
            else:
                raise Exception("请填写老师信息")
        res = await self.teacher_borrow_rule.add_transfer_in_details(teacher_borrow)
        return res

    async def post_teacher_borrow_out(self, teacher_borrow: TeacherBorrowModel):
        """
        借出
        """
        res = await self.teacher_borrow_rule.add_transfer_out_details(teacher_borrow)
        return res

    async def delete_teacher_borrow(self,
                                    teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                   description="teacher_borrowID", example=1234)
                                    ):
        await self.teacher_borrow_rule.delete_teacher_borrow(teacher_borrow_id)

    async def put_teacher_borrow(self, teacher_borrow: TeacherBorrowUpdateModel):
        res = await self.teacher_borrow_rule.update_teacher_borrow(teacher_borrow)
        return res

    async def get_teacher_borrow_all(self, teacher_id: int = Query(None, title="teacher_borrowID",
                                                                   description="teacher_borrowID", example=1234)):
        """
        获取单个老师所有借动信息,是教师详情页中的借动明细
        """
        return await self.teacher_borrow_rule.get_all_teacher_borrow(teacher_id)

    async def query_teacher_borrow(self, teacher_borrow: TeacherTransactionQuery):
        """
        查询老师是否在系统内
        """
        return await self.teacher_borrow_rule.query_teacher_transfer(teacher_borrow)

    # 借动管理查询
    async def page_borrow_out_launch(self, teacher_borrow=Depends(TeacherBorrowQueryModel), page_request=Depends(PageRequest)):
        """
       我发起的借出
        """
        type="launch"
        paging_result = await self.teacher_borrow_rule.query_borrow_out_with_page(type, teacher_borrow, page_request)
        return paging_result

    async def page_borrow_out_approval(self, teacher_borrow=Depends(TeacherBorrowQueryModel), page_request=Depends(PageRequest)):
        """
        我审批的借出
        """
        type="approval"
        paging_result = await self.teacher_borrow_rule.query_borrow_out_with_page(type, teacher_borrow, page_request)
        return paging_result

    async def page_borrow_in_launch(self, teacher_borrow=Depends(TeacherBorrowQueryModel), page_request=Depends(PageRequest)):
        """
        我发起的借入
        """
        type="launch"
        paging_result = await self.teacher_borrow_rule.query_borrow_in_with_page(type, teacher_borrow, page_request)
        return paging_result

    async def page_borrow_in_approval(self, teacher_borrow=Depends(TeacherBorrowQueryModel), page_request=Depends(PageRequest)):
        """
        我审批的借入
        """
        type="approval"
        paging_result = await self.teacher_borrow_rule.query_borrow_in_with_page(type, teacher_borrow, page_request)
        return paging_result

    # 审批相关
    # async def patch_borrow_submitting(self,
    #                                   teacher_borrow_id: int = Query(None, title="teacher_borrowID",
    #                                                                  description="teacher_borrowID", example=1234)):
    #     res = await self.teacher_borrow_rule.submitting(teacher_borrow_id)
    #     return res
    #
    # async def patch_borrow_submitted(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
    #                                                                       description="teacher_borrowID",
    #                                                                       example=1234)):
    #     res = await self.teacher_borrow_rule.submitted(teacher_borrow_id)
    #     return res

    async def patch_borrow_approved(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.approved(teacher_borrow_id)
        return res

    async def patch_borrow_rejected(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.rejected(teacher_borrow_id)
        return res

    async def patch_borrow_revoked(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.revoked(teacher_borrow_id)
        return res