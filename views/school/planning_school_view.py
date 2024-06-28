import logging
from datetime import datetime
from typing import List

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from business_exceptions.planning_school import PlanningSchoolValidateError, PlanningSchoolBaseInfoValidateError
from rules.operation_record import OperationRecordRule
from rules.system_rule import SystemRule
from views.common.common_view import compare_modify_fields, get_extend_params, get_client_ip
from views.models.operation_record import OperationRecord, ChangeModule, OperationType, OperationType, OperationTarget
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo, PlanningSchoolKeyInfo, \
    PlanningSchoolStatus, PlanningSchoolFounderType, PlanningSchoolPageSearch, PlanningSchoolKeyAddInfo, \
    PlanningSchoolBaseInfoOptional, PlanningSchoolTask
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from models.grade import Grade
from rules.planning_school_rule import PlanningSchoolRule
from views.models.grades import Grades
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule

from rules.planning_school_eduinfo_rule import PlanningSchoolEduinfoRule
from views.models.system import PLANNING_SCHOOL_OPEN_WORKFLOW_CODE


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class CustomValidationError:
    pass


class PlanningSchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        self.planning_school_eduinfo_rule = get_injector(PlanningSchoolEduinfoRule)
        self.operation_record_rule = get_injector(OperationRecordRule)
        self.system_rule = get_injector(SystemRule)

    #   包含3部分信息 1.基本信息 2.通讯信息 3.教育信息
    async def get(self,

                  planning_school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
                                                        max_length=20, example='SC2032633'),
                  planning_school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                                                    example='XX小学'),
                  planning_school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),

                  ):

        planning_school, extra_model = await self.planning_school_rule.get_planning_school_by_id(planning_school_id,
                                                                                                 PlanningSchoolKeyInfo)
        planning_school_communication = await self.planning_school_communication_rule.get_planning_school_communication_by_planning_shcool_id(
            planning_school_id)
        planning_school_eduinfo = await self.planning_school_eduinfo_rule.get_planning_school_eduinfo_by_planning_school_id(
            planning_school_id)

        return {'planning_school': planning_school, 'planning_school_communication': planning_school_communication,
                'planning_school_eduinfo': planning_school_eduinfo, 'planning_school_keyinfo': extra_model}

    async def post(self, planning_school: PlanningSchoolKeyAddInfo,
                   request: Request  ,

                   ):
        # obj= await get_extend_params(request)

        # print(planning_school)
        # 保存 模型
        res = await self.planning_school_rule.add_planning_school(planning_school)
        resc = PlanningSchoolCommunications(id=0)
        # logging.debug(resc,'模型2', res.id, type( res.id ))
        newid = str(res.id)
        print(resc, '模型23', res.id, type(res.id))
        # str( res.id).copy()

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
    async def put_keyinfo(self,
                          planning_school: PlanningSchoolKeyInfo,
                          request: Request,
                          # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                          ):

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)

        res2 = compare_modify_fields(planning_school, origin)
        # print(  res2)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(planning_school.id),
            target=OperationTarget.PLANNING_SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.KEY_INFO_CHANGE.value,
            change_detail="修改基本信息",
            change_data=str(res2)[0:1000],
        ))

        return res

    # 删除
    async def delete(self, planning_school_id: int = Query(..., title="", description="学校id/园所id",
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
            change_data=str(res)[0:1000],  ))

        return res

    # 修改 变更 基本信息
    async def patch_baseinfo(self, planning_school_baseinfo: PlanningSchoolBaseInfo, ):

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school_baseinfo.id)
        log_con = compare_modify_fields(planning_school_baseinfo, origin)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school_baseinfo, 2)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            target=OperationTarget.PLANNING_SCHOOL.value,
            action_type=OperationType.MODIFY.value,
            change_module=ChangeModule.BASIC_INFO_CHANGE.value,
            change_detail="修改基本信息",
            action_target_id=str(planning_school_baseinfo.id),
            change_data=str(log_con)[0:1000],
              ))

        return res

    async def page(self,
                   # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   planning_school_code: str = Query("", title="", description=" 园所标识码", ),
                   planning_school_level: str = Query("", title="", description=" 学校星级", ),
                   planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),
                   planning_school_no: str = Query("", title="学校编号", description="学校编号/园所代码", min_length=1,
                                                   max_length=20, ),
                   borough: str = Query("", title="  ", description=" 行政管辖区", ),
                   status: PlanningSchoolStatus = Query(None, title="", description=" 状态", examples=['正常']),

                   founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                                         examples=['地方']),
                   founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                                       examples=['教育部门']),
                   founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                                       examples=['县级教育部门']),

                   page_request=Depends(PageRequest)):
        print(page_request, )
        items = []
        #PlanningSchoolBaseInfoOptional
        req= PlanningSchoolPageSearch(block=block,
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
        print('入参接收',req)
        paging_result = await self.system_rule.query_workflow_with_page(req,page_request,'',PLANNING_SCHOOL_OPEN_WORKFLOW_CODE,  )
        print('333',page_request)
        return paging_result


    # 开办   校验合法性等  业务逻辑   开班式 校验所有的数据是否 都填写了
    async def patch_open(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                               min_length=1, max_length=20, example='SC2032633')):
        # print(planning_school)
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
        res = await self.planning_school_rule.add_planning_school_work_flow(planning_school, extra_model)
        process_instance_id=0
        if len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']

            pass


        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(planning_school_id),
            action_type=OperationType.MODIFY.value,
            change_data=str(planning_school_id)[0:1000],
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CREATE_SCHOOL.value,
            change_detail="开办学校",
            process_instance_id=process_instance_id
        ))

        return res

    # 关闭  todo  附件 和 原因的保存 到日志 
    async def patch_close(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                min_length=1, max_length=20, example='SC2032633'),
                          action_reason: str = Query(None, description="原因", min_length=1, max_length=20,
                                                     example='家庭搬迁'),
                          related_license_upload: List[str] = Query(None, description="相关证照上传", min_length=1,
                                                                    max_length=60, example=''),

                          ):
        # print(planning_school)
        # res = await self.planning_school_rule.update_planning_school_status(planning_school_id,
        #                                                                     PlanningSchoolStatus.CLOSED.value)
        # 请求工作流
        planning_school, extra_model = await self.planning_school_rule.get_planning_school_by_id(planning_school_id,
                                                                                                 PlanningSchoolBaseInfo,)

        res = await self.planning_school_rule.add_planning_school_close_work_flow(planning_school, extra_model,action_reason,related_license_upload)
        process_instance_id=0
        if len(res)>1 and 'process_instance_id' in res[0].keys() and  res[0]['process_instance_id']:
            process_instance_id= res[0]['process_instance_id']

            pass

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_type=OperationType.MODIFY.value,
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CLOSE_SCHOOL.value,
            change_detail="关闭学校",
            action_target_id=str(planning_school_id),
            change_data=str(planning_school_id)[0:1000],
           ))

        return res

    # 导入   任务队列的
    async def post_planning_school_import(self,
                                      filename: str = Query(..., description="文件名"),
                                      bucket: str = Query(..., description="文件名"),
                                      scene: str = Query('', description="文件名"),
                                      ) -> Task:
        task = Task(
            # 需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="planning_school_import",
            # 文件 要对应的 视图模型
            payload=PlanningSchoolTask(file_name=filename, bucket=bucket, scene=scene),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    # 更新 全部信息 用于页面的 暂存 操作  不校验 数据的合法性     允许 部分 不填  现保存
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
        # if isinstance(planning_school_eduinfo.att_class_type,  bool):
        #     planning_school_eduinfo.att_class_type= str( planning_school_eduinfo.att_class_type )

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)
        log_con = compare_modify_fields(planning_school, origin)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)
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
            change_data=str(log_con)[0:1000],
           ))

        return res

    # 正式开办  传全部  插入或者更新
    async def put_open(self,

                       planning_school: PlanningSchoolBaseInfo,
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
        # if isinstance(planning_school_eduinfo.att_class_type,  bool):
        #     planning_school_eduinfo.att_class_type= str( planning_school_eduinfo.att_class_type )

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)
        log_con = compare_modify_fields(planning_school, origin)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)
        res_com = await self.planning_school_communication_rule.update_planning_school_communication_byargs(
            planning_school_communication)
        res_edu = await self.planning_school_eduinfo_rule.update_planning_school_eduinfo_byargs(planning_school_eduinfo)

        #  调用 内部方法 开办

        res2 = await self.patch_open(str(planning_school_id))

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_type=OperationType.MODIFY.value,
            target=OperationTarget.PLANNING_SCHOOL.value,
            change_module=ChangeModule.CREATE_SCHOOL.value,
            change_detail="提交全部信息 开办",
            action_target_id=str(planning_school_id),
            change_data=str(log_con)[0:1000],
        ))

        return res2

    async def get_search(self,
                         planning_school_name: str = Query("", title="学校名称", description="1-20字符", ),

                         page_request=Depends(PageRequest)):
        print(page_request, )
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.planning_school_rule.query_planning_schools(planning_school_name)
        return paging_result
    # 学校开设审核
    async def patch_open_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                               min_length=1, max_length=20, example='SC2032633')):
        pass
    # 学校关闭审核
    async def patch_close_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                     min_length=1, max_length=20, example='SC2032633')):
        pass
    # 学校关键信息变更审核
    async def patch_keyinfo_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                      min_length=1, max_length=20, example='SC2032633')):
        pass
    # 规划校的开办关闭修改的 取消接口
    async def patch_open_cancel(self, node_id: str = Query(..., title="流程对应的节点ID", description="",
                                                                     min_length=1, max_length=20, example='SC2032633')):

        #  审批流取消
        res2 = await self.planning_school_rule.req_workflow_cancel(node_id,)

        if res2 is None:
            return {}
        if isinstance(res2, str):
            return {res2}

        # print(new_students_key_info)
        return res2
        pass
    # 学校关闭
    async def patch_close_cancel(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                      min_length=1, max_length=20, example='SC2032633')):
        pass
    # 学校关键信息变更
    async def patch_keyinfo_cancel(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                        min_length=1, max_length=20, example='SC2032633')):
        pass


    async def page_planning_school_biz(self,
                   # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
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
        print(page_request, )
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.planning_school_rule.query_planning_school_with_page(page_request,
                                                                                        planning_school_name,
                                                                                        planning_school_no,
                                                                                        planning_school_code,
                                                                                        block, planning_school_level,
                                                                                        borough, status, founder_type,
                                                                                        founder_type_lv2,
                                                                                        founder_type_lv3

                                                                                        )
        return paging_result
