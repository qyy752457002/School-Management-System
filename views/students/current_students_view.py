import copy
import datetime
import json

from fastapi.params import Body
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
from mini_framework.utils.json import JsonUtils
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.student import StudentExistsThisSchoolError, StudentTransactionExistsError
from models.student_transaction import AuditAction, TransactionDirection, AuditFlowStatus
from rules.classes_rule import ClassesRule
from rules.graduation_student_rule import GraduationStudentRule
from rules.operation_record import OperationRecordRule
from rules.student_transaction import StudentTransactionRule
from rules.student_transaction_flow import StudentTransactionFlowRule
from rules.students_key_info_change_rule import StudentsKeyInfoChangeRule
from rules.system_rule import SystemRule
from views.common.common_view import compare_modify_fields, get_client_ip, convert_dates_to_strings
from views.models.operation_record import OperationRecord, ChangeModule, OperationType, OperationType, OperationTarget
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
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.system_rule = get_injector(SystemRule)
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.student_session_rule = get_injector(StudentSessionRule)
        self.student_transaction_rule = get_injector(StudentTransactionRule)
        self.student_transaction_flow_rule = get_injector(StudentTransactionFlowRule)
        self.students_family_info_rule = get_injector(StudentsFamilyInfoRule)
        self.graduation_student_rule = get_injector(GraduationStudentRule)
        self.student_key_info_change_rule = get_injector(StudentsKeyInfoChangeRule)

    async def get_student_session(self, sessions_id: int = Query(..., title="", description="届别id",
                                                                 example="1")):
        """
        在校生 查询届别信息
        """
        res = await self.student_session_rule.get_student_session_by_id(sessions_id)
        return res

    async def post_student_session(self, student_session: StudentSession):
        """
        在校生 新增届别信息
        """
        res = await self.student_session_rule.add_student_session(student_session)
        return res

    async def patch_student_session(self, student_session: StudentSession):
        """
        在校生 编辑届别信息
        """
        res = await self.student_session_rule.update_student_session(student_session)
        return res

    async def page_session(self,
                           session_name: str = Query("", title="", description="", ),
                           session_alias: str = Query("", title="", description="", ),
                           status: str = Query("", title="", description="状态", ),
                           page_request=Depends(PageRequest)
                           ):
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.student_session_rule.query_session_with_page(page_request, status,session_name,session_alias)
        return paging_result

    # 转学申请的 列表
    async def page_student_transaction(self,
                                       audit_status: StudentTransactionStatus = Query("", title="", description="状态",
                                                                                      examples=['needaudit']),
                                       student_name: str = Query("", title="",
                                                                 description="学生姓名", min_length=1, max_length=20),

                                       school_id: int = Query(0, title="", description="学校ID", ),
                                       student_gender: str = Query("", title="", description=" 学生性别", min_length=1,
                                                                   max_length=20),

                                       apply_user: str = Query("", title="",
                                                               description="申请人", min_length=1,
                                                               max_length=20, ),
                                       edu_no: str = Query("", title="  ", description=" 学籍号码", min_length=1,
                                                           max_length=20),

                                       page_request=Depends(PageRequest)):
        print(audit_status, )
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.student_transaction_rule.query_student_transaction_with_page(page_request,
                                                                                                audit_status,
                                                                                                student_name,
                                                                                                student_gender,
                                                                                                school_id,
                                                                                                apply_user,
                                                                                                edu_no

                                                                                                )
        return paging_result
    # 转学申请详情
    async def get_student_transaction_info(self,

                                           apply_id: int = Query(..., description=" ", example='1'),

                                           ):
        relationinfo = tinfo = ''
        # 转发去 工作流获取详细
        result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
            apply_id)
        if not result.get('json_data'):
            return {'工作流数据异常 无法解析'}

        json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
        if 'original_dict' in json_data.keys() and  json_data['original_dict']:
            result={**json_data['original_dict'],**result}


        return result

    # 在校生转入
    async def patch_transferin(self, student_edu_info: StudentEduInfo):
        # print(new_students_key_info)
        # 检测 重复发起
        is_lock = await self.student_transaction_rule.exist_undealed_student_transaction(student_edu_info.student_id)
        if is_lock:
            raise StudentTransactionExistsError()



        # 新增转学数据到库 用于接收流程ID后处理数据变更 后期可以采用工作流的分布式传参到另外一个接口来实现变更代替这里
        # 转出
        student_edu_info_out= copy.deepcopy(student_edu_info)
        # 读取当前在校信息  确保学校等信息这里都有
        res_student = await self.students_base_info_rule.get_students_base_info_by_student_id(student_edu_info.student_id)
        if res_student:

            student_edu_info_out.school_id = res_student.school_id
            student_edu_info_out.grade_id = res_student.grade_id
            student_edu_info_out.class_id = res_student.class_id
            class_rule = get_injector(ClassesRule)
            class_info =await class_rule.get_classes_by_id(res_student.class_id)

            student_edu_info_out.classes = class_info.class_name
            student_edu_info_out.major_id = class_info.major_for_vocational
            if student_edu_info_out.school_id== student_edu_info.school_id:
                raise StudentExistsThisSchoolError()
                pass

        student_edu_info_out.status = AuditAction.NEEDAUDIT.value
        student_edu_info_out=await self.students_rule.complete_info_students_by_id(student_edu_info_out)


        res_out = await self.student_transaction_rule.add_student_transaction(student_edu_info_out,
                                                                              TransactionDirection.OUT.value)


        # 调用审批流 创建
        stuinfo= await self.students_rule.get_students_by_id(student_edu_info.student_id)
        student_edu_info=await  self.students_rule.complete_info_students_by_id(student_edu_info)
        # student_edu_info.school_name = stuinfo.school_name

        origin_data = {'student_transaction_in': convert_dates_to_strings(student_edu_info.__dict__) , 'student_transaction_out': convert_dates_to_strings(student_edu_info_out.__dict__) , 'student_info': convert_dates_to_strings(stuinfo.__dict__) }

        res3 = await self.student_transaction_flow_rule.add_student_transaction_work_flow(student_edu_info,stuinfo,stuinfo,None, origin_data)
        process_instance_id= node_instance_id =  0
        if res3 and  len(res3)>0 :
            print(res3[0])
            process_instance_id = res3[1]['process_instance_id']
            node_instance_id = res3[1]['node_instance_id']


        # 转入信息
        student_edu_info.relation_id = res_out.id
        student_edu_info.process_instance_id =  process_instance_id
        # print('debug-----222222222222',res_out)

        student_edu_info.status = AuditAction.NEEDAUDIT.value
        audit_info = res = await self.student_transaction_rule.add_student_transaction(student_edu_info, TransactionDirection.IN.value,res_out.id )

        # 转学日志

        origin =  student_edu_info_out
        log_con = compare_modify_fields(student_edu_info, origin)

        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.STUDENT_TRANSACTION.value,
            change_detail="转学",
            action_target_id=str(student_edu_info.student_id),
            # change_data=json_string,
            process_instance_id= process_instance_id
        ))

        return res3

    # 在校生转入   发起审批
    async def patch_transferin_audit(self,
                                     audit_info: StudentTransactionAudit

                                     ):
        # todo 校验必须是转出校的老师才能审批  调用推进

        # 审批通过 操作 或者拒绝

        # 流乘记录 初审  转出校/转如校的老师 都会调用审批流    todo 假设终态  则调用事务和审批流
        # student_trans_flow = StudentTransactionFlow(apply_id=audit_info.transferin_audit_id,
        #                                             status=audit_info.transferin_audit_action.value,
        #                                             stage=audit_info.transferin_audit_action.value,
        #                                             remark=audit_info.remark)
        # res = await self.student_transaction_flow_rule.add_student_transaction_flow(student_trans_flow)
        # 读取转学信息
        # student_transaction=await self.student_transaction_rule.get_student_transaction_by_id(audit_info.transferin_audit_id)
        resultra = await self.student_transaction_flow_rule.exe_student_transaction(audit_info,)
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        # print(new_students_key_info)
        return resultra
    # 转学异动 撤回
    async def patch_transaction_cancel(self,
                                       transferin_id: int = Query(..., description="转入申请id", example='2')

                                     # audit_info: StudentTransactionAudit

                                     ):
        # todo 校验是否本人或者老师

        # 流乘记录
        #  审批流取消
        res2 = await self.student_transaction_flow_rule.req_workflow_cancel(transferin_id,)
        await self.student_transaction_flow_rule.set_transaction_end(transferin_id,AuditAction.CANCEL)



        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        # print(new_students_key_info)
        return res2

    # 在校生转入    详情 就是工作流程的审核记录 各个阶段
    async def get_transferin_audit(self,
                                   apply_id: int = Query(..., description=" 列表接口返回的process_instance_id", example='1'),

                                   ):
        res = await self.student_transaction_flow_rule.query_student_transaction_flow(apply_id)

        # print(new_students_key_info)
        return res

    # 在校生转入   系统外转入
    async def patch_transferin_fromoutside(self,
                                           student_baseinfo: NewStudentTransferIn,
                                           student_edu_info_in: StudentEduInfo,
                                           student_edu_info_out: StudentEduInfoOut,
                                           ):
        # print(new_students_key_info)

        #  新增学生   同时写入 转出和转入 流程 在校生加 年级
        res_student_add = await self.students_rule.add_student_new_student_transferin(student_baseinfo)
        res_student_baseinfo = await self.students_base_info_rule.add_students_base_info(StudentsBaseInfo(student_id=res_student_add.student_id,edu_number=student_baseinfo.edu_number))

        print(res_student_add)

        # 检测 重复发起
        is_lock = await self.student_transaction_rule.exist_undealed_student_transaction(res_student_add.student_id)
        if is_lock:
            raise StudentTransactionExistsError()


        # 调用审批流 创建
        student_edu_info_in.student_id= res_student_add.student_id
        stuinfo= await self.students_rule.get_students_by_id(student_edu_info_in.student_id)

        origin_data = {'student_transaction_in':  '', 'student_transaction_out':convert_dates_to_strings( student_edu_info_out.__dict__), 'student_info':convert_dates_to_strings( res_student_add.__dict__), }
        # origin_datastr= JsonUtils.dict_to_json_str(origin_data) student_info
        origin_data['student_transaction_in'] = convert_dates_to_strings(student_edu_info_in.__dict__)

        res_workflow = await self.student_transaction_flow_rule.add_student_transaction_work_flow(student_edu_info_in,stuinfo,res_student_add,res_student_baseinfo,origin_data)
        process_instance_id= node_instance_id =  0
        if res_workflow and  len(res_workflow)>0 :
            print(res_workflow[0])
            process_instance_id = res_workflow[1]['process_instance_id']
            node_instance_id = res_workflow[1]['node_instance_id']
        else:
            return {'调用 审批流 失败'}
            pass
        # 转出
        student_edu_info_out.status = AuditAction.NEEDAUDIT.value
        student_edu_info_out.student_id = res_student_add.student_id
        res_out = await self.student_transaction_rule.add_student_transaction(student_edu_info_out,  TransactionDirection.OUT.value)

        # 转入
        student_edu_info_in.status = AuditAction.NEEDAUDIT.value
        student_edu_info_in.student_id = res_student_add.student_id
        student_edu_info_in.relation_id = res_out.id
        student_edu_info_in.process_instance_id = process_instance_id
        # print(res_out.id, 000000)

        res_student_transaction = await self.student_transaction_rule.add_student_transaction(student_edu_info_in, TransactionDirection.IN.value, res_out.id)

        # 转学日志

        origin =  student_edu_info_out
        log_con = compare_modify_fields(student_edu_info_in, origin)

        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.STUDENT_TRANSACTION.value,
            change_detail="转学",
            action_target_id=str(res_student_add.student_id),
            # change_data=json_string,
            process_instance_id= process_instance_id

        ))

        return res_student_transaction,res_workflow

    # 在校生 系统内转出
    async def patch_transferout_tooutside(self,
                                          student_edu_info_in: StudentEduInfoOut,
                                          # student_edu_info_out: StudentEduInfo,
                                          student_id: int = Query(..., description="学生id", example='1'),

                                          ):
        # print(new_students_key_info)
        # 检测 重复发起
        is_lock = await self.student_transaction_rule.exist_undealed_student_transaction(student_id)
        if is_lock:
            raise StudentTransactionExistsError()

        #      同时写入 转出和转入 流程
        res_student = await self.students_rule.get_students_by_id(student_id)
        print(res_student)
        # 转出 放到 rule里 读取 并插入装出
        # res = await self.students_rule.get_students_by_id(student_id)

        student_edu_info_out = await self.student_transaction_rule.get_student_edu_info_by_id(student_id, )

        student_edu_info_out.status = AuditAction.NEEDAUDIT.value
        student_edu_info_out.student_id = res_student.student_id
        # student_edu_info_out.process_instance_id = process_instance_id

        res_out = await self.student_transaction_rule.add_student_transaction(student_edu_info_out,
                                                                              TransactionDirection.OUT.value)

        # 调用审批流 创建
        student_edu_info_in.student_id= student_id
        stuinfo= await self.students_rule.get_students_by_id(student_edu_info_in.student_id)

        origin_data = {'student_transaction_in': convert_dates_to_strings(student_edu_info_in.__dict__), 'student_transaction_out': convert_dates_to_strings(student_edu_info_out.__dict__), 'student_info':convert_dates_to_strings(res_student.__dict__) , }

        res3 = await self.student_transaction_flow_rule.add_student_transaction_work_flow(student_edu_info_in,stuinfo,student_edu_info_in,None,origin_data)
        process_instance_id= node_instance_id =  0
        if res3 and  len(res3)>0 :
            print(res3[0])
            process_instance_id = res3[1]['process_instance_id']
            node_instance_id = res3[1]['node_instance_id']


        # 转入

        student_edu_info_in.status = AuditAction.NEEDAUDIT.value
        student_edu_info_in.student_id = res_student.student_id
        student_edu_info_in.relation_id = res_out.id
        # print(  res_out.id,000000)
        student_edu_info_in.process_instance_id = process_instance_id


        res = await self.student_transaction_rule.add_student_transaction(student_edu_info_in,
                                                                          TransactionDirection.IN.value, res_out.id)





        # 转学日志

        origin =  student_edu_info_out
        log_con = compare_modify_fields(student_edu_info_in, origin)

        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.STUDENT_TRANSACTION.value,
            change_detail="转学",
            action_target_id=str(student_id),
            # change_data=json_string,
            process_instance_id= process_instance_id
        ))
        return res,res3


    # 在校生 发起毕业    todo  支持传入部门学生ID或者  / all年级毕业  批量另起
    async def patch_graduate(self,
                             student: StudentGraduation,
                             ):
        # print(new_students_key_info)
        res = await self.graduation_student_rule.update_graduation_student(student.student_id, student.graduation_type,
                                                                           student.graduation_remarks)

        return res

    # 在校生 查看关键信息

    async def get_studentkeyinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号",
                                                               example="SC2032633")):
        """
        在校生 查看关键信息
        """
        res = await self.students_rule.get_students_by_id(student_id)
        return res

    async def put_studentkeyinfo(self, new_students_key_info: StudentsKeyinfo):
        """
        在校生 编辑关键信息 插入 关键信息变更表
        """
        res = await self.student_key_info_change_rule.add_student_key_info_change(new_students_key_info)
        # res = await self.students_rule.update_students(new_students_key_info)
        return res

    async def delete_studentkeyinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        在校生 删除关键信息
        """
        await self.students_rule.delete_students(student_id)
        return str(student_id)
#     撤回   审核  查看
    # 查看 学生 关键信息变更
    async def get_studentkeyinfochange(self, apply_id: str = Query(..., title=" 学生 关键信息变更的申请ID", description="",
                                                               example="1")):
        """
        在校生 查看关键信息变更
        """
        res = await self.student_key_info_change_rule.get_student_key_info_change_by_id(apply_id)
        return res
    # 撤回 学生 关键信息变更
    async def patch_studentkeyinfochange_cancel(self, apply_id: str = Query(..., title=" 学生 关键信息变更的申请ID", description="",
                                                                   example="1")):
        """
        在校生 查看关键信息变更 todo  审核状态
        """

        student_edu_info = StudentsKeyinfoChange(id=apply_id,
                                                      # approval_status=StudentTransactionStatus.CANCEL.value,
                                                 )
        res = await self.student_key_info_change_rule.update_student_key_info_change(student_edu_info)

        # res2 = await self.student_inner_transaction_rule.update_student_transaction(student_edu_info)
        #
        # # 流乘记录
        # student_trans_flow = StudentTransactionFlow(apply_id=transaction_id,
        #                                             status=StudentTransactionStatus.CANCEL.value,
        #                                             # stage=audit_info.transferin_audit_action.value,
        #                                             remark= '用户撤回')
        # res = await self.student_transaction_flow_rule.add_student_transaction_flow(student_trans_flow)

        return res
    #审核 学生 关键信息变更
    async def patch_studentkeyinfochange_audit(self,
        audit_info: StudentsKeyinfoChangeAudit

                                               ):


        student_inner_transaction_info = StudentsKeyinfoChange(id=audit_info.apply_id,
                                                                    approval_status=audit_info.audit_action.value)
        res = await self.student_key_info_change_rule.update_student_inner_transaction(student_inner_transaction_info)


        return res

    async def post_current_student_export(self,
        students_query=Depends(NewStudentsQuery),

                                          ) -> Task:
        task = Task(
            task_type="student_export",
            payload=students_query,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task
    # 转学申请详情
    async def get_student_transaction_info_biz(self,

                                           apply_id: int = Query(..., description=" ", example='1'),

                                           ):
        relationinfo = tinfo = ''
        tinfo = await self.student_transaction_rule.get_student_transaction_by_id(apply_id)

        if isinstance(tinfo, object) and hasattr(tinfo, 'relation_id') and tinfo.relation_id:
            relationinfo = await self.student_transaction_rule.get_student_transaction_by_id(tinfo.relation_id, )
            pass

        stubaseinfo = await self.students_rule.get_students_by_id(tinfo.student_id)
        # stubaseinfo=''

        return {'student_transaction_in': tinfo, 'student_transaction_out': relationinfo,
                'student_info': stubaseinfo, }

class CurrentStudentsBaseInfoView(BaseView):
    def __init__(self):
        super().__init__()
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.student_session_rule = get_injector(StudentSessionRule)

    async def get_studentbaseinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号",
                                                                example="SC2032633")):
        """
        在校生 查询基本信息
        """
        res = await self.students_base_info_rule.get_students_base_info_by_student_id(student_id)
        return res

    async def put_studentbaseinfo(self, new_students_base_info: StudentsBaseInfo,request: Request):
        """
        在校生 编辑基本信息
        """

        origin = await self.students_base_info_rule.get_students_base_info_by_student_id(new_students_base_info.student_id)
        log_con = compare_modify_fields(new_students_base_info, origin)

        res = await self.students_base_info_rule.update_students_base_info(new_students_base_info)

        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(new_students_base_info.student_id),
            change_data=json_string,

            ))
        return res

    async def delete_studentbaseinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        在校生 删除基本信息
        """
        res = await self.students_base_info_rule.delete_students_base_info(student_id)
        return res


class CurrentStudentsFamilyView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.students_family_info_rule = get_injector(StudentsFamilyInfoRule)
        self.operation_record_rule = get_injector(OperationRecordRule)

    async def put_studentfamilyinfo(self, new_students_family_info: StudentsUpdateFamilyInfo,request: Request):
        """
        新生编辑家庭信息
        """
        origin = await self.students_family_info_rule.get_students_family_info_by_id(new_students_family_info.student_family_info_id)
        log_con = compare_modify_fields(new_students_family_info, origin)

        res = await self.students_family_info_rule.update_students_family_info(new_students_family_info)
        json_string = json.dumps(log_con, ensure_ascii=False)
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.STUDENT.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.FAMILY_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(new_students_family_info.student_id),
            change_data=json_string,
            ))
        return res

    async def delete_studentfamilyinfo(self,
                                       student_family_info_id: str = Query(..., title="学生编号",
                                                                           description="学生编号", )):
        """
        新生删除家庭信息
        """
        await self.students_family_info_rule.delete_students_family_info(student_family_info_id)
        return str(student_family_info_id)

    async def get_tudentfamilyinfo(self,
                                   student_family_info_id: str = Query(..., title="学生编号",
                                                                       description="学生编号", )):
        """
        查询单条家庭信息
        """
        res = await self.students_family_info_rule.get_students_family_info_by_id(student_family_info_id)
        return res

    async def get_studentfamilyinfoall(self,
                                       student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        新生查询家庭信息
        """
        res = await self.students_family_info_rule.get_all_students_family_info(student_id)
        return res
