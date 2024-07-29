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
from views.models.class_division_records import ClassDivisionRecordsSearchRes
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
    async def sync_shine_newstudent_classdivision(self,
                                            enrollment_number: str = Query('', title="", description="报名号",
                                                                           min_length=1, max_length=30, example=''),
                                            school_id: int | str = Query(0, title="", description="学校ID", example=''),
                                            id_type: str = Query('', title="", description="身份证件类型", min_length=1,
                                                                 max_length=30, example=''),
                                            student_name: str = Query('', title="", description="姓名", min_length=1,
                                                                      max_length=30, example=''),
                                            created_at: str = Query('', title="", description="分班时间", min_length=1,
                                                                    max_length=30, example=''),
                                            student_gender: str = Query('', title="", description="性别", min_length=1,
                                                                        max_length=30, example=''),
                                            class_id: int | str = Query(0, title="", description="班级", example=''),
                                            status: str = Query('', title="", description="状态", min_length=1,
                                                                max_length=30, example=''),
                                            page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.class_division_records_rule.query_class_division_records_with_page(
            page_request, school_id, id_type, student_name, created_at, student_gender, class_id, status,
            enrollment_number, )
        return paging_result


    # 修改分班
    async def patch_newstudent_classdivision(self,
                                             class_id: int | str = Query(..., title="", description="班级ID", ),
                                             student_id: str = Query(..., title="", description="学生ID/逗号分割", ),

                                             ):
        """
        分班 捕获异常
        """
        try:
            res = None
            if class_id:
                class_id = int(class_id)
            # 学生班级和学生状态
            res = await self.students_base_info_rule.update_students_class_division(class_id, student_id)
            # 分班记录
            res_div = await self.class_division_records_rule.add_class_division_records(class_id, student_id)
            # 更新学生的 班级和 学校信息
            student_ids = student_id
            if ',' in student_ids:
                student_ids = student_ids.split(',')
            else:
                student_ids = [student_ids]
            for student_id in student_ids:
                baseinfo = StudentsBaseInfo(student_id=student_id, class_id=class_id, school_id=res_div.school_id,
                                            grade_id=res_div.grade_id)

                res3 = await self.students_base_info_rule.update_students_base_info(baseinfo)

        except ValueError as e:
            traceback.print_exc()
            return e
        except Exception as e:
            print(e)
            traceback.print_exc()

            return e

        return res


    # 分页查询
    async def page_newstudent_classdivision(self,
                                            enrollment_number: str = Query('', title="", description="报名号",
                                                                           min_length=1, max_length=30, example=''),
                                            school_id: int | str = Query(0, title="", description="学校ID", example=''),
                                            id_type: str = Query('', title="", description="身份证件类型", min_length=1,
                                                                 max_length=30, example=''),
                                            student_name: str = Query('', title="", description="姓名", min_length=1,
                                                                      max_length=30, example=''),
                                            created_at: str = Query('', title="", description="分班时间", min_length=1,
                                                                    max_length=30, example=''),
                                            student_gender: str = Query('', title="", description="性别", min_length=1,
                                                                        max_length=30, example=''),
                                            class_id: int | str = Query(0, title="", description="班级", example=''),
                                            status: str = Query('', title="", description="状态", min_length=1,
                                                                max_length=30, example=''),
                                            page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.class_division_records_rule.query_class_division_records_with_page(
            page_request, school_id, id_type, student_name, created_at, student_gender, class_id, status,
            enrollment_number, )
        return paging_result



