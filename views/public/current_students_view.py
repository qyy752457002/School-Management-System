import copy
import json

from fastapi.params import Body
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.student import StudentExistsThisSchoolError
from models.student_transaction import AuditAction, TransactionDirection, AuditFlowStatus
from rules.classes_rule import ClassesRule
from rules.graduation_student_rule import GraduationStudentRule
from rules.student_transaction import StudentTransactionRule
from rules.student_transaction_flow import StudentTransactionFlowRule
from rules.students_key_info_change_rule import StudentsKeyInfoChangeRule
from views.models.student_transaction import StudentTransaction, StudentTransactionFlow, StudentTransactionStatus, \
    StudentEduInfo, StudentTransactionAudit, StudentEduInfoOut
from views.models.students import NewStudents, StudentsKeyinfo, StudentsBaseInfo, StudentsFamilyInfo, \
    NewStudentTransferIn, StudentGraduation, StudentsKeyinfoChange, StudentsKeyinfoChangeAudit, NewStudentsQuery
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest

from mini_framework.design_patterns.depend_inject import get_injector
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from rules.student_session_rule import StudentSessionRule
from rules.students_family_info_rule import StudentsFamilyInfoRule
from views.models.students import StudentSession, StudentsUpdateFamilyInfo


class CurrentStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.student_session_rule = get_injector(StudentSessionRule)
        self.student_transaction_rule = get_injector(StudentTransactionRule)
        self.student_transaction_flow_rule = get_injector(StudentTransactionFlowRule)
        self.students_family_info_rule = get_injector(StudentsFamilyInfoRule)
        self.graduation_student_rule = get_injector(GraduationStudentRule)
        self.student_key_info_change_rule = get_injector(StudentsKeyInfoChangeRule)


    async def post_student_transaction_prepare(self,
                                               request:Request,
                                               ):
        """
        转学事务 准备 接口 检查数据返回状态
        """
        res = request.headers.get("data")
        return {"status": "prepared","data":res}

    async def post_student_transaction_precommit(self,
                                               request:Request,
                                               ):
        """
        转学事务 预提交 接口
        """
        res = request.headers.get("data")
        return {"status": "precommited","data":res}

    async def post_student_transaction_commit(self,
                                                 request:Request,
                                                 ):
        """
        转学事务 提交 接口
        """
        res = request.headers.get("data")
        return {"status": "commited2","data":res}

    async def post_student_transaction_rollback(self,
                                              request:Request,
                                              ):
        """
        转学事务 回滚 接口
        """
        res = request.headers.get("data")
        return {"status": "rollbacked","data":res}