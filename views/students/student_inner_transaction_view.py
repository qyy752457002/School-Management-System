import traceback
from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.student_inner_transaction_rule import StudentInnerTransactionRule
from rules.student_transaction_flow import StudentTransactionFlowRule
from views.models.student_inner_transaction import StudentInnerTransaction, StudentInnerTransactionSearch, \
    StudentInnerTransactionRes, StudentInnerTransactionAudit
from views.models.student_transaction import StudentTransactionStatus, StudentTransactionFlow
from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo, StudentGraduation
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date
from views.models.students import GraduationStudents


class StudentInnerTransactionView(BaseView):
    def __init__(self):
        super().__init__()
        self.student_inner_transaction_rule = get_injector(StudentInnerTransactionRule)
        self.student_transaction_flow_rule = get_injector(StudentTransactionFlowRule)


    async def post(self, student_inner_transaction: StudentInnerTransaction):
        # print(graduation_student)
        try:


            res =await self.student_inner_transaction_rule.add_student_inner_transaction(student_inner_transaction)
        except Exception as e:
            print(e)
            traceback.print_exc()
            return e

        return res

    # 分页查询
    async def page(self,
                   student_inner_transaction_search= Depends( StudentInnerTransactionSearch)   ,

                   page_request=Depends(PageRequest)):
        print(page_request)
        items = []
        try:
            res = await self.student_inner_transaction_rule.query_student_inner_transaction_with_page(page_request, student_inner_transaction_search )


        except Exception as e:
            print(e)
            traceback.print_exc()
            return e


        return res

    # 异动 撤回
    async def patch_student_inner_transaction_cancel(self,
                                       transaction_id: int|str = Query(..., description="异动id", example='2')
                                       ):
        # todo 校验是否本人或者老师

        student_edu_info = StudentInnerTransactionRes(id=transaction_id,
                                              approval_status=StudentTransactionStatus.CANCEL.value, )
        res2 = await self.student_inner_transaction_rule.update_student_inner_transaction(student_edu_info)

        # 流乘记录 todo 工作流
        # student_trans_flow = StudentTransactionFlow(apply_id=transaction_id,
        #                                             status=StudentTransactionStatus.CANCEL.value,
        #                                             # stage=audit_info.transferin_audit_action.value,
        #                                             remark= '用户撤回')
        # res = await self.student_transaction_flow_rule.add_student_transaction_flow(student_trans_flow)

        # print(new_students_key_info)
        return res2
    # 在校生校内异动审核
    async def patch_student_inner_transaction_audit(self,
                                                    audit_info: StudentInnerTransactionAudit

                                                     ):
        # todo 校验是否本人或者老师

        student_inner_transaction_info = StudentInnerTransactionRes(id=audit_info.transaction_id,
                                                      approval_status=audit_info.transaction_audit_action.value, )
        res2 = await self.student_inner_transaction_rule.update_student_inner_transaction(student_inner_transaction_info)

        # 流乘记录 todo 接入 工作流 状态

        # print(new_students_key_info)
        return res2
