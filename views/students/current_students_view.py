from typing import List

from mini_framework.web.views import BaseView

from models.student_transaction import AuditAction, TransactionDirection
from models.students import StudentGraduatedType
from rules.graduation_student_rule import GraduationStudentRule
from rules.student_transaction import StudentTransactionRule
from rules.student_transaction_flow import StudentTransactionFlowRule
from views.models.student_transaction import StudentTransaction, StudentTransactionFlow, StudentTransactionStatus, \
    StudentEduInfo, StudentTransactionAudit, StudentEduInfoOut
from views.models.students import NewStudents, StudentsKeyinfo, StudentsBaseInfo, StudentsFamilyInfo, \
    NewStudentTransferIn, StudentGraduation
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest

from mini_framework.design_patterns.depend_inject import get_injector
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from rules.student_session_rule import StudentSessionRule
from rules.students_family_info_rule import StudentsFamilyInfoRule
from views.models.students import StudentSession,StudentsUpdateFamilyInfo


class CurrentStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.student_session_rule = get_injector(StudentSessionRule)
        self.student_transaction_rule = get_injector(StudentTransactionRule)
        self.student_transaction_flow_rule = get_injector(StudentTransactionFlowRule)
        self.students_family_info_rule = get_injector(StudentsFamilyInfoRule)
        self.graduation_student_rule = get_injector( GraduationStudentRule)


    async def get_student_session(self, sessions_id: int  = Query(..., title="", description="届别id",
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
                           status: str = Query("", title="", description="状态",),
                                                                          page_request=Depends(PageRequest)
                        ):
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.student_session_rule.query_session_with_page(page_request ,status)
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

    # 在校生转入    届别 班级
    async def patch_transferin(self, student_edu_info: StudentEduInfo):
        # print(new_students_key_info)
        student_edu_info.status = AuditAction.NEEDAUDIT.value
        res = await self.student_transaction_rule.add_student_transaction(student_edu_info)

        return res

    # 在校生转入   审批
    async def patch_transferin_audit(self,
                                     audit_info:StudentTransactionAudit

                                     ):
        # 审批通过 操作 或者拒绝
        student_edu_info = StudentTransaction(id=audit_info.transferin_audit_id, status=audit_info.transferin_audit_action.value, )
        res = await self.student_transaction_rule.update_student_transaction(student_edu_info)
        # 流乘记录
        student_trans_flow = StudentTransactionFlow(apply_id=audit_info.transferin_audit_id, status=audit_info.transferin_audit_action.value,
                                                    remark=audit_info.remark)

        res = await self.student_transaction_flow_rule.add_student_transaction_flow(student_trans_flow)

        # print(new_students_key_info)
        return res

    # 在校生转入   系统外转入    单独模型
    async def patch_transferin_fromoutside(self,
                                           student_baseinfo: NewStudentTransferIn,
                                           student_edu_info_in: StudentEduInfo,
                                           student_edu_info_out: StudentEduInfoOut,

                                           ):
        # print(new_students_key_info)
        #  新增学生   同时写入 转出和转入 流程
        res_student = await self.students_rule.add_student_new_student_transferin(student_baseinfo)
        print(res_student)
        # 转出

        student_edu_info_out.status = AuditAction.NEEDAUDIT.value
        student_edu_info_out.student_id = res_student.student_id

        res_out = await self.student_transaction_rule.add_student_transaction(student_edu_info_out,
                                                                          TransactionDirection.OUT.value)

        # 转入

        student_edu_info_in.status = AuditAction.NEEDAUDIT.value
        student_edu_info_in.student_id = res_student.student_id
        student_edu_info_in.relation_id = res_out.id
        print(  res_out.id,000000)

        res = await self.student_transaction_rule.add_student_transaction(student_edu_info_in, TransactionDirection.IN.value,res_out.id)

        return res

    # 在校生 系统内转出
    async def patch_transferout_tooutside(self,
                                          student_edu_info_in: StudentEduInfo,
                                          student_edu_info_out: StudentEduInfo,
                                          student_id: int  = Query(..., description="学生id",   example='1'),

                                          ):
        # print(new_students_key_info)
        #      同时写入 转出和转入 流程
        res_student = await self.students_rule.get_students_by_id(student_id)
        print(res_student)
        # 转出

        student_edu_info_out.status = AuditAction.NEEDAUDIT.value
        student_edu_info_out.student_id = res_student.student_id

        res_out = await self.student_transaction_rule.add_student_transaction(student_edu_info_out,
                                                                              TransactionDirection.OUT.value)

        # 转入

        student_edu_info_in.status = AuditAction.NEEDAUDIT.value
        student_edu_info_in.student_id = res_student.student_id
        student_edu_info_in.relation_id = res_out.id
        # print(  res_out.id,000000)

        res = await self.student_transaction_rule.add_student_transaction(student_edu_info_in, TransactionDirection.IN.value,res_out.id)
        return res

    # # 在校生转入   审批同意
    # async def patch_transferin_auditpass(self,
    #                                      transferin_audit_id: str = Query(..., description="转入申请id", min_length=1,
    #                                                                       max_length=20, example='SC2032633'),
    #                                      remark: str = Query(..., description="备注", min_length=1, max_length=20,
    #                                                          example='SC2032633'),
    #                                      ):
    #     # print(new_students_key_info)
    #     return transferin_audit_id
    #
    # # 在校生转入   审批拒绝
    # async def patch_transferin_auditrefuse(self,
    #                                        transferin_audit_id: str = Query(..., description="转入申请id", min_length=1,
    #                                                                         max_length=20, example='SC2032633'),
    #                                        remark: str = Query(..., description="备注", min_length=1, max_length=20,
    #                                                            example='SC2032633'),
    #                                        ):
    #     # print(new_students_key_info)
    #     return transferin_audit_id

    # 在校生 发起毕业    todo  支持传入部门学生ID或者  / all年级毕业  批量另起
    async def patch_graduate(self,
                             student: StudentGraduation,
                             # student_id:  int  = Query(..., description="学生ID",
                             #                               example='1'),
                             # graduate_status: StudentGraduatedType = Query(..., description="毕业状态", min_length=1, max_length=20,
                             #                              example='completion'),
                             # graduate_remark: str = Query( '', description="毕业备注", min_length=1, max_length=250,
                             #                               example=''),
                             ):
        # print(new_students_key_info)
        res = await self.graduation_student_rule.update_graduation_student(student.student_id,student.graduation_type,student.graduation_remarks)

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
        在校生 编辑关键信息
        """
        res = await self.students_rule.update_students(new_students_key_info)
        return res

    async def delete_studentkeyinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        在校生 删除关键信息
        """
        await self.students_rule.delete_students(student_id)
        return str(student_id)

class CurrentStudentsBaseInfoView(BaseView):
    def __init__(self):
        super().__init__()
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

    async def put_studentbaseinfo(self, new_students_base_info: StudentsBaseInfo):
        """
        在校生 编辑基本信息
        """
        res = await self.students_base_info_rule.update_students_base_info(new_students_base_info)
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

    async def put_studentfamilyinfo(self, new_students_family_info: StudentsUpdateFamilyInfo):
        """
        新生编辑家庭信息
        """
        res = await self.students_family_info_rule.update_students_family_info(new_students_family_info)
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
                                       student_family_info_id: str = Query(..., title="学生编号", description="学生编号", )):
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