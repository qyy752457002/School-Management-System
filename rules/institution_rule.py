import hashlib
import json
import os
from datetime import datetime

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.storage.manager import storage_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from pydantic import BaseModel

from daos.institution_dao import InstitutionDAO
from models.institution import Institution
from models.student_transaction import AuditAction
from rules.common.common_rule import send_request
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config, map_keys
from views.models.institutions import Institutions as InstitutionModel, Institutions, InstitutionKeyInfo, \
    InstitutionOptional, InstitutionBaseInfo, InstitutionPageSearch
from views.models.planning_school import PlanningSchoolTransactionAudit, PlanningSchoolStatus
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, INSTITUTION_OPEN_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE
from views.models.school import School as SchoolModel, SchoolKeyAddInfo, SchoolKeyInfo
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus


@dataclass_inject
class InstitutionRule(SchoolRule):

    async def add_school_keyinfo_change_work_flow(self, school_flow: InstitutionKeyInfo,process_code=None,institution_info=None):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        if process_code:
            datadict['process_code'] = process_code
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['school_no'] = school_flow.school_no

        datadict['school_name'] = school_flow.school_name
        # datadict['school_edu_level'] =   school_flow.school_edu_level
        datadict['block'] =   school_flow.block
        datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        # datadict['school_category'] =   school_flow.school_category
        # datadict['school_operation_type'] =   school_flow.school_operation_type
        # datadict['school_org_type'] =   school_flow.school_org_type

        datadict['apply_user'] =  'tester'
        mapa = school_flow.__dict__
        mapa['institution_id'] = school_flow.id
        # 合并info
        mapa.update(institution_info.__dict__)
        mapa = map_keys(mapa, self.other_mapper)
        datadict['json_data'] =  json.dumps(mapa, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response


    # 向工作流中心发送申请
    async def add_school_work_flow(self, school_flow: InstitutionBaseInfo,):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        # datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        # datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        # datadict['block'] =   school_flow.block
        # datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no
        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['institution_id'] = school_flow.id
        dicta = map_keys(dicta, self.other_mapper)

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response


    async def add_school_close_work_flow(self, school_flow: InstitutionBaseInfo,action_reason,related_license_upload):
        # school_flow.id=0
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        # datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        # datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        # datadict['block'] =   school_flow.block
        # datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no

        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload
        dicta['institution_id'] = school_flow.id
        dicta = map_keys(dicta, self.other_mapper)

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'

        response= None
        try:
            response = await send_request(apiname,datadict,'post')
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def deal_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        school = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到事业单位信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
        if action=='close':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            # 拿到的是 实际模型的数下  和 需要校验的原始的 键不同   这里转为 原始的键 先
            json_data= map_keys(json_data, self.other_mapper)
            # obj = view_model_to_orm_model(json_data, InstitutionKeyInfo,other_mapper=self.other_mapper)

            planning_school_orm = InstitutionKeyInfo( **json_data)
            planning_school_orm.id= school.id

            res = await self.update_school_byargs(  planning_school_orm)
            pass

        # res = await self.update_school_status(school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass


    async def institution_export(self, task: Task):
        bucket = 'student'
        print(bucket,'桶')

        export_params: InstitutionPageSearch = (
            task.payload if task.payload is InstitutionPageSearch() else InstitutionPageSearch()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"institution_export{shortuuid.uuid()}.xlsx"
        temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)
        temp_file_path = os.path.join(temp_file_path, random_file_name)
        while True:
            # todo  这里的参数需要 解包
            paging = await self.school_dao.query_school_with_page(
                page_request, export_params.school_name,export_params.school_no,export_params.school_code,
                export_params.block,export_params.school_level,export_params.borough,export_params.status,export_params.founder_type,
                export_params.founder_type_lv2,
                export_params.founder_type_lv3 ,export_params.planning_school_id,export_params.province,export_params.city,export_params.institution_category,
            )
            paging_result = PaginatedResponse.from_paging(
                paging, InstitutionPageSearch, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            for item in paging_result.items:
                item.approval_status =  item.approval_status.value

            # logger.info('分页的结果',len(paging_result.items))
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", paging_result.items)
            excel_writer.set_data(temp_file_path)
            excel_writer.execute()
            # break
            if len(paging.items) < page_request.per_page:
                break
            page_request.page += 1
        #     保存文件时可能报错
        print('临时文件路径',temp_file_path)
        file_storage =  storage_manager.put_file_to_object(
            bucket, f"{random_file_name}.xlsx", temp_file_path
        )
        # 这里会写入 task result 提示 缺乏 result file id  导致报错
        try:

            file_storage_resp = await storage_manager.add_file(
                self.file_storage_dao, file_storage
            )
            print('file_storage_resp ',file_storage_resp)

            task_result = TaskResult()
            task_result.task_id = task.task_id
            task_result.result_file = file_storage_resp.file_name
            task_result.result_bucket = file_storage_resp.virtual_bucket_name
            task_result.result_file_id = file_storage_resp.file_id
            task_result.last_updated = datetime.now()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id =  0
            print('拼接数据task_result ',task_result)

            resadd = await self.task_dao.add_task_result(task_result)
            print('task_result写入结果',resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result