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
from common.decorators import require_role_permission
from rules.class_division_records_rule import ClassDivisionRecordsRule
from rules.operation_record import OperationRecordRule
from views.common.common_view import compare_modify_fields, get_client_ip, convert_query_to_none, get_extend_params
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


class NewsStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.class_division_records_rule = get_injector(ClassDivisionRecordsRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
    # 新增学生 只含基本信息
    @require_role_permission("new_student", "open")
    async def post_newstudent(self, students: NewStudents):
        """
        新增新生信息
        """
        res = await self.students_rule.add_students(students)
        students.student_id = res.student_id
        special_date = datetime.datetime.now()

        vm2 = NewBaseInfoCreate(student_id=students.student_id, school_id=students.school_id,
                                registration_date=special_date.strftime("%Y-%m-%d"))
        res2 = await self.students_base_info_rule.add_students_base_info(vm2)

        return res

    # 分页查询
    #
    @require_role_permission("new_student", "view")

    async def page_newstudent(self,
                              request:Request,

                              new_students_query=Depends(NewStudentsQuery),


                              page_request=Depends(PageRequest),
                              ):
        """
        分页查询
        """
        obj= await get_extend_params(request)

        paging_result = await self.students_base_info_rule.query_students_base_info_with_page(new_students_query,
                                                                                              page_request,obj)
        return paging_result

    async def get_newstudentkeyinfo(self, student_id: str = Query(..., title="", description="学生id",
                                                                  example="1")):
        """新生查询关键信息"""
        res = await self.students_rule.get_students_by_id(student_id)

        return res

    @require_role_permission("new_student", "edit")

    async def put_newstudentkeyinfo(self, new_students_key_info: StudentsKeyinfo, request: Request):
        """"
        新生编辑关键信息
        """
        check = await self.students_rule.is_can_update_student(new_students_key_info.student_id)
        if not check:
            raise StudentStatusError()

        origin = await self.students_rule.get_students_by_id(new_students_key_info.student_id)
        log_con = compare_modify_fields(new_students_key_info, origin)

        print(new_students_key_info)
        res = await self.students_rule.update_students(new_students_key_info)

        # log_con=''
        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="修改关键信息",
            action_target_id=str(new_students_key_info.student_id),
            change_data=json_string,

        ))
        return res

    async def delete_newstudentkeyinfo(self, student_id: str = Query(..., title="", description="学生id", )):
        """
        删除新生关键信息
        """
        await self.students_rule.delete_students(student_id)
        return str(student_id)
    @require_role_permission("new_student", "flowout")

    async def patch_newstudent_flowout(self, new_students_flow_out: NewStudentsFlowOut):
        """
        新生流出
        """
        new_students_flow_out = convert_query_to_none(new_students_flow_out)
        check = await self.students_rule.is_can_update_student(new_students_flow_out.student_id)
        if not check:
            raise StudentStatusError()
            # return "该学生状态不允许流出"

        res_base_info = await self.students_base_info_rule.update_students_base_info( new_students_flow_out)  # 修改基本信息中的流出时间等
        res_base_info2 = await self.students_rule.update_students( NewStudentsQueryRe(student_id=new_students_flow_out.student_id,approval_status=StudentApprovalAtatus.OUT.value))  # 修改基本信息中的流出时间等
        return res_base_info

    # todo 仅仅修改一个状态就行
    # 正式录取接口
    @require_role_permission("new_student", "formaladmission")

    async def patch_formaladmission(self, student_id: str = Query(..., description="学生id", example=["123,569,987"]),
                                    ):
        print(student_id)
        res = await self.students_rule.update_student_formaladmission(student_id, )
        return res

    # 导入   任务队列的
    @require_role_permission("new_student", "import")

    async def post_new_student_import(self,
                                      # file_name: str = Body(..., description="文件名"),
                                      file: PlanningSchoolImportReq

                                      # bucket: str = Query(..., description="文件名"),
                                      # scene: str = Query('', description="文件名"),
                                      ) -> Task:
        file_name = file.file_name
        task_model = PlanningSchoolFileStorageModel(file_name=file_name, virtual_bucket_name=file.bucket_name,
                                                    file_size='51363', scene=ImportScene.NEWSTUDENT.value)

        task = Task(
            # todo sourcefile无法记录3个参数  故 暂时用3个参数来实现  需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="school_task_new_student_import",
            # 文件 要对应的 视图模型
            payload=task_model,
            # payload=NewStudentTask(file_name=filename, bucket=bucket, scene=scene),
            # payload=NewStudentTask(file_name=file_name, scene= ImportScene.NEWSTUDENT.value, bucket='new_student_import' ),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task


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

    async def get_newstudentbaseinfo(self, student_id: str = Query(..., title="学生ID", description="学生ID",
                                                                   example="1")):
        """
        查询新生基本信息
        """
        res = await self.students_base_info_rule.get_students_base_info_by_student_id(student_id)
        return res
    # 新增学生基本信息
    async def post_newstudentbaseinfo(self, new_students_base_info: NewBaseInfoCreate):
        """
        新生新增基本信息
        """
        check = await self.students_rule.is_can_update_student(new_students_base_info.student_id)
        if not check:
            raise StudentStatusError()
        res = await self.students_base_info_rule.add_students_base_info(new_students_base_info)
        return res
    # 保存学生基本信息 触发对接组织中心
    async def put_newstudentbaseinfo(self, new_students_base_info: NewBaseInfoUpdate, request: Request):
        """
        新生编辑基本信息
        """
        check = await self.students_rule.is_can_update_student(new_students_base_info.student_id)
        if not check:
            raise StudentStatusError()

        origin = await self.students_base_info_rule.get_students_base_info_by_student_id(
            new_students_base_info.student_id)
        log_con = compare_modify_fields(new_students_base_info, origin)
        # 如果日期是字符串型 转换为date
        if isinstance(new_students_base_info.admission_date, str):
            # 先截取10位长度
            new_students_base_info.admission_date = new_students_base_info.admission_date[:10]
            # 创建一个date对象
            # 使用 strptime 方法将字符串转换为 datetime 对象
            datetime_object = datetimealias.strptime(new_students_base_info.admission_date, '%Y-%m-%d')

            # 然后，如果您需要一个 date 对象，可以通过 datetime 对象的 date 方法获取
            new_students_base_info.admission_date = datetime_object.date()

        res = await self.students_base_info_rule.update_students_base_info(new_students_base_info)

        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="新生编辑基本信息",
            action_target_id=str(new_students_base_info.student_id),
            change_data=json_string,

        ))
        return res

    # 修改分班
    @require_role_permission("classdivision", "open")
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

    # 摇号分班  未使用
    @require_role_permission("classdivision", "lottery_classdivision")

    async def patch_newstudent_lottery_classdivision(self,
                                                     background_tasks: BackgroundTasks,

                                                     school_id: int | str = Query(..., title="",
                                                                                  description="学校ID", ),
                                                     grade_id: int | str = Query(..., title="", description="年级ID", ),

                                                     ):
        """
        """
        background_tasks.add_task(self.lottery_class_division, (school_id, grade_id), message="some notification")
        return {"message": "Notification sent in the background"}

    #
    def lottery_class_division(self, args, message=""):
        print(args, message)
        with open("log.txt", mode="a") as log:
            log.write(message)

    # 分页查询
    @require_role_permission("classdivision", "view")

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

    async def delete_newstudentbaseinfo(self,
                                        student_id: str = Query(..., title="学生ID", description="学生ID", )):
        """
        新生删除基本信息
        """
        await self.students_base_info_rule.delete_students_base_info(student_id)
        return str(student_id)


class NewsStudentsFamilyInfoView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_family_info_rule = get_injector(StudentsFamilyInfoRule)
        self.operation_record_rule = get_injector(OperationRecordRule)

    async def post_newstudentfamilyinfo(self, new_students_family_info: StudentsFamilyInfoCreate):
        """
        新生增加家庭信息
        """
        res = await self.students_family_info_rule.add_students_family_info(new_students_family_info)

        return res

    async def put_newstudentfamilyinfo(self, new_students_family_info: StudentsUpdateFamilyInfo, request: Request):
        """
        新生编辑家庭信息  变更日志
        """
        origin = await self.students_family_info_rule.get_students_family_info_by_id(
            new_students_family_info.student_family_info_id)
        log_con = compare_modify_fields(new_students_family_info, origin)
        res = await self.students_family_info_rule.update_students_family_info(new_students_family_info)
        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(

            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.FAMILY_INFO_CHANGE.value,
            change_detail="新生编辑家庭信息",
            action_target_id=str(new_students_family_info.student_id),
            change_data=json_string,

        ))
        return res

    async def delete_newstudentfamilyinfo(self,
                                          student_family_info_id: str = Query(..., title="学生家庭成员ID",
                                                                              description="学生家庭成员ID", )):
        """
        新生删除家庭信息
        """
        await self.students_family_info_rule.delete_students_family_info(student_family_info_id)
        return str(student_family_info_id)

    async def get_newstudentfamilyinfo(self,
                                       student_family_info_id: str = Query(..., title="学生家庭成员ID",
                                                                           description="学生家庭成员ID", )):
        """
        查询单条家庭信息
        """
        res = await self.students_family_info_rule.get_students_family_info_by_id(student_family_info_id)
        return res

    async def get_newstudentfamilyinfoall(self,
                                          student_id: str = Query(..., title="学生ID", description="学生ID", )):
        """
        新生查询家庭信息
        """
        res = await self.students_family_info_rule.get_all_students_family_info(student_id)
        return res

    # 新生导出

    async def post_new_student_export(self,
                                      students_query=Depends(NewStudentsQuery),

                                      ) -> Task:
        students_query.approval_status = [StudentApprovalAtatus.ENROLLMENT]

        task = Task(
            task_type="school_task_student_export",
            payload=students_query,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 分班导出
    async def post_newstudent_classdivision_export(self,
                                                   students_query=Depends(ClassDivisionRecordsSearchRes),

                                                   ) -> Task:
        # students_query.approval_status =   [StudentApprovalAtatus.ENROLLMENT  ]

        task = Task(
            task_type="school_task_newstudent_classdivision_export",
            payload=students_query,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 学生家庭成员导入
    async def post_newstudent_familyinfo_import(self,
                                                file: PlanningSchoolImportReq
                                                ) -> Task:
        file_name = file.file_name
        task_model = PlanningSchoolFileStorageModel(file_name=file_name, virtual_bucket_name=file.bucket_name,
                                                    file_size='51363', scene=ImportScene.NEWSTUDENT_FAMILYINFO.value)
        task = Task(
            task_type="school_task_newstudent_familyinfo_import",
            # 文件 要对应的 视图模型
            payload=task_model,
            # payload=NewStudentTask(file_name=file_name, scene= ImportScene.NEWSTUDENT_FAMILYINFO.value, bucket='newstudent_familyinfo_import' ),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task
