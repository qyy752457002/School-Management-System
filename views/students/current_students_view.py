from typing import List

from mini_framework.web.views import BaseView

from models.student_transaction import AuditAction
from rules.student_transaction import StudentTransactionRule
from rules.student_transaction_flow import StudentTransactionFlowRule
from views.models.student_transaction import StudentTransaction, StudentTransactionFlow
from views.models.students import NewStudents, StudentsKeyinfo, StudentsBaseInfo, StudentsFamilyInfo, StudentEduInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel
from rules.students_base_info_rule import StudentsBaseInfoRule
from mini_framework.design_patterns.depend_inject import get_injector
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from rules.student_session_rule import StudentSessionRule
from views.models.students import StudentSession


class CurrentStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.students_rule = get_injector(StudentsRule)
        self.student_session_rule = get_injector(StudentSessionRule)
        self.student_transaction_rule = get_injector(StudentTransactionRule)
        self.student_transaction_flow_rule = get_injector(StudentTransactionFlowRule)


    async def get_student_session(self,sessions_id: str = Query(None, title="届别编号", description="届别编号",
                                                                   example="2023届")):
        """
        在校生 查询届别信息
        """
        res = await self.student_session_rule.get_student_session_by_id(sessions_id)
        return res

    async def post_student_session(self,student_session: StudentSession):
        """
        在校生 新增届别信息
        """
        res = await self.student_session_rule.add_student_session(student_session)
        return res

    async def patch_student_session(self,student_session: StudentSession):
        """
        在校生 编辑届别信息
        """
        res = await self.student_session_rule.add_student_session(student_session)
        return res

    # 在校生转入    届别 班级
    async def patch_transferin(self, student_edu_info: StudentEduInfo):
        # print(new_students_key_info)
        student_edu_info.status=AuditAction.NEEDAUDIT.value
        res = await self.student_transaction_rule.add_student_transaction(student_edu_info)

        return res

    # 在校生转入   审批
    async def patch_transferin_audit(self, transferin_audit_id: int = Query(..., description="转入申请id",   example='2'),
                                     transferin_audit_action: AuditAction  = Query(..., description="审批的操作",   example='pass'),
                                     remark: str = Query("", description="审批的备注", min_length=0, max_length=200,   example='同意 无误'),

                                     ):
        # 审批通过 操作 或者拒绝
        student_edu_info =  StudentTransaction(id=transferin_audit_id,status=transferin_audit_action.value, )
        res = await self.student_transaction_rule.update_student_transaction(student_edu_info)
        # 流乘记录
        student_trans_flow =  StudentTransactionFlow( apply_id=transferin_audit_id,status=transferin_audit_action.value,remark=remark)

        res = await self.student_transaction_flow_rule.add_student_transaction_flow(student_trans_flow)


        # print(new_students_key_info)
        return res

    # 在校生转入   系统外转入 todo  单独模型 
    async def patch_transferin_fromoutside(self,
                                           student_baseinfo: NewStudents,
                                           student_edu_info_in: StudentEduInfo,
                                           student_edu_info_out: StudentEduInfo,

                                           ):
        # print(new_students_key_info)
        #  新增学生   同时写入 转出和转入 流程
        res = await self.students_rule.add_students(StudentEduInfo)


        return res

    # 在校生 系统外转出
    async def patch_transferout_tooutside(self, StudentEduInfo: StudentEduInfo,
                                          NewStudents: NewStudents,
                                          StudentoutEduInfo: StudentEduInfo,
                                          ):
        # print(new_students_key_info)
        return StudentEduInfo

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

    # 在校生 发起毕业 todo  支持传入部门学生ID或者  / all年级毕业
    async def patch_graduate(self,
                             student_id: List[str] = Query(..., description="学生ID", min_length=1, max_length=20,
                                                           example='SC2032633'),
                             graduate_status: str = Query(..., description="毕业状态", min_length=1, max_length=20,
                                                          example='结业'),
                             graduate_picture: str = Query(..., description="毕业照url", min_length=1, max_length=20,
                                                           example=''),
                             ):
        # print(new_students_key_info)
        return student_id

    # 在校生 查看关键信息

    async def get_studentkeyinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号",
                                                               example="SC2032633")):
        """
        在校生 查看关键信息
        """
        res = await self.students_rule.get_students_by_id(student_id)
        return res

    async def patch_studentkeyinfo(self, new_students_key_info: StudentsKeyinfo):
        """
        在校生 编辑关键信息
        """
        res = await self.students_rule.add_students(new_students_key_info)
        return res

    async def delete_studentkeyinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号", )):
        """
        在校生 删除关键信息
        """
        res = await self.students_rule.delete_students(student_id)
        return res

    async def get_studentbaseinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号",
                                                                example="SC2032633")):
        """
        在校生 查询基本信息
        """
        res = await self.students_base_info_rule.get_students_base_info_by_id(student_id)
        return res

    async def patch_studentbaseinfo(self, new_students_base_info: StudentsBaseInfo):
        """
        在校生 编辑基本信息
        """
        res = await self.students_base_info_rule.add_students_base_info(new_students_base_info)
        return res

    async def delete_studentbaseinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号", )):
        """
        在校生 删除基本信息
        """
        res = await self.students_base_info_rule.delete_students_base_info(student_id)
        return res

    async def get_studentfamilyinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号", )):
        """
        在校生 查询家庭信息
        """
        res = await self.students_base_info_rule.get_students_family_info_by_id(student_id)
        return res

    async def patch_studentfamilyinfo(self, new_students_family_info: StudentsFamilyInfo):
        """
        在校生 编辑家庭信息
        """
        res = await self.students_base_info_rule.add_students_family_info(new_students_family_info)
        return res

    async def delete_studentfamilyinfo(self, student_id: str = Query(None, title="学生编号", description="学生编号", )):
        """
        在校生 删除家庭信息
        """
        res = await self.students_base_info_rule.delete_students_family_info(student_id)
        return res
