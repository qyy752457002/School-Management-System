import hashlib
import json
from datetime import datetime

import shortuuid
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
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
    InstitutionOptional, InstitutionBaseInfo
from views.models.planning_school import PlanningSchoolTransactionAudit, PlanningSchoolStatus
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, INSTITUTION_OPEN_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE
from views.models.school import School as SchoolModel, SchoolKeyAddInfo, SchoolKeyInfo
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus


@dataclass_inject
class InstitutionRule(SchoolRule):

    async def add_school_keyinfo_change_work_flow(self, school_flow: InstitutionKeyInfo,process_code=None):
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
            print('未查到规划信息',process_instance_id)
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