import copy
import json
import os
from datetime import datetime, date

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from rules.common.common_rule import send_request, send_orgcenter_request
from rules.school_rule import SchoolRule
from rules.tenant_rule import TenantRule
from views.common.common_view import workflow_service_config, map_keys, convert_dates_to_strings
from views.models.institutions import InstitutionKeyInfo, \
    InstitutionBaseInfo, InstitutionPageSearch
from views.models.organization import Organization
from views.models.planning_school import PlanningSchoolStatus
from views.models.school import SchoolBaseInfoOptional
from views.models.system import INSTITUTION_OPEN_WORKFLOW_CODE, INSTITUTION_CLOSE_WORKFLOW_CODE, \
    SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, InstitutionType


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

        datadict['apply_user'] =  'tester'
        mapa = school_flow.__dict__
        mapb = institution_info.__dict__
        mapa['institution_id'] = school_flow.id
        # 合并info
        mapb.update(mapa)
        mapb = map_keys(mapb, self.other_mapper)
        datadict['json_data'] =  json.dumps(mapb, ensure_ascii=False)
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

    async def deal_school(self,process_instance_id,action, ):
        #  读取流程实例ID
        school = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到事业单位信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
            try:
                # 单位发送过去
                res_unit, data_unit = await self.send_school_to_org_center(school)
                # 单位的组织 对接
                # res_unit = await self.send_unit_orgnization_to_org_center(school)
                res_oigna = await self.send_unit_orgnization_to_org_center(school, data_unit)

                # 添加组织结构 部门
                org = Organization(org_name=school.school_name,
                                   school_id=school.id,
                                   org_type='校',
                                   parent_id=0,
                                   org_code=school.school_no,
                                   org_code_type='school',
                                   )
                # 部门对接
                res_org, data_org = await self.send_org_to_org_center(org, res_unit)
                # 管理员 对接
                res_admin = await self.send_admin_to_org_center(school,data_org)
                # 添加 用户和组织关系 就是部门
                await self.send_user_org_relation_to_org_center(school, res_unit, data_org, res_admin)
                #     todo 自懂获取秘钥
                tenant_rule = get_injector(TenantRule)
                print('开始 获取租户信息-单位')
                await tenant_rule.sync_tenant_all(school.id)
            except Exception as e:
                print('异常', e)
                raise e
            # await self.send_school_to_org_center(school)
            # await self.send_admin_to_org_center(school)
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
        bucket = 'school'
        print(bucket,'桶')

        export_params: InstitutionPageSearch = (
            task.payload if task.payload is InstitutionPageSearch() else InstitutionPageSearch()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"institution_export{shortuuid.uuid()}.xlsx"
        # 获取当前脚本所在目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取当前脚本所在目录的父目录
        parent_dir = os.path.dirname(script_dir)

        # 构建与 script_dir 并列的 temp 目录的路径
        temp_dir_path = os.path.join(parent_dir, 'temp')

        # 确保 temp 目录存在，如果不存在则创建它
        os.makedirs(temp_dir_path, exist_ok=True)
        temp_file_path = os.path.join(temp_dir_path, random_file_name)
        while True:
            # todo  这里的参数需要 解包
            paging = await self.school_dao.query_school_with_page(
                page_request, export_params.school_name,export_params.school_no,export_params.school_code,
                export_params.block,export_params.school_level,export_params.borough,export_params.status,export_params.founder_type,
                export_params.founder_type_lv2,
                export_params.founder_type_lv3 ,export_params.planning_school_id,export_params.province,export_params.city,export_params.institution_category,
            )
            paging_result = PaginatedResponse.from_paging(
                paging, SchoolBaseInfoOptional, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            await self.convert_school_to_export_format(paging_result)
            logger.info('分页的结果条数',len(paging_result.items))
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
            task_result.result_id = shortuuid.uuid()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id =  0
            print('拼接数据task_result ',task_result)

            resadd = await self.task_dao.add_task_result(task_result,True)
            print('task_result写入结果',resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result
