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

    async def get_teacher_borrow(self,
                                 teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                description="teacher_borrowID", example=1234)
                                 ):
        res = await self.teacher_borrow_rule.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        return res

    async def post_teacher_borrow(self, teacher_borrow: TeacherBorrowModel):
        res = await self.teacher_borrow_rule.add_teacher_borrow(teacher_borrow)
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
        获取单个老师所有借动信息
        """
        return await self.teacher_borrow_rule.get_all_teacher_borrow(teacher_id)

    async def page_borrow_launch(self, teacher_borrow=Depends(TeacherBorrowModel), page_request=Depends(PageRequest)):
        """
        分页查询借调信息
        """
        paging_result = await self.teacher_borrow_rule.query_borrow_with_page(teacher_borrow, page_request)
        return paging_result

    # 审批相关
    async def patch_borrow_submitting(self,
                                      teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                     description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.submitting(teacher_borrow_id)
        return res

    async def patch_borrow_submitted(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                          description="teacher_borrowID",
                                                                          example=1234)):
        res = await self.teacher_borrow_rule.submitted(teacher_borrow_id)
        return res

    async def patch_borrow_approved(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.approved(teacher_borrow_id)
        return res

    async def patch_borrow_rejected(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        res = await self.teacher_borrow_rule.rejected(teacher_borrow_id)
        return res
