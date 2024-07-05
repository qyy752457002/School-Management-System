from typing import List

from fastapi.params import Body
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.json import JsonUtils
from mini_framework.web.toolkit.model_utilities import view_model_to_orm_model
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.institution import InstitutionStatusError, InstitutionNotFoundError
from models.student_transaction import AuditAction
from rules.operation_record import OperationRecordRule
from rules.school_communication_rule import SchoolCommunicationRule
from rules.school_eduinfo_rule import SchoolEduinfoRule
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import compare_modify_fields, get_extend_params
from views.models.operation_record import OperationTarget, OperationType, ChangeModule, OperationRecord
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo, PlanningSchoolTransactionAudit, \
    PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.school import School, SchoolKeyInfo, SchoolPageSearch, SchoolBaseInfo
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.institutions import Institutions, InstitutionTask, InstitutionOptional, InstitutionKeyInfo, \
    InstitutionPageSearch, InstitutionsAdd, InstitutionBaseInfo, InstitutionsWorkflowInfo, InstitutionCommunications
from rules.institution_rule import InstitutionRule
from mini_framework.web.request_context import request_context_manager

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task

from views.models.school_communications import SchoolCommunications
from views.models.school_eduinfo import SchoolEduInfo
from views.models.system import InstitutionType, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, \
    INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class InstitutionView(BaseView):
    def __init__(self):
        super().__init__()
        self.institution_rule = get_injector(InstitutionRule)
        self.school_rule = get_injector(SchoolRule)
        self.school_eduinfo_rule = get_injector(SchoolEduinfoRule)
        self.school_communication_rule = get_injector(SchoolCommunicationRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.system_rule = get_injector(SystemRule)


    async def get(self,
                  institution_id: int = Query(..., description="|", example='1'),
                  ):
        school = await self.institution_rule.get_school_by_id(institution_id,extra_model=InstitutionOptional)
        institution_keyinfo = await self.institution_rule.get_school_by_id(institution_id, extra_model=InstitutionKeyInfo)

        school_eduinfo={}
        school_communication = await self.school_communication_rule.get_school_communication_by_school_id(institution_id)
        # todo 异常可能导致orm转换时 的链接释放
        try:

            school_eduinfo = await self.school_eduinfo_rule.get_school_eduinfo_by_school_id(institution_id)
        except Exception as e:
            print(e)
        return {'institution': school,     'institution_keyinfo': institution_keyinfo,'institution_communication': school_communication, 'institution_eduinfo': school_eduinfo,}

    async def post(self, school: InstitutionsAdd):
        # res = await self.institution_rule.add_institution(school)
        print('school',school)
        res = await self.institution_rule.add_school(school)
        print(res)
        resc = SchoolCommunications(id=0)
        # logging.debug(resc,'模型2', res.id, type( res.id ))
        newid = str(res.id)
        print(resc, '模型23', res.id, type(res.id))
        # str( res.id).copy()

        resc.school_id = int(newid)
        print(resc, newid, '||||||||')

        # 保存通信信息
        res_comm = await self.school_communication_rule.add_school_communication(resc,
                                                                                 convertmodel=False)
        print(res_comm, '模型2 res')
        #
        resedu = SchoolEduInfo(id=0)
        resedu.school_id = res.id
        # 保存教育信息
        res_edu = await self.school_eduinfo_rule.add_school_eduinfo(resedu, convertmodel=False)
        print(res_edu)

        return res
        # return  school

    # # 修改 关键信息 留给页面的 '变更按钮'
    async def put_keyinfo(self,
                          school: InstitutionKeyInfo,

                          ):
        print('入参',school)
        # 检测 是否允许修改
        is_draft = await self.institution_rule.is_can_not_add_workflow(school.id,True)
        if is_draft:
            raise InstitutionStatusError()
        origin = await self.institution_rule.get_school_by_id(school.id,extra_model=InstitutionKeyInfo)

        res2 = compare_modify_fields(school, origin)
        # print(  res2)

        # res = await self.planning_institution_rule.update_planning_institution_byargs(planning_school)
        #  工作流
        # planning_school.id = planning_institution_id
        res = await self.institution_rule.add_school_keyinfo_change_work_flow(school,INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE)
        process_instance_id=0
        if res and  len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionsWorkflowInfo(id=school.id, process_instance_id=process_instance_id,workflow_status= AuditAction.NEEDAUDIT.value)

            resu = await self.institution_rule.update_school_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.INSTITUTION.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="修改关键信息",
            action_target_id=str(school.id),
            change_data= JsonUtils.dict_to_json_str(res2),
            process_instance_id=process_instance_id
        ))

        return res

    # 删除
    async def delete(self,
                     institution_id: int = Query(..., description="|", example='1'),
                     ):
        # print(school_id)
        res = await self.institution_rule.softdelete_school(institution_id)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.INSTITUTION.value,
            action_type=OperationType.DELETE.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="删除",

            action_target_id=str(institution_id),

            change_data= JsonUtils.dict_to_json_str({'institution_id':institution_id}),


        ))

        return res

    # 修改 变更 基本信息
    async def patch_baseinfo(self,
                             institution_baseinfo: InstitutionBaseInfo,
                             institution_communication: InstitutionCommunications,

                             ):
        # 学校转ins
        origin = await self.institution_rule.get_school_by_id(institution_baseinfo.id,extra_model=InstitutionBaseInfo)

        if not  origin:
            raise InstitutionNotFoundError()

        if origin.status == PlanningSchoolStatus.DRAFT.value:
            institution_baseinfo.status = PlanningSchoolStatus.OPENING.value
            # raise InstitutionStatusError(f"{origin.institution_name}状态为正常，不能修改")
        log_con = compare_modify_fields(institution_baseinfo, origin)
        # todo 完成转换 v2m ins 转学校
        # school_db = view_model_to_orm_model(institution_baseinfo, School,    exclude=["id"])    #这里已经是school开头的字段 应该可以直接转


        res = await self.institution_rule.update_school_byargs(institution_baseinfo, )
        institution_communication.school_id = institution_baseinfo.id

        res_com = await self.school_communication_rule.update_school_communication_byargs(institution_communication, )

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.INSTITUTION.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(institution_baseinfo.id),

            change_data= JsonUtils.dict_to_json_str(log_con),

        ))

        return res


    async def page(self,
                   page_request= Depends(PageRequest),
                   institution_category: InstitutionType = Query(None, title='单位分类',examples=['institution/administration']),
                   social_credit_code: str = Query( '',title='统一社会信用代码',description=" 统一社会信用代码",examples=['DK156512656']),
                   institution_name: str = Query(None, description="机构名称", example='XX小学'),
                   institution_org_type: str = Query('', title="", description=" 学校办别",examples=['民办']),
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   borough: str = Query("", title="  ", description=" 行政管辖区", ),
                   # status: PlanningSchoolStatus = Query("", title="", description=" 状态", examples=['正常']),
                   ):
        print(page_request)
        items=[]
        if not institution_category:
            institution_category = [InstitutionType.INSTITUTION,InstitutionType.ADMINISTRATION]
        res = await self.institution_rule.query_school_with_page(page_request,institution_category=institution_category,school_name=institution_name,school_org_type=institution_org_type,block=block,borough=borough,social_credit_code=social_credit_code,extra_model=InstitutionBaseInfo)
        return res


    # 开办
    async def patch_open(self, institution_id: str = Query(..., title="", description="", min_length=1,
                                                      max_length=20, example='12')):
        # print(school)
        # res = await self.institution_rule.update_institution_status(institution_id, PlanningSchoolStatus.NORMAL.value, 'open')
        # 检测 是否允许修改
        is_draft = await self.institution_rule.is_can_not_add_workflow(institution_id)
        if is_draft:
            raise InstitutionStatusError()

        # 请求工作流
        school = await self.institution_rule.get_school_by_id(institution_id,)

        res = await self.institution_rule.add_school_work_flow(school)
        process_instance_id=0
        if res and  len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionOptional(id=institution_id, process_instance_id=process_instance_id,workflow_status=AuditAction.NEEDAUDIT.value)

            res_u = await self.institution_rule.update_school_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.INSTITUTION.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="开办事业行政单位",
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

        school = await self.institution_rule.get_school_by_id(institution_id,)

        res = await self.institution_rule.add_school_close_work_flow(school, action_reason,related_license_upload)
        process_instance_id=0

        if res and  len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']
            pl = InstitutionOptional(id=institution_id, process_instance_id=process_instance_id,workflow_status= AuditAction.NEEDAUDIT.value)

            resu = await self.institution_rule.update_school_byargs(pl  )

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.INSTITUTION.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="关闭行政事业单位",
            action_target_id=str(institution_id),
            # change_data=str(institution_id)[0:1000],
            process_instance_id=process_instance_id

        ))

        return res


        # return  {institution_no,borough,block }
    # 这里没有 put全部 开办和全部关闭 和 搜索
    # 学校搜索 模糊搜索 TODO 增加 区域ID  学校ID 支持多个传入
    async def get_search(self,
                         request: Request  ,
                         institution_category: InstitutionType = Query(None, title='单位分类',examples=['institution/administration']),


                         school_name: str = Query("", title="名称", description="1-20字符", ),
                         school_id: str = Query("", title="多个逗号分割", description="", ),
                         block: str = Query("", title="地域管辖区", description="", ),
                         borough: str = Query("", title="行政管辖区", description="", ),

                         page_request=Depends(PageRequest),

                         ):
        items = []
        if not institution_category:
            institution_category = [InstitutionType.INSTITUTION,InstitutionType.ADMINISTRATION]
        # 学校 区 只能看自己的范围内的数据
        paging_result = await self.institution_rule.query_schools(school_name,await get_extend_params(request),school_id,block,borough,institution_category=institution_category,extra_model=InstitutionBaseInfo)
        return paging_result

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

    # 导入 事业单位      上传文件获取 桶底值

    async def post_institution_import(self,
                                      file_name: str = Body(..., description="文件名"),
                                      # bucket: str = Query(..., description="文件名"),
                                      # scene: str = Query('', description="文件名"),
                                      ) -> Task:

        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="institution_import",
            # 文件 要对应的 视图模型
            payload=InstitutionTask(file_name=file_name, bucket='', scene='institution_import'),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task
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
    # 分校的审批流列表
    async def page_institution_audit(self,
                                     social_credit_code: str = Query( '',title='统一社会信用代码',description=" 统一社会信用代码",examples=['DK156512656']),
                                     institution_name: str = Query(None, description="机构名称", example='XX小学'),
                                     institution_org_type: str = Query('', title="", description=" 学校办别",examples=['民办']),
                                     block: str = Query("", title=" ", description="地域管辖区", ),
                                     borough: str = Query("", title="  ", description=" 行政管辖区", ),
                                     process_code: str = Query("", title="流程代码", description="例如p_institution_open", ),
                                     page_request=Depends(PageRequest)):
        items = []
        #PlanningSchoolBaseInfoOptional
        print('入参接收',page_request,)
        req= InstitutionPageSearch(block=block,
                                   borough=borough,
                                   institution_name=institution_name,
                                   social_credit_code=social_credit_code,
                                   institution_org_type=institution_org_type,
                                   founder_type_lv3=[]
                                   )
        print('入参接收2',req)
        paging_result = await self.system_rule.query_workflow_with_page(req,page_request,'',process_code,  )
        print('333',page_request)
        return paging_result
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
