import datetime
import json
import traceback
from time import strptime
from typing import List
from datetime import datetime as datetimealias

from fastapi.params import Body
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.student import StudentStatusError
from rules.class_division_records_rule import ClassDivisionRecordsRule
from rules.operation_record import OperationRecordRule
from views.common.common_view import compare_modify_fields, get_client_ip, convert_query_to_none
from views.models.class_division_records import ClassDivisionRecordsSearchRes, ClassDivisionRecordsImport
from views.models.operation_record import OperationRecord, ChangeModule, OperationType, OperationType, OperationTarget
from views.models.planning_school import PlanningSchoolImportReq, PlanningSchoolFileStorageModel
from views.models.students import NewStudents, NewStudentsQuery, NewStudentsQueryRe, StudentsKeyinfo, StudentsBaseInfo, \
    StudentsFamilyInfo, NewStudentTask
# from fastapi import Field
from mini_framework.web.views import BaseView

from views.models.system import ImportScene
from views.models.teachers import NewTeacher, TeacherInfo
from fastapi import Query, Depends, BackgroundTasks

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.students import Student, StudentApprovalAtatus
from rules.students_rule import StudentsRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel
from views.models.students import NewStudents, NewBaseInfoCreate, NewBaseInfoUpdate, StudentsFamilyInfoCreate
from views.models.students import NewStudentsFlowOut, StudentsUpdateFamilyInfo
from datetime import date
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_family_info_rule import StudentsFamilyInfoRule



class NewsStudentsInfoView(BaseView):
    """
    新生基本信息
    """

    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.class_division_records_rule = get_injector(ClassDivisionRecordsRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
    # 供阳光分班结果同步
    async def post_newstudent_classdivision(self,
                                                  class_division_records:List[ClassDivisionRecordsImport],

                                            ):
        """

        """
        paging_result=None
        paging_result = await self.deal_newstudent_classdivision(class_division_records)

        # for class_division_record in class_division_records:

        return paging_result


    # 修改分班
    async def deal_newstudent_classdivision(self,
                                             class_division_records

                                             ):
        """
        分班 捕获异常
        """
        try:
            res = None
            # 根据编码转换ID 等操作
            res = await self.class_division_records_rule.add_class_division_records_and_update_student_baseinfo(class_division_records )


        except ValueError as e:
            traceback.print_exc()
            return e
        except Exception as e:
            print(e)
            traceback.print_exc()

            return e

        return res





