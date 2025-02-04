from typing import Optional

from fastapi import Query, Depends, Body
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.views import BaseView
from starlette.requests import Request

from common.decorators import require_role_permission
from rules.teacher_borrow_rule import TeacherBorrowRule
from rules.teacher_retire_rule import TeacherRetireRule
from rules.teacher_transaction_rule import TeacherTransactionRule
from rules.teachers_rule import TeachersRule
from rules.transfer_details_rule import TransferDetailsRule
from views.common.common_view import get_extend_params
from views.models.system import UnitType
from views.models.teacher_transaction import TeacherBorrowModel, TeacherBorrowQueryModel, \
    TeacherRetireQuery, TeacherRetireCreateModel
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionQuery, \
    TeacherTransferQueryModel, TeacherTransactionQueryModel
from views.models.teacher_transaction import TransferDetailsModel
from views.models.teachers import TeacherAdd
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO

class TransferDetailsView(BaseView):
    def __init__(self):
        super().__init__()
        self.transfer_details_rule = get_injector(TransferDetailsRule)
        self.teacher_rule = get_injector(TeachersRule)

    async def get_transfer_details(self,
                                   transfer_details_id: str = Query(None, title="transfer_detailsID",
                                                                    description="transfer_detailsID", example=1234)
                                   ):
        """
        审批时仅查看调动信息，无日志信息
        """
        transfer_details_id = int(transfer_details_id)
        res = await self.transfer_details_rule.get_transfer_details_by_transfer_details_id(transfer_details_id)
        return res

    @require_role_permission("teacherTransferIn", "edit")
    async def post_transfer_in_details(self, transfer_details: TransferDetailsModel,
                                       add_teacher: Optional[TeacherAdd] = None,
                                       # transfer_inner: bool = Query(True, title="transfer_status",
                                       #                              description="transfer_status",
                                       #                              example=True)
                                       ):
        """
        调入
        """

        user_id = request_context_manager.current().current_login_account.name
        if add_teacher != None:
            await self.transfer_details_rule.add_transfer_in_outer_details(add_teacher, transfer_details, user_id)
        else:
            await self.transfer_details_rule.add_transfer_in_inner_details(transfer_details, user_id)
        return

    @require_role_permission("teacherTransferOut", "edit")
    async def post_transfer_out_details(self, transfer_details: TransferDetailsModel):
        """
        调出
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.transfer_details_rule.add_transfer_out_details(transfer_details, user_id)
        return res

    # async def delete_transfer_details(self,
    #                                   transfer_details_id: int = Query(None, title="transfer_detailsID",
    #                                                                    description="transfer_detailsID", example=1234)
    #                                   ):
    #     await self.transfer_details_rule.delete_transfer_details(transfer_details_id)

    # async def put_transfer_details(self, transfer_details: TransferDetailsReModel):
    #     res = await self.transfer_details_rule.update_transfer_details(transfer_details)
    #     return res

    async def get_transfer_details_all(self, teacher_id: str = Query(None, title="transfer_ID",
                                                                     description="transfer_ID", example=1234)):
        """
        查询单个老师所有调动信息,是教师详情页中的调动明细
        """
        teacher_id = int(teacher_id)
        return await self.transfer_details_rule.get_all_transfer_details(teacher_id)

    @require_role_permission("teacherTransferOut", "view")
    async def page_transfer_with_page(self, transfer_details=Depends(TeacherTransferQueryModel),
                                      page_request=Depends(PageRequest)):
        user_id = request_context_manager.current().current_login_account.name
        paging_result = await self.transfer_details_rule.query_transfer_with_page(transfer_details, page_request,
                                                                                  user_id)
        return paging_result

    @require_role_permission("teacherInfo", "transferIn")
    async def get_teacher_transfer(self, teacher_transaction=Depends(TeacherTransactionQuery)):
        """
        查询系统内有没有此人
        """
        res, transfer_inner = await self.transfer_details_rule.query_teacher_transfer(teacher_transaction)
        return res

    # 调动管理查询
    @require_role_permission("teacherInfo", "transferOut")
    async def page_transfer_out_launch(self, request: Request, transfer_details=Depends(TeacherTransferQueryModel),
                                       page_request=Depends(PageRequest)):
        """
        我发起的调出
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    transfer_details.original_district_area_id =school.borough
                else:
                    transfer_details.original_unit_id = tenant.origin_id
        # extend_param = {}
        # ob = await get_extend_params(request)
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     transfer_details.original_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            transfer_details.original_district_area_id = ob.county_id
        type = "launch"
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        paging_result = await self.transfer_details_rule.query_transfer_out_with_page(type, transfer_details,
                                                                                      page_request, extend_param)
        return paging_result

    @require_role_permission("teacherTransferOut", "approval")
    async def page_transfer_out_approval(self, request: Request, transfer_details=Depends(TeacherTransferQueryModel),
                                         page_request=Depends(PageRequest)):
        """
        我审批的调出
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    transfer_details.original_district_area_id =school.borough
                else:
                    transfer_details.original_unit_id = tenant.origin_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            transfer_details.original_district_area_id = ob.county_id
        type = "approval"
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        paging_result = await self.transfer_details_rule.query_transfer_out_with_page(type, transfer_details,
                                                                                      page_request, extend_param)
        return paging_result

    @require_role_permission("teacherInfo", "transferOut")
    async def page_transfer_in_launch(self, request: Request, transfer_details=Depends(TeacherTransferQueryModel),
                                      page_request=Depends(PageRequest)):
        """
        我发起的调入
        """
        type = "launch"
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    transfer_details.current_district_area_id =school.borough
                else:
                    transfer_details.current_unit_id= tenant.origin_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            transfer_details.current_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        paging_result = await self.transfer_details_rule.query_transfer_in_with_page(type, transfer_details,
                                                                                     page_request, extend_param)
        return paging_result

    @require_role_permission("teacherTransferIn", "approval")
    async def page_transfer_in_approval(self, request: Request, transfer_details=Depends(TeacherTransferQueryModel),
                                        page_request=Depends(PageRequest)):
        """
        我审批的调入
        """
        # todo 调入审批需要做两次查询，一次是系统内调入，需要查询之前单位，一次是系统外调入，需要查询之间的单位
        type = "approval"

        query_type = ""
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    transfer_details.current_district_area_id =school.borough
                else:
                    transfer_details.current_unit_id = tenant.origin_id
                    query_type = "school"
                    # transfer_details.original_unit_id = ob.school_id
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     transfer_details.current_unit_id = ob.school_id
        #     query_type = "school"

            # transfer_details.original_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            transfer_details.current_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        paging_result = await self.transfer_details_rule.query_transfer_in_with_page(type, transfer_details,
                                                                                     page_request, extend_param,
                                                                                     query_type)
        return paging_result

    # 调动审批
    # async def patch_transfer_submitting(self,
    #                                     transfer_details_id: int = Query(None, title="transfer_detailsID",
    #                                                                     description="transfer_detailsID", example=1234)):
    #     res = await self.transfer_details_rule.submitting(transfer_details_id)
    #     return res
    #
    # async def patch_transfer_submitted(self,
    #                                   transfer_details_id: int = Query(None, title="transfer_detailsID",
    #                                                                   description="transfer_detailsID", example=1234)):
    #     res = await self.transfer_details_rule.submitted(transfer_details_id)
    #     return res
    @require_role_permission("teacherTransferIn", "approval")
    async def patch_transfer_approved(self,
                                      teacher_id: str = Body(None, title="transfer_detailsID",
                                                             description="transfer_detailsID", example=1234),
                                      process_instance_id: str = Body(..., title="流程实例id",
                                                                      description="流程实例id",
                                                                      example=123),
                                      reason: str = Body("", title="reason",
                                                         description="审核理由")):

        user_id = request_context_manager.current().current_login_account.name
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        reason = reason
        res = await self.transfer_details_rule.transfer_approved(teacher_id, process_instance_id, user_id,
                                                                 reason)
        return res

    @require_role_permission("teacherTransferIn", "approval")
    async def patch_transfer_rejected(self,
                                      teacher_id: str = Body(None, title="教师id",
                                                             description="教师id", example=1234),
                                      process_instance_id: str = Body(..., title="流程实例id",
                                                                      description="流程实例id",
                                                                      example=123),
                                      reason: str = Body("", title="reason",
                                                         description="审核理由")):
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        res = await self.transfer_details_rule.transfer_rejected(teacher_id, process_instance_id, user_id,
                                                                 reason)
        return res

    @require_role_permission("teacherTransferIn", "revoke")
    async def patch_transfer_revoked(self,
                                     teacher_id: str = Body(None, title="教师id",
                                                            description="教师id", example=1234),
                                     process_instance_id: str = Body(..., title="流程实例id", description="流程实例id",
                                                                     example=123),
                                     reason: str = Body("", title="reason",
                                                        description="审核理由")):
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        res = await self.transfer_details_rule.transfer_revoked(teacher_id, process_instance_id, user_id,
                                                                reason)
        return res


# 异动相关
class TeacherTransactionView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_transaction_rule = get_injector(TeacherTransactionRule)

    @require_role_permission("teacherInfo", "transaction")
    async def get_teacher_transaction(self,
                                      teacher_transaction_id: int | str = Query(..., title="teacher_transactionID",
                                                                                description="teacher_transactionID",
                                                                                example=1234)
                                      ):
        teacher_transaction_id = int(teacher_transaction_id)
        # 异动审批中查询单个教师单个异动信息
        res = await self.teacher_transaction_rule.get_teacher_transaction_by_teacher_transaction_id(
            teacher_transaction_id)
        return res

    # 教师 异动接口
    @require_role_permission("teacherInfo", "transaction")
    async def post_teacher_transaction(self, teacher_transaction: TeacherTransactionModel):
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_transaction_rule.add_teacher_transaction_except_retire(teacher_transaction, user_id)
        return res

    # async def put_teacher_transaction(self, teacher_transaction: TeacherTransactionUpdateModel):
    #     res = await self.teacher_transaction_rule.update_teacher_transaction(teacher_transaction)
    #     return res
    @require_role_permission("teacherTransaction", "view")
    async def get_teacher_transaction_all(self, teacher_id: int | str = Query(None, title="teacher_transactionID",
                                                                              description="teacher_transactionID",
                                                                              example=1234)):
        """
        单个老师获取该老师的所有异动信息
        """
        teacher_id = int(teacher_id)
        return await self.teacher_transaction_rule.get_all_teacher_transaction(teacher_id)

    @require_role_permission("teacherTransaction", "view")
    async def page_transaction(self, request: Request, teacher_transaction=Depends(TeacherTransactionQueryModel),
                               page_request=Depends(PageRequest)):
        """
        分页查询
        """
        ob = await get_extend_params(request)
        paging_result = await self.teacher_transaction_rule.query_transaction_with_page(teacher_transaction,
                                                                                        page_request, ob)
        return paging_result

    # 异动审批
    # async def patch_transaction_submitting(self,
    #                                        teacher_transaction_id: int = Query(None, title="teacher_transactionID",
    #                                                                            description="teacher_transactionID",
    #                                                                            example=1234)):
    #     res = await self.teacher_transaction_rule.submitting(teacher_transaction_id)
    #     return res

    # async def patch_transaction_submitted(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
    #                                                                                 description="teacher_transactionID",
    #                                                                                 example=1234)):
    #     res = await self.teacher_transaction_rule.submitted(teacher_transaction_id)
    #     return res
    #
    # async def patch_transaction_approved(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
    #                                                                                description="teacher_transactionID",
    #                                                                                example=1234)):
    #     res = await self.teacher_transaction_rule.approved(teacher_transaction_id)
    #     return res
    #
    # async def patch_transaction_rejected(self, teacher_transaction_id: int = Query(None, title="teacher_transactionID",
    #                                                                                description="teacher_transactionID",
    #                                                                                example=1234)):
    #     res = await self.teacher_transaction_rule.rejected(teacher_transaction_id)
    #     return res
    @require_role_permission("teacherTransaction", "edit")
    async def patch_teacher_active(self,
                                   teacher_id: int | str = Body(..., title="教师编号", description="教师编号",
                                                                example=123),
                                   transaction_id: int | str = Body(..., title="教师变动记录编号",
                                                                    description="教师变动记录编号",
                                                                    example=123)):
        teacher_id = int(teacher_id)
        transaction_id = int(transaction_id)
        try:
            await self.teacher_transaction_rule.transaction_teacher_active(teacher_id, transaction_id)
            return True
        except Exception as e:
            return False


# 退休相关
class TeacherRetireView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_retire_rule = get_injector(TeacherRetireRule)

    @require_role_permission("teacherInfo", "retire")
    async def post_teacher_retire(self, teacher_retire: TeacherRetireCreateModel):
        """
        教师退休
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_retire_rule.add_teacher_retire(teacher_retire, user_id)
        return res

    @require_role_permission("teacherRetire", "view")
    async def page_teacher_retire(self, request: Request, current_teacher=Depends(TeacherRetireQuery),
                                  page_request=Depends(PageRequest)):
        """
        退休老师分页查询
        """
        ob = await get_extend_params(request)
        paging_result = await self.teacher_retire_rule.query_retire_teacher_with_page(current_teacher, page_request, ob)
        return paging_result


# 借动相关
class TeacherBorrowView(BaseView):
    def __init__(self):
        super().__init__()

        self.teacher_borrow_rule = get_injector(TeacherBorrowRule)
        self.teacher_rule = get_injector(TeachersRule)

    async def get_teacher_borrow(self,
                                 teacher_borrow_id: int | str = Query(None, title="teacher_borrowID",
                                                                      description="teacher_borrowID", example=1234)
                                 ):
        """
        审批时仅查看调动信息，无日志信息
        """
        teacher_borrow_id = int(teacher_borrow_id)
        res = await self.teacher_borrow_rule.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        return res

    @require_role_permission("teacherBorrowIn", "edit")
    async def post_teacher_borrow_in(self, teacher_borrow: TeacherBorrowModel,
                                     add_teacher: Optional[TeacherAdd] = None,
                                     ):
        """
        借入
        """
        user_id = request_context_manager.current().current_login_account.name
        if add_teacher != None:

            res = await self.teacher_borrow_rule.add_teacher_borrow_in_outer(add_teacher, teacher_borrow, user_id)
        else:
            res = await self.teacher_borrow_rule.add_teacher_borrow_in_inner(teacher_borrow, user_id)
        return res

    @require_role_permission("teacherBorrowOut", "edit")
    async def post_teacher_borrow_out(self, teacher_borrow: TeacherBorrowModel):
        """
        借出
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_borrow_rule.add_teacher_borrow_out(teacher_borrow, user_id)
        return res

    # async def delete_teacher_borrow(self,
    #                                 teacher_borrow_id: int = Query(None, title="teacher_borrowID",
    #                                                                description="teacher_borrowID", example=1234)
    #                                 ):
    #     await self.teacher_borrow_rule.delete_teacher_borrow(teacher_borrow_id)
    #
    # async def put_teacher_borrow(self, teacher_borrow: TeacherBorrowReModel):
    #     res = await self.teacher_borrow_rule.update_teacher_borrow(teacher_borrow)
    #     return res

    async def get_teacher_borrow_all(self, teacher_id: int | str = Query(None, title="teacher_borrowID",
                                                                         description="teacher_borrowID", example=1234)):
        """
        获取单个老师所有借动信息,是教师详情页中的借动明细
        """
        teacher_id = int(teacher_id)
        return await self.teacher_borrow_rule.get_all_teacher_borrow(teacher_id)

    @require_role_permission("teacherBorrowOut", "view")
    async def page_borrow_with_page(self, teacher_borrow=Depends(TeacherBorrowQueryModel),
                                    page_request=Depends(PageRequest)):
        """
        分页查询
        """
        user_id = request_context_manager.current().current_login_account.name
        paging_result = await self.teacher_borrow_rule.query_teacher_borrow_with_page(teacher_borrow, page_request,
                                                                                      user_id)
        return paging_result

    # async def get_teacher_borrow_in_system(self, teacher_borrow: TeacherTransactionQuery):
    #     """
    #     查询老师是否在系统内
    #     """
    #     return await self.teacher_borrow_rule.query_teacher_transfer(teacher_borrow)

    # 借动管理查询
    @require_role_permission("teacherBorrowOut", "view")
    async def page_borrow_out_launch(self, request: Request, teacher_borrow=Depends(TeacherBorrowQueryModel),
                                     page_request=Depends(PageRequest)):
        """
       我发起的借出
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    teacher_borrow.original_district_area_id =school.borough
                else:
                    teacher_borrow.original_unit_id = tenant.origin_id
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     teacher_borrow.original_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            teacher_borrow.original_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = "launch"
        paging_result = await self.teacher_borrow_rule.query_borrow_out_with_page(type, teacher_borrow, page_request,
                                                                                  extend_param)
        return paging_result

    @require_role_permission("teacherBorrowOut", "approval")
    async def page_borrow_out_approval(self, request: Request, teacher_borrow=Depends(TeacherBorrowQueryModel),
                                       page_request=Depends(PageRequest)):
        """
        我审批的借出
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    teacher_borrow.original_district_area_id =school.borough
                else:
                    teacher_borrow.original_unit_id = tenant.origin_id
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     teacher_borrow.original_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            teacher_borrow.original_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = "approval"
        paging_result = await self.teacher_borrow_rule.query_borrow_out_with_page(type, teacher_borrow, page_request,
                                                                                  extend_param)
        return paging_result

    @require_role_permission("teacherBorrowIn", "view")
    async def page_borrow_in_launch(self, request: Request, teacher_borrow=Depends(TeacherBorrowQueryModel),
                                    page_request=Depends(PageRequest)):
        """
        我发起的借入
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    teacher_borrow.current_district_area_id =school.borough
                else:
                    teacher_borrow.current_unit_id = tenant.origin_id
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     teacher_borrow.current_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            teacher_borrow.current_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = "launch"
        paging_result = await self.teacher_borrow_rule.query_borrow_in_with_page(type, teacher_borrow, page_request,
                                                                                 extend_param)
        return paging_result

    @require_role_permission("teacherBorrowIn", "approval")
    async def page_borrow_in_approval(self, request: Request, teacher_borrow=Depends(TeacherBorrowQueryModel),
                                      page_request=Depends(PageRequest)):
        """
        我审批的借入
        """
        # todo 调入审批需要做两次查询，一次是系统内调入，需要查询之前单位，一次是系统外调入，需要查询之间的单位
        query_type = ""
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.tenant:
            tenant_dao = get_injector(TenantDAO)
            tenant = await tenant_dao.get_tenant_by_code(ob.tenant.code)
            if ob.tenant.code == "210100":
                pass
            elif tenant.tenant_type == "planning_school":
                pass
            elif tenant.tenant_type == "school":
                school_dao = get_injector(SchoolDAO)
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if not school:
                    return "学校不存在"
                if school.institution_category == "institution":
                    teacher_borrow.current_district_area_id =school.borough
                else:
                    teacher_borrow.current_unit_id  = tenant.origin_id
                    query_type = "school"
        # if ob.unit_type == UnitType.SCHOOL.value:
        #     teacher_borrow.current_unit_id = ob.school_id
        #     query_type = "school"

            # teacher_borrow.original_unit_id = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            teacher_borrow.current_district_area_id = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = "approval"
        paging_result = await self.teacher_borrow_rule.query_borrow_in_with_page(type, teacher_borrow, page_request,
                                                                                 extend_param,query_type)
        return paging_result

    # 审批相关
    # async def patch_borrow_submitting(self,
    #                                   teacher_borrow_id: int = Query(None, title="teacher_borrowID",
    #                                                                  description="teacher_borrowID", example=1234)):
    #     res = await self.teacher_borrow_rule.submitting(teacher_borrow_id)
    #     return res
    #
    # async def patch_borrow_submitted(self, teacher_borrow_id: int = Query(None, title="teacher_borrowID",
    #                                                                       description="teacher_borrowID",
    #                                                                       example=1234)):
    #     res = await self.teacher_borrow_rule.submitted(teacher_borrow_id)
    #     return res
    @require_role_permission("teacherBorrowIn", "approval")
    async def patch_borrow_approved(self,
                                    teacher_id: int | str = Body(None, title="transfer_detailsID",
                                                                 description="transfer_detailsID", example=1234),
                                    process_instance_id: int | str = Body(..., title="流程实例id",
                                                                          description="流程实例id",
                                                                          example=123),
                                    reason: str = Body("", title="reason",
                                                       description="审核理由")):
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        res = await self.teacher_borrow_rule.borrow_approved(teacher_id, process_instance_id, user_id,
                                                             reason)
        return res

    @require_role_permission("teacherBorrowIn", "approval")
    async def patch_borrow_rejected(self,
                                    teacher_id: int | str = Body(None, title="transfer_detailsID",
                                                                 description="transfer_detailsID", example=1234),
                                    process_instance_id: int | str = Body(..., title="流程实例id",
                                                                          description="流程实例id",
                                                                          example=123),
                                    reason: str = Body("", title="reason",
                                                       description="审核理由")):
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        res = await self.teacher_borrow_rule.borrow_rejected(teacher_id, process_instance_id, user_id,
                                                             reason)
        return res

    @require_role_permission("teacherBorrowIn", "revoke")
    async def patch_borrow_revoked(self,
                                   teacher_id: int | str = Body(None, title="transfer_detailsID",
                                                                description="transfer_detailsID", example=1234),
                                   process_instance_id: int | str = Body(..., title="流程实例id",
                                                                         description="流程实例id",
                                                                         example=123),
                                   reason: str = Body("", title="reason",
                                                      description="审核理由")):
        user_id = request_context_manager.current().current_login_account.name
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        reason = reason
        res = await self.teacher_borrow_rule.borrow_revoked(teacher_id, process_instance_id, user_id,
                                                            reason)
        return res

    @require_role_permission("teacherBorrowIn", "edit")
    async def patch_teacher_borrow_active(self,
                                          teacher_id: int | str = Body(..., title="教师编号", description="教师编号",
                                                                       example=123),
                                          process_instance_id: int | str = Body(..., title="教师变动记录编号",
                                                                                description="教师变动记录编号",
                                                                                example=123)):
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        await self.teacher_borrow_rule.borrow_teacher_active(teacher_id, process_instance_id)
        return teacher_id
