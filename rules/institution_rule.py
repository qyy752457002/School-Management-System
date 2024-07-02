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
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config
from views.models.institutions import Institutions as InstitutionModel, Institutions, InstitutionKeyInfo, \
    InstitutionOptional
from views.models.planning_school import PlanningSchoolTransactionAudit, PlanningSchoolStatus
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, INSTITUTION_OPEN_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE


@dataclass_inject
class InstitutionRule(object):
    institution_dao: InstitutionDAO
    system_rule: SystemRule


    async def get_institution_by_id(self, institution_id,extra_model=None):
        institution_db = await self.institution_dao.get_institution_by_id(institution_id)
        if not institution_db:
            return None
        if extra_model:
            institution = orm_model_to_view_model(institution_db, extra_model)
        else:
            institution = orm_model_to_view_model(institution_db, InstitutionOptional)

        return institution

    async def add_institution(self, institution: InstitutionModel):
        # exists_institution = await self.institution_dao.get_institution_by_id(
        #     institution.id)
        # if exists_institution:
        #     raise Exception(f"行政事业单位{institution.institution_name}已存在")


        institution_db = Institution()
        institution_db = view_model_to_orm_model(institution, Institution,    exclude=["id"])
        generator = SnowflakeIdGenerator(1, 1)
        id = generator.generate_id()
        institution_db.id = id

        institution_db.updated_at = datetime.now()
        institution_db.created_at = datetime.now()

        institution_db = await self.institution_dao.add_institution(institution_db)
        print(institution_db,'插入suc')
        institution = orm_model_to_view_model(institution_db, InstitutionOptional, exclude=[""])
        return institution

    async def update_institution(self, institution,ctype=1):
        exists_institution = await self.institution_dao.get_institution_by_id(institution.id)
        if not exists_institution:
            raise Exception(f"行政事业单位{institution.id}不存在")
        if ctype==1:
            institution_db = Institution()
            institution_db.id = institution.id
            institution_db.institution_no = institution.institution_no
            institution_db.institution_name = institution.institution_name
            institution_db.block = institution.block
            institution_db.borough = institution.borough
            institution_db.institution_type = institution.institution_type
            institution_db.institution_operation_type = institution.institution_operation_type
            institution_db.institution_operation_type_lv2 = institution.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3 = institution.institution_operation_type_lv3
            institution_db.institution_org_type = institution.institution_org_type
            institution_db.institution_level = institution.institution_level
        else:
            institution_db = Institution()
            institution_db.id = institution.id
            institution_db.institution_name=institution.institution_name
            institution_db.institution_short_name=institution.institution_short_name
            institution_db.institution_code=institution.institution_code
            institution_db.create_institution_date=institution.create_institution_date
            institution_db.founder_type=institution.founder_type
            institution_db.founder_name=institution.founder_name
            institution_db.urban_rural_nature=institution.urban_rural_nature
            institution_db.institution_operation_type=institution.institution_operation_type
            institution_db.institution_org_form=institution.institution_org_form
            institution_db.institution_operation_type_lv2=institution.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3=institution.institution_operation_type_lv3
            institution_db.department_unit_number=institution.department_unit_number
            institution_db.sy_zones=institution.sy_zones
            institution_db.historical_evolution=institution.historical_evolution


        institution_db = await self.institution_dao.update_institution(institution_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # institution = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""])
        return institution_db

    async def softdelete_institution(self, institution_id):
        exists_institution = await self.institution_dao.get_institution_by_id(institution_id)
        if not exists_institution:
            raise Exception(f"行政事业单位{institution_id}不存在")
        institution_db = await self.institution_dao.softdelete_institution(exists_institution)
        # institution = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""],)
        return institution_db


    async def get_institution_count(self):
        return await self.institution_dao.get_institution_count()

    async def query_institution_with_page(self, page_request: PageRequest, institution_name=None,
                                              institution_id=None,institution_no=None,institution_category=None, institution_org_type=None,block=None,borough=None,social_credit_code=None,  ):
        paging = await self.institution_dao.query_institution_with_page(institution_name, institution_id,institution_no,
                                                                                page_request,institution_category,institution_org_type,block,borough,social_credit_code)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, InstitutionOptional, {"create_institution_date": "create_date","website_url": "website_url",})
        return paging_result

    # 向工作流中心发送申请
    async def add_institution_work_flow(self, institution_flow: Institutions,):
        # institution_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= institution_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['institution_code'] = institution_flow.institution_code
        datadict['institution_name'] = institution_flow.institution_name
        datadict['social_credit_code'] =   institution_flow.social_credit_code
        # datadict['block'] =   institution_flow.block
        # datadict['borough'] =   institution_flow.borough
        # datadict['institution_level'] =   institution_flow.institution_level
        # datadict['institution_no'] =   institution_flow.institution_no
        datadict['apply_user'] =  'tester'
        dicta = institution_flow.__dict__
        dicta['institution_id'] = institution_flow.id

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)

        # datadict['json_data'] =  json.dumps(institution_flow.__dict__, ensure_ascii=False)
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


    async def add_institution_close_work_flow(self, institution_flow: Institutions,action_reason,related_license_upload):
        # institution_flow.id=0
        data= institution_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['institution_code'] = institution_flow.institution_code
        datadict['institution_name'] = institution_flow.institution_name
        # datadict['founder_type_lv3'] =   institution_flow.founder_type_lv3
        # datadict['block'] =   institution_flow.block
        # datadict['borough'] =   institution_flow.borough
        # datadict['institution_level'] =   institution_flow.institution_level
        # datadict['institution_no'] =   institution_flow.institution_no

        datadict['apply_user'] =  'tester'
        dicta = institution_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload
        dicta['institution_id'] = institution_flow.id

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'

        response= None
        try:
            response = await send_request(apiname,datadict,'post')
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def req_workflow_audit(self,audit_info:PlanningSchoolTransactionAudit,action):

        # 发起审批流的 处理

        datadict = dict()
        if audit_info.process_instance_id>0:
            node_id=await self.system_rule.get_work_flow_current_node_by_process_instance_id(  audit_info.process_instance_id)
            audit_info.node_id=node_id['node_instance_id']


        # 节点实例id
        datadict['node_instance_id'] =  audit_info.node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # from urllib.parse import urlencode
        # apiname += ('?' + urlencode(datadict))
        # 如果是query 需要拼接参数

        # 字典参数
        datadict ={"user_id":"11","action":"approved",**datadict}
        if audit_info.transaction_audit_action== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if audit_info.transaction_audit_action== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await send_request(apiname,datadict,'post',True)
        print(response,'接口响应')
        if audit_info.transaction_audit_action== AuditAction.PASS.value:
            # 成功则写入数据
            # transrule = get_injector(StudentTransactionRule)
            # await transrule.deal_student_transaction(student_edu_info)
            res2 = await self.deal_school(audit_info.process_instance_id, action)
        # 终态的处理

        await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)



        return response
        pass

    async def deal_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        school = await self.institution_dao.get_institution_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到规划信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_institution_status(school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
        if action=='close':
            res = await self.update_institution_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # res = await self.update_institution_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            planning_institution_orm = InstitutionKeyInfo(**json_data)
            planning_institution_orm.id= school.id

            res = await self.update_institution_byargs(  planning_institution_orm)
            pass

        # res = await self.update_institution_status(institution_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass

    async def add_institution_keyinfo_change_work_flow(self, institution_flow: InstitutionKeyInfo,):
        # institution_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= institution_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        # datadict['institution_no'] = institution_flow.institution_no

        datadict['institution_name'] = institution_flow.institution_name
        # datadict['institution_edu_level'] =   institution_flow.institution_edu_level
        # datadict['block'] =   institution_flow.block
        # datadict['borough'] =   institution_flow.borough
        # datadict['institution_level'] =   institution_flow.institution_level
        # datadict['institution_category'] =   institution_flow.institution_category
        # datadict['institution_operation_type'] =   institution_flow.institution_operation_type
        # datadict['institution_org_type'] =   institution_flow.institution_org_type

        datadict['apply_user'] =  'tester'
        mapa = institution_flow.__dict__
        mapa['institution_id'] = institution_flow.id
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

    async def req_workflow_cancel(self,node_id,process_instance_id=None):

        # 发起审批流的 处理
        datadict = dict()
        # 节点实例id    自动获取
        if process_instance_id>0:
            node_id=await self.system_rule.get_work_flow_current_node_by_process_instance_id(  process_instance_id)
            node_id=node_id['node_instance_id']

        datadict['node_instance_id'] =  node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # 字典参数
        # datadict ={"user_id":"11","action":"revoke"}
        datadict ={"user_id":"11","action":"revoke",**datadict}

        response= await send_request(apiname,datadict,'post',True)

        print(response,'接口响应')
        # 终态的处理

        await self.set_transaction_end(process_instance_id, AuditAction.CANCEL)


        return response
        pass


    async def set_transaction_end(self,process_instance_id,status):
        tinfo=await self.institution_dao.get_institution_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status=status.value
            await self.update_institution_byargs(tinfo)


        pass
    async def is_can_not_add_workflow(self, student_id,is_all_status_allow=False):
        tinfo=await self.get_institution_by_id(student_id)
        # 是否需要拦截
        if not is_all_status_allow:
            if tinfo and  tinfo.status == PlanningSchoolStatus.DRAFT.value:
                return True

        # 检查是否有占用
        if tinfo and  tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
            return True
        return False


    async def update_institution_status(self, institution_id, status,action=None):
        exists_school = await self.institution_dao.get_institution_by_id(institution_id)
        if not exists_school:
            raise Exception(f"事业行政单位{institution_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_school.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"事业行政单位当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_school.status,2222222)
        institution_db = await self.institution_dao.update_institution_byargs(exists_school,*need_update_list)


        # institution_db = await self.institution_dao.update_institution_status(exists_school,status)
        # school = orm_model_to_view_model(institution_db, SchoolModel, exclude=[""],)
        return institution_db


    async def update_institution_byargs(self, school,):
        exists_school = await self.institution_dao.get_institution_by_id(school.id)
        if not exists_school:
            raise Exception(f"事业行政单位{school.id}不存在")
        if exists_school.status== PlanningSchoolStatus.DRAFT.value:
            exists_school.status= PlanningSchoolStatus.OPENING.value
            school.status= PlanningSchoolStatus.OPENING.value
        else:
            pass

        if isinstance(school, BaseModel):

            school= view_model_to_orm_model(school, Institution,  other_mapper={"website_url": 'website_url',"create_date":'create_institution_date'})
        need_update_list = []
        for key, value in school.__dict__.items():
            if key.startswith('_'):
                continue
            if value:
                need_update_list.append(key)


        institution_db = await self.institution_dao.update_institution_byargs(school, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(institution_db, SchoolModel, exclude=[""])
        return institution_db