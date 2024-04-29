from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.student_inner_transaction_rule import StudentInnerTransactionRule
from views.models.student_inner_transaction import StudentInnerTransaction, StudentInnerTransactionSearch
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


    async def post(self, student_inner_transaction: StudentInnerTransaction):
        # print(graduation_student)


        res =await self.student_inner_transaction_rule.add_student_inner_transaction(student_inner_transaction)

        return res

    # 分页查询
    async def page(self,
                   student_inner_transaction_search= Depends( StudentInnerTransactionSearch)   ,

                   page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = await self.student_inner_transaction_rule.query_student_inner_transaction_with_page(page_request, student_inner_transaction_search )
        return res
