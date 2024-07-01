from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.json import JsonUtils
from mini_framework.web.views import BaseView

from business_exceptions.institution import InstitutionStatusError
from models.student_transaction import AuditAction
from rules.operation_record import OperationRecordRule
from rules.system_rule import SystemRule
from views.common.common_view import compare_modify_fields
from views.models.operation_record import OperationTarget, OperationType, ChangeModule, OperationRecord
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo, PlanningSchoolTransactionAudit, \
    PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.school import School, SchoolKeyInfo, SchoolPageSearch
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.institutions import Institutions, InstitutionTask, InstitutionOptional, InstitutionKeyInfo, \
    InstitutionPageSearch
from rules.institution_rule import InstitutionRule
from mini_framework.web.request_context import request_context_manager

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
# 当前工具包里支持get  patch前缀的 方法的自定义使用
class InstitutionView(BaseView):
    def __init__(self):
        super().__init__()
        self.institution_rule = get_injector(InstitutionRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.system_rule = get_injector(SystemRule)



    async def page(self,
                   page_request= Depends(PageRequest),
                   # planning_institution_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),
                  # planning_institution_name:str= Query(None, description="学校名称" ,min_length=1,max_length=20,example='XX小学'),




                  ):
        print(page_request)
        items=[]
        res = await self.institution_rule.query_institution_with_page(page_request,)
        return res

    async def post_institution_import_example(self, account: Institutions = Body(..., description="")) -> Task:
        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个键
            task_type="institution_import",
            # 文件 要对应的 视图模型
            payload=account,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 导入 事业单位      上传文件获取 桶底值

    async def post_institution_import(self,
                                      filename: str = Query(..., description="文件名"),
                                      bucket: str = Query(..., description="文件名"),
                                      scene: str = Query('', description="文件名"),
                                      ) -> Task:

        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="institution_import",
            # 文件 要对应的 视图模型
            payload=InstitutionTask(file_name=filename, bucket=bucket, scene=scene),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 开办
    async def patch_open(self, institution_id: str = Query(..., title="学校编号", description="学校id/园所id", min_length=1,
                                                      max_length=20, example='SC2032633')):
        # print(school)
        # res = await self.institution_rule.update_institution_status(institution_id, PlanningSchoolStatus.NORMAL.value, 'open')
        # 检测 是否允许修改
        is_draft = await self.institution_rule.is_can_not_add_workflow(institution_id)
        if is_draft:
            raise InstitutionStatusError()

        # 请求工作流
        school = await self.institution_rule.get_institution_by_id(institution_id,)

        res = await self.institution_rule.add_institution_work_flow(school)
        process_instance_id=0
        if len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionOptional(id=institution_id, process_instance_id=process_instance_id)

            res = await self.institution_rule.update_institution_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="开办分校",
            action_target_id=str(institution_id),
            # change_data=str(institution_id)[0:1000],
            process_instance_id=process_instance_id

        ))

        return res

    # 关闭
    async def patch_close(self, institution_id: str = Query(..., title="学校编号", description="学校id/园所id", min_length=1,
                                                       max_length=20, example='SC2032633'),
                          action_reason: str = Query(None, description="原因", min_length=1, max_length=20,
                                                     example='家庭搬迁'),
                          related_license_upload: str = Query(None, description="相关证照上传", min_length=1,
                                                                    max_length=60, example=''),
                          ):
        # res = await self.institution_rule.update_institution_status(institution_id, PlanningSchoolStatus.CLOSED.value)
        # 检测 是否允许修改
        is_draft = await self.institution_rule.is_can_not_add_workflow(institution_id)
        if is_draft:
            raise InstitutionStatusError()
        # 请求工作流

        school = await self.institution_rule.get_institution_by_id(institution_id,)

        res = await self.institution_rule.add_institution_close_work_flow(school, action_reason,related_license_upload)
        process_instance_id=0

        if res and  len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionOptional(id=institution_id, process_instance_id=process_instance_id,workflow_status= AuditAction.NEEDAUDIT.value)

            res = await self.institution_rule.update_institution_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="关闭分校",
            action_target_id=str(institution_id),
            # change_data=str(institution_id)[0:1000],
            process_instance_id=process_instance_id

        ))

        return res


    # # 修改 关键信息
    async def put_keyinfo(self,
                          school: InstitutionKeyInfo,

                          ):
        # 检测 是否允许修改
        is_draft = await self.institution_rule.is_can_not_add_workflow(school.id)
        if is_draft:
            raise InstitutionStatusError()
        origin = await self.institution_rule.get_institution_by_id(school.id)

        res2 = compare_modify_fields(school, origin)
        # print(  res2)

        # res = await self.planning_institution_rule.update_planning_institution_byargs(planning_school)
        #  工作流
        # planning_school.id = planning_institution_id
        res = await self.institution_rule.add_institution_keyinfo_change_work_flow(school,)
        process_instance_id=0
        if res and  len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionOptional(id=school.id, process_instance_id=process_instance_id,workflow_status= AuditAction.NEEDAUDIT.value)

            res = await self.institution_rule.update_institution_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="修改关键信息",
            action_target_id=str(school.id),
            change_data= JsonUtils.dict_to_json_str(res2),
            process_instance_id=process_instance_id
        ))

        return res
        # return  {institution_no,borough,block }

    # 学校开设审核
    async def patch_open_audit(self,
                               audit_info: PlanningSchoolTransactionAudit

                               ):
        print('前端入参',audit_info)
        resultra = await self.institution_rule.req_workflow_audit(audit_info,'open')
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        # print(new_students_key_info)
        return resultra
        pass
    # 学校关闭审核
    async def patch_close_audit(self,
                                audit_info: PlanningSchoolTransactionAudit

                                ):
        print('前端入参',audit_info)
        resultra = await self.institution_rule.req_workflow_audit(audit_info,'close')
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        # print(new_students_key_info)
        return resultra
        pass
    # 学校关键信息变更审核
    async def patch_keyinfo_audit(self,
                                  audit_info: PlanningSchoolTransactionAudit

                                  ):
        print('前端入参',audit_info)
        resultra = await self.institution_rule.req_workflow_audit(audit_info,'keyinfo_change')
        if resultra is None:
            return {}
        if isinstance(resultra, str):
            return {resultra}

        # print(new_students_key_info)
        return resultra
        pass

    async def patch_open_cancel(self,

                                process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                 example= 25),
                                node_id: int  = Query(0, title="流程对应的节点ID", description="",
                                                      example='22')

                                ):

        #  审批流取消
        res2 = await self.institution_rule.req_workflow_cancel(node_id,process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        # print(new_students_key_info)
        return res2
        pass
        # 学校关闭
    async def patch_close_cancel(self,
                                 process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                  example= 25),
                                 node_id: int  = Query(0, title="流程对应的节点ID", description="",
                                                       example='22')
                                 ):

        #  审批流取消
        res2 = await self.institution_rule.req_workflow_cancel(node_id,process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        # print(new_students_key_info)
        return res2
        pass
        # 学校关键信息变更
    async def patch_keyinfo_cancel(self,
                                   process_instance_id: int = Query(0, title="流程ID", description="流程ID",
                                                                    example= 25),
                                   node_id: int  = Query(0, title="流程对应的节点ID", description="",
                                                         example='22')
                                   ):
        #  审批流取消
        res2 = await self.institution_rule.req_workflow_cancel(node_id,process_instance_id)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        # print(new_students_key_info)
        return res2
        pass

    # 分校的审批流列表
    async def page_institution_audit(self,
                                block: str = Query("", title=" ", description="地域管辖区", ),
                                institution_code: str = Query("", title="", description=" 园所标识码", ),
                                institution_level: str = Query("", title="", description=" 学校星级", ),
                                borough: str = Query("", title="  ", description=" 行政管辖区", ),
                                status: PlanningSchoolStatus = Query(None, title="", description=" 状态", examples=['正常']),

                                founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                                                      examples=['地方']),
                                founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                                                    examples=['教育部门']),
                                founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                                                    examples=['县级教育部门']),

                                institution_no: str|None = Query(None, title="学校编号", description="学校编号",
                                                            example='SC2032633'),
                                institution_name: str = Query(None, description="学校名称",
                                                         example='XX小学'),
                                planning_institution_id: int = Query(None, description="规划校ID", example='1'),
                                province: str = Query("", title="", description="省份代码", ),
                                city: str = Query("", title="", description="城市", ),

                                # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                                process_code: str = Query("", title="流程代码", description="例如p_institution_open", ),
                                planning_institution_code: str = Query("", title="", description=" 园所标识码", ),
                                page_request=Depends(PageRequest)):
        items = []
        #PlanningSchoolBaseInfoOptional
        print('入参接收',page_request,status)
        req= InstitutionPageSearch(block=block,
                              planning_institution_code=planning_institution_code,
                              borough=borough,
                              status=status,
                              founder_type=founder_type,
                              founder_type_lv2=founder_type_lv2,
                              founder_type_lv3=founder_type_lv3,
                              institution_no=institution_no,
                              institution_name=institution_name,
                              planning_institution_id=planning_institution_id,
                              province=province,
                              city=city,
                              institution_code=institution_code,
                              institution_level=institution_level,


                              )
        print('入参接收2',req)
        paging_result = await self.system_rule.query_workflow_with_page(req,page_request,'',process_code,  )
        print('333',page_request)
        return paging_result

    #工作流申请详情
    async def get_institution_workflow_info(self,

                                       apply_id: int = Query(..., description="流程ID", example='1'),

                                       ):
        relationinfo = tinfo = ''
        # 转发去 工作流获取详细
        result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
            apply_id)
        if not result.get('json_data'):
            return {'工作流数据异常 无法解析'}

        json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
        # 移到顶层
        result={ **result,**json_data}

        if 'original_dict' in json_data.keys() and  json_data['original_dict']:
            result={**json_data['original_dict'],**result}


        return result
