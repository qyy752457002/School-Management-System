import json
from typing import List

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.multi_tenant.registry import tenant_registry
from mini_framework.utils.json import JsonUtils
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.planning_school import PlanningSchoolValidateError, \
    PlanningSchoolStatusError
from common.decorators import require_role_permission
from models.student_transaction import AuditAction
from rules.common.common_rule import get_org_center_userinfo, verify_auth
from rules.leader_info_rule import LeaderInfoRule
from rules.operation_record import OperationRecordRule
from rules.school_communication_rule import SchoolCommunicationRule
from rules.school_eduinfo_rule import SchoolEduinfoRule
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import compare_modify_fields, convert_dates_to_strings, \
    serialize, convert_query_to_none, convert_snowid_in_model, get_extend_params,  get_tenant_by_code
from views.models.operation_record import OperationRecord, ChangeModule, OperationType, OperationTarget
from views.models.planning_school import PlanningSchoolBaseInfo, PlanningSchoolKeyInfo, \
    PlanningSchoolStatus, PlanningSchoolFounderType, PlanningSchoolPageSearch, PlanningSchoolKeyAddInfo, \
    PlanningSchoolBaseInfoOptional, PlanningSchoolTransactionAudit, PlanningSchoolImportReq, \
    PlanningSchoolFileStorageModel
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest

from rules.planning_school_rule import PlanningSchoolRule
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule

from rules.planning_school_eduinfo_rule import PlanningSchoolEduinfoRule
from views.models.system import ProcessCodeType, ImportScene


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class CustomValidationError:
    pass

"""
规划下  学校 事业 班级 新生 学生家庭 
学校  规划校 事业  在校生 新生 分班记录 
"""

class PlanningSchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        self.planning_school_eduinfo_rule = get_injector(PlanningSchoolEduinfoRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.system_rule = get_injector(SystemRule)
        self.school_rule = get_injector(SchoolRule)
        self.school_eduinfo_rule = get_injector(SchoolEduinfoRule)
        self.school_communication_rule = get_injector(SchoolCommunicationRule)
        self.leaderinfo_rule = get_injector(LeaderInfoRule)

    #   包含3部分信息 1.基本信息 2.通讯信息 3.教育信息
    @require_role_permission("planning_school", "view")
    async def get(self,
                  planning_school_id: int | str = Query(..., description="学校id|根据学校查规划校", example='1'),
                  ):
        planning_school = ''
        planning_school_communication = ''
        planning_school_eduinfo = ''
        extra_model = ''
        leaderinfo=None
        try:

            planning_school, extra_model = await self.planning_school_rule.get_planning_school_by_id(planning_school_id,
                                                                                                     PlanningSchoolKeyInfo)
            planning_school_communication = await self.planning_school_communication_rule.get_planning_school_communication_by_planning_shcool_id(
                planning_school_id)
            planning_school_eduinfo = await self.planning_school_eduinfo_rule.get_planning_school_eduinfo_by_planning_school_id(
                planning_school_id)
        #     增加返回领导信息
            leaderinfo = await self.leaderinfo_rule.get_all_leader_info(planning_school_id)
        except PlanningSchoolValidateError as e:
            print(e)

        return {'planning_school': planning_school, 'planning_school_communication': planning_school_communication,
                'planning_school_eduinfo': planning_school_eduinfo, 'planning_school_keyinfo': extra_model}
    @require_role_permission("planning_school", "open")
    async def post(self, planning_school: PlanningSchoolKeyAddInfo,
                   ):
        # 保存 模型 生产    必填 改掉    字段不变
        res = await self.planning_school_rule.add_planning_school(planning_school)
        resc = PlanningSchoolCommunications(id=0)
        newid = str(res.id)
        print(resc, '模型23', res.id, type(res.id))

        resc.planning_school_id = int(newid)
        print(resc, newid, '||||||||')

        # 保存通信信息
        res_comm = await self.planning_school_communication_rule.add_planning_school_communication(resc,
                                                                                                   convertmodel=False)
        print(res_comm, '模型2 res')
        #
        resedu = PlanningSchoolEduInfo(id=0)
        resedu.planning_school_id = res.id
        # 保存教育信息
        res_edu = await self.planning_school_eduinfo_rule.add_planning_school_eduinfo(resedu, convertmodel=False)
        print(res_edu)

        return res

    # # 修改 关键信息
    @require_role_permission("planning_school", "change_keyinfo")
    async def put_keyinfo(self,
                          planning_school: PlanningSchoolKeyInfo,
                          ):
        # 如果是草稿态 允许直接修改关键信息
        # 如果 不是normal态 也是允许修改关键信息的  但是要校验是否有待处理的流程ID
        # 如果是正式态 允许改 发起审核流程
        # 如果是关闭态 不允许这个操作
        is_can = await self.planning_school_rule.is_can_change_keyinfo(planning_school.id, )

        # 检测 是否允许修改
        is_draft = await self.planning_school_rule.is_can_not_add_workflow(planning_school.id, True)
        if is_draft or not is_can:
            raise PlanningSchoolStatusError()

        tinfo = origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)

        res2 = compare_modify_fields(planning_school, origin)
        # print(  res2)
        process_instance_id = 0

        if tinfo and tinfo.status == PlanningSchoolStatus.NORMAL.value:
            #  工作流
            res = await self.planning_school_rule.add_planning_school_keyinfo_change_work_flow(planning_school, )
            if res and len(res) > 1 and 'process_instance_id' in res[0].keys() and res[0]['process_instance_id']:
                process_instance_id = res[0]['process_instance_id']
                pl = PlanningSchoolBaseInfoOptional(id=planning_school.id, process_instance_id=process_instance_id,
                                                    workflow_status=AuditAction.NEEDAUDIT.value)

                res = await self.planning_school_rule.update_planning_school_byargs(pl)

                pass
            convert_snowid_in_model(res, ['id', 'process_instance_id'])
            #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
            res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
                action_target_id=str(planning_school.id),
                target=OperationTarget.PLANNING_SCHOOL.value,
                action_type=OperationType.MODIFY.value,
                change_module=ChangeModule.KEY_INFO_CHANGE.value,
                change_detail="修改基本信息",
                change_data=JsonUtils.dict_to_json_str(res2),
                process_instance_id=process_instance_id
            ))
            pass
        else:
            # 检测是否有待处理的流程ID
            res = await self.planning_school_rule.update_planning_school_byargs(planning_school)

            pass

        return res

    # 删除
    @require_role_permission("planning_school", "delete")
    async def delete(self, planning_school_id: int | str = Query(..., title="", description="学校id/园所id",
                                                                 example='2203'), ):
        print(planning_school_id)
        res = await self.planning_school_rule.softdelete_planning_school(planning_school_id)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.PLANNING_SCHOOL.value,
            action_type=OperationType.DELETE.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(planning_school_id),
            change_data=json.dumps(convert_dates_to_strings(serialize(res))),
        ))

        return res

    # 修改 变更 基本信息
    @require_role_permission("planning_school", "change_baseinfo")
    async def patch_baseinfo(self, planning_school_baseinfo: PlanningSchoolBaseInfo, ):

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school_baseinfo.id)
        log_con = compare_modify_fields(planning_school_baseinfo, origin)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school_baseinfo, )

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.PLANNING_SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(planning_school_baseinfo.id),
            change_data=JsonUtils.dict_to_json_str(log_con),
        ))

        return res

    # 规划校的审批流列表
    @require_role_permission("planning_school", "view")
    async def page_planning_school_audit(self,
                                         # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                                         process_code: str = Query("", title="流程代码",
                                                                   description="例如p_school_open", ),
                                         block: str = Query("", title=" ", description="地域管辖区", ),
                                         planning_school_code: str = Query("", title="", description=" 园所标识码", ),
                                         planning_school_level: str = Query("", title="", description=" 学校星级", ),
                                         planning_school_name: str = Query("", title="学校名称",
                                                                           description="1-20字符", ),
                                         planning_school_no: str = Query("", title="学校编号",
                                                                         description="学校编号/园所代码", min_length=1,
                                                                         max_length=20, ),
                                         borough: str = Query("", title="  ", description=" 行政管辖区", ),
                                         status: PlanningSchoolStatus = Query(None, title="", description=" 状态",
                                                                              examples=['正常']),

                                         founder_type: List[PlanningSchoolFounderType] = Query([], title="",
                                                                                               description="举办者类型",
                                                                                               examples=['地方']),
                                         founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                                                             examples=['教育部门']),
                                         founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                                                             examples=['县级教育部门']),

                                         page_request=Depends(PageRequest)):
        print(page_request, vars(ProcessCodeType))
        items = []
        req = PlanningSchoolPageSearch(block=block,
                                       planning_school_code=planning_school_code,
                                       planning_school_level=planning_school_level,
                                       planning_school_name=planning_school_name,
                                       planning_school_no=planning_school_no,
                                       borough=borough,
                                       status=status,
                                       founder_type=founder_type,
                                       founder_type_lv2=founder_type_lv2,
                                       founder_type_lv3=founder_type_lv3,
                                       )
        print('入参接收', req)
        paging_result = await self.system_rule.query_workflow_with_page(req, page_request, '', process_code, )
        print('333', page_request)
        return paging_result

    # 开办   校验合法性等  业务逻辑   开班式 校验所有的数据是否 都填写了
    @require_role_permission("planning_school", "open")
    async def patch_open(self, planning_school_id: str | int = Query(..., title="学校编号", description="学校id/园所id",
                                                                     min_length=1, max_length=20, example='SC2032633'),
                         is_add_log=True):
        # print(planning_school)
        # 检测 是否允许修改
        is_draft = await self.planning_school_rule.is_can_not_add_workflow(planning_school_id)
        if is_draft:
            raise PlanningSchoolStatusError()

        planning_school, extra_model = await self.planning_school_rule.get_planning_school_by_id(planning_school_id,
                                                                                                 PlanningSchoolBaseInfo)

        try:
            validated_data = PlanningSchoolBaseInfo.validate(extra_model.dict())
        except Exception as e:
            # 处理验证错误，例如返回错误信息或抛出自定义异常
            # error_messages = ", ".join([f"{k}: {v}" for k, v in e.errors()])
            print(e)
            raise PlanningSchoolValidateError()
        else:
            pass
            # return validated_data

        # res = await self.planning_school_rule.update_planning_school_status(planning_school_id,  PlanningSchoolStatus.NORMAL.value, 'open')
        # 请求工作流
        planning_school.id = planning_school_id
        res = await self.planning_school_rule.add_planning_school_work_flow(planning_school, extra_model)
        process_instance_id = 0
        if res and len(res) > 1 and 'process_instance_id' in res[0].keys() and res[0]['process_instance_id']:
            process_instance_id = res[0]['process_instance_id']
            pl = PlanningSchoolBaseInfoOptional(id=planning_school_id, process_instance_id=process_instance_id,
                                                workflow_status=AuditAction.NEEDAUDIT.value)

            res = await self.planning_school_rule.update_planning_school_byargs(pl)
            convert_snowid_in_model(res, extra_colums=['process_instance_id', ])

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        if is_add_log:
            res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
                action_target_id=str(planning_school_id),
                action_type=OperationType.MODIFY.value,
                # change_data=str(planning_school_id)[0:1000],
                change_data=JsonUtils.dict_to_json_str(planning_school_id),
                target=OperationTarget.PLANNING_SCHOOL.value,
                change_module=ChangeModule.CREATE_SCHOOL.value,
                change_detail="开办学校",
                process_instance_id=process_instance_id
            ))

        return res

    # 关闭    附件 和 原因的保存 到日志
    @require_role_permission("planning_school", "close")
    async def patch_close(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                min_length=1, max_length=20, example='SC2032633'),
                          action_reason: str = Query(None, description="原因", min_length=1, max_length=20,
                                                     example='家庭搬迁'),
                          related_license_upload: str = Query(None, description="相关证照上传", min_length=1,
                                                              max_length=60, example=''),

                          ):
        # 检测 是否允许修改
        is_draft = await self.planning_school_rule.is_can_not_add_workflow(planning_school_id)
        if is_draft:
            raise PlanningSchoolStatusError()
        # print(planning_school)
        # res = await self.planning_school_rule.update_planning_school_status(planning_school_id,
        #                                                                     PlanningSchoolStatus.CLOSED.value)
        # 请求工作流
        planning_school, extra_model = await self.planning_school_rule.get_planning_school_by_id(planning_school_id,
                                                                                                 PlanningSchoolBaseInfo, )

        res = await self.planning_school_rule.add_planning_school_close_work_flow(planning_school, extra_model,
                                                                                  action_reason, related_license_upload)
        process_instance_id = 0

        if res and len(res) > 1 and 'process_instance_id' in res[0].keys() and res[0]['process_instance_id']:
            process_instance_id = res[0]['process_instance_id']
            pl = PlanningSchoolBaseInfoOptional(id=planning_school_id, process_instance_id=process_instance_id,
                                                workflow_status=AuditAction.NEEDAUDIT.value)

            res = await self.planning_school_rule.update_planning_school_byargs(pl)

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_type=OperationType.MODIFY.value,
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CLOSE_SCHOOL.value,
            change_detail="关闭学校",
            action_target_id=str(planning_school_id),
            change_data=JsonUtils.dict_to_json_str(planning_school_id),
            process_instance_id=process_instance_id
        ))

        return res

    # 导入   任务队列的
    @require_role_permission("planning_school", "import")
    async def post_planning_school_import(self,
                                          file: PlanningSchoolImportReq

                                          ) -> Task:
        file_name = file.file_name
        print('入参', file)
        task_model = PlanningSchoolFileStorageModel(file_name=file_name, virtual_bucket_name=file.bucket_name,file_size='51363', scene= ImportScene.PLANNING_SCHOOL.value)
        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="school_task_planning_school_import",
            # 文件 要对应的 视图模型
            payload=task_model,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功', task)
        return task

    # 更新 全部信息 用于页面的 暂存 操作  不校验 数据的合法性     允许 部分 不填  现保存
    @require_role_permission("planning_school", "edit")
    async def put(self,

                  planning_school: PlanningSchoolBaseInfoOptional,
                  planning_school_communication: PlanningSchoolCommunications,
                  planning_school_eduinfo: PlanningSchoolEduInfo,
                  planning_school_id: int = Query(..., title="", description="学校id/园所id", example='38'),

                  ):
        # print(planning_school)
        planning_school.id = planning_school_id
        planning_school_communication.planning_school_id = planning_school_id
        planning_school_eduinfo.planning_school_id = planning_school_id
        planning_school_communication.id = None
        planning_school_eduinfo.id = None

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)
        log_con = compare_modify_fields(planning_school, origin)
        # 保存时 进到暂存状态 
        # planning_school.status = PlanningSchoolStatus.OPENING.value

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school,modify_status= False)
        res_com = await self.planning_school_communication_rule.update_planning_school_communication_byargs(
            planning_school_communication)
        res_edu = await self.planning_school_eduinfo_rule.update_planning_school_eduinfo_byargs(planning_school_eduinfo)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_type=OperationType.MODIFY.value,
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CREATE_SCHOOL.value,
            change_detail="暂存全部信息",
            action_target_id=str(planning_school_id),
            change_data=JsonUtils.dict_to_json_str(log_con),

        ))

        return res

    # 正式开办  传全部  插入或者更新
    @require_role_permission("planning_school", "open")
    async def put_open(self,

                       planning_school: PlanningSchoolBaseInfo,
                       planning_school_communication: PlanningSchoolCommunications,
                       planning_school_eduinfo: PlanningSchoolEduInfo,
                       planning_school_id: int | str = Query(..., title="", description="学校id/园所id", example='38'),

                       ):
        # print(planning_school)
        planning_school.id = planning_school_id
        planning_school_communication.planning_school_id = planning_school_id
        planning_school_eduinfo.planning_school_id = planning_school_id
        planning_school_communication.id = None
        planning_school_eduinfo.id = None
        # 直接开办同时 更新状态到开办中
        planning_school.status = PlanningSchoolStatus.OPENING.value

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)
        log_con = compare_modify_fields(planning_school, origin)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)
        res_com = await self.planning_school_communication_rule.update_planning_school_communication_byargs(
            planning_school_communication)
        res_edu = await self.planning_school_eduinfo_rule.update_planning_school_eduinfo_byargs(planning_school_eduinfo)

        #  调用 内部方法 开办

        res2 = await self.patch_open(str(planning_school_id), False)

        # 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_type=OperationType.MODIFY.value,
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CREATE_SCHOOL.value,
            change_detail="提交全部信息 开办",
            action_target_id=str(planning_school_id),
            change_data=JsonUtils.dict_to_json_str(log_con),

        ))

        return res2

    async def get_search(self,
                         planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),

                         page_request=Depends(PageRequest)):
        print(page_request, )
        items = []
        paging_result = await self.planning_school_rule.query_planning_schools(planning_school_name)
        return paging_result

    # 学校开设审核
    @require_role_permission("planning_school_open_audit", "pass")
    async def patch_open_audit(self,
                               audit_info: PlanningSchoolTransactionAudit
                               ):
        print('前端入参', audit_info)
        try:
            resultra = await self.planning_school_rule.req_workflow_audit(audit_info, 'open')
            if resultra is None:
                return {}
            if isinstance(resultra, str):
                return {resultra}
            return resultra
        except Exception as e:
            print(e)
            return {e}
        pass

    # 学校关闭审核
    @require_role_permission("planning_school_close_audit", "pass")
    async def patch_close_audit(self,
                                audit_info: PlanningSchoolTransactionAudit

                                ):
        resultra = await self.planning_school_rule.req_workflow_audit(audit_info, 'close')
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        return resultra
        pass

    # 学校关键信息变更审核
    @require_role_permission("planning_school_keyinfo_audit", "pass")
    async def patch_keyinfo_audit(self,
                                  audit_info: PlanningSchoolTransactionAudit

                                  ):
        resultra = await self.planning_school_rule.req_workflow_audit(audit_info, 'keyinfo_change')
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        return resultra
        pass

    # 规划校的开办关闭修改的 取消接口
    @require_role_permission("planning_school_open_audit", "cancel")
    async def patch_open_cancel(self,

                                process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                 example=25),
                                node_id: int = Query(0, title="流程对应的节点ID", description="",
                                                     example='22')

                                ):

        #  审批流取消
        res2 = await self.planning_school_rule.req_workflow_cancel(node_id, process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        return res2
        pass

    # 学校关闭
    @require_role_permission("planning_school_close_audit", "cancel")
    async def patch_close_cancel(self,
                                 process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                  example=25),
                                 node_id: int = Query(0, title="流程对应的节点ID", description="",
                                                      example='22')
                                 ):

        #  审批流取消
        res2 = await self.planning_school_rule.req_workflow_cancel(node_id, process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        return res2
        pass

    # 学校关键信息变更
    @require_role_permission("planning_school_keyinfo_audit", "cancel")
    async def patch_keyinfo_cancel(self,
                                   process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                    example=25),
                                   node_id: int = Query(0, title="流程对应的节点ID", description="",
                                                        example='22')
                                   ):
        #  审批流取消
        res2 = await self.planning_school_rule.req_workflow_cancel(node_id, process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        return res2
        pass

    # 原始的获取规划校分页接口 再用
    @require_role_permission("planning_school", "view")
    async def page(self,
                   # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                   request:Request,
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   planning_school_code: str = Query("", title="", description=" 园所标识码", ),
                   planning_school_level: str = Query("", title="", description=" 学校星级", ),
                   planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),
                   planning_school_no: str = Query("", title="学校编号", description="学校编号/园所代码", min_length=1,
                                                   max_length=20, ),
                   borough: str = Query("", title="  ", description=" 行政管辖区", ),
                   status: PlanningSchoolStatus = Query("", title="", description=" 状态", examples=['正常']),

                   founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                                         examples=['地方']),
                   founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                                       examples=['教育部门']),
                   founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                                       examples=['县级教育部门']),
                   page_request=Depends(PageRequest)):

        items = []
        obj= await get_extend_params(request)
        print(tenant_registry)
        # code =tenant_registry.get_tenant(request)
        # temp = get_tenant_by_code()


        paging_result = await self.planning_school_rule.query_planning_school_with_page(page_request,
                                                                                        planning_school_name,
                                                                                        planning_school_no,
                                                                                        planning_school_code,
                                                                                        block, planning_school_level,
                                                                                        borough, status, founder_type,
                                                                                        founder_type_lv2,
                                                                                        founder_type_lv3,obj
                                                                                        )
        return paging_result

    # 工作流申请详情
    async def get_planning_school_workflow_info(self,
                                                apply_id: int = Query(..., description="流程ID", example='1'),
                                                ):
        relationinfo = tinfo = ''
        # 转发去 工作流获取详细
        result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
            apply_id)
        if not result.get('json_data'):
            return {'工作流数据异常 无法解析'}

        json_data = JsonUtils.json_str_to_dict(result.get('json_data'))
        print(json_data)
        result = {**result, **json_data}

        if 'original_dict' in json_data.keys() and json_data['original_dict']:
            result = {**json_data['original_dict'], **result, **json_data}

        return result

    # 规划校导出
    async def post_planning_school_export(self,
                                          # students_query=Depends(NewStudentsQuery),
                                          page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                                          ) -> Task:
        print('入参接收', page_search)

        page_search = convert_query_to_none(page_search)
        print('入参接收2', page_search)

        task = Task(
            task_type="school_task_planning_school_export",
            payload=page_search,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task
