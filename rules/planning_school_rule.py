import json

from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select
from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.planning_school_dao import PlanningSchoolDAO
from models.planning_school import PlanningSchool
from models.student_transaction import AuditAction
from rules import enum_value_rule
from rules.common.common_rule import send_request
from rules.enum_value_rule import EnumValueRule
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus, \
    PlanningSchoolKeyInfo, PlanningSchoolTransactionAudit, PlanningSchoolBaseInfoOptional
from views.models.planning_school import PlanningSchoolBaseInfo
from mini_framework.databases.conn_managers.db_manager import db_connection_manager

from views.models.system import STUDENT_TRANSFER_WORKFLOW_CODE, PLANNING_SCHOOL_OPEN_WORKFLOW_CODE, \
    PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE, PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE


@dataclass_inject
class PlanningSchoolRule(object):
    planning_school_dao: PlanningSchoolDAO
    system_rule: SystemRule

    async def get_planning_school_by_id(self, planning_school_id,extra_model=None):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not planning_school_db:
            raise PlanningSchoolNotFoundError()
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel)
        if extra_model:
            planning_school_extra = orm_model_to_view_model(planning_school_db, extra_model,
                                                       exclude=[""])
            return planning_school,planning_school_extra

        else:
            return planning_school

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school_name)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def add_planning_school(self, planning_school: PlanningSchoolModel):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school.planning_school_name)
        if exists_planning_school:
            raise Exception(f"规划校{planning_school.planning_school_name}已存在")
        planning_school_db = view_model_to_orm_model(planning_school, PlanningSchool,    exclude=["id"])
        planning_school_db.status =  PlanningSchoolStatus.DRAFT.value
        planning_school_db.created_uid = 0
        planning_school_db.updated_uid = 0
        if planning_school.province and len( planning_school.province)>0:
            pass
        else:
            planning_school.province = "210000"
        if planning_school.city and len( planning_school.city)>0:
            pass
        else:
            planning_school.city = "210100"

        planning_school_db = await self.planning_school_dao.add_planning_school(planning_school_db)
        print('id 111',planning_school_db.id)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=["created_at",'updated_at'])
        return planning_school

    async def delete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.delete_planning_school(exists_planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school

    async def softdelete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.softdelete_planning_school(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db

    async def get_all_planning_schools(self):
        return await self.planning_school_dao.get_all_planning_schools()

    async def get_planning_school_count(self):
        return await self.planning_school_dao.get_planning_school_count()

    async def query_planning_school_with_page(self, page_request: PageRequest,  planning_school_name,planning_school_no,planning_school_code,
                                              block,planning_school_level,borough,status ,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ):
        # todo 根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res= await enum_value_rule.get_next_level_enum_values('founder_type'  ,founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)


            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if len(founder_type_lv2)>0:
            founder_type_lv3_res= await enum_value_rule.get_next_level_enum_values('founder_type_lv2'  ,founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.planning_school_dao.query_planning_school_with_page(  page_request, planning_school_name,planning_school_no,planning_school_code,
                                                                                  block,planning_school_level,borough,status,founder_type,
                                                                                  founder_type_lv2,
                                                                                  founder_type_lv3 )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolModel)
        return paging_result


    async def update_planning_school_status(self, planning_school_id, target_status,action=None):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        # 判断原来的状态+要更改的状态 进行后续的更新
        if target_status== PlanningSchoolStatus.NORMAL.value and exists_planning_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办 自动创建一条学校信息
            exists_planning_school.status= PlanningSchoolStatus.NORMAL.value
        elif target_status== PlanningSchoolStatus.CLOSED.value and exists_planning_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_planning_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_planning_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"规划校当前状态不支持您的操作{exists_planning_school.status}")

        need_update_list = []
        need_update_list.append('status')

        print(exists_planning_school.status,2222222)
        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(exists_planning_school,*need_update_list)
        if action=='open':
            school_rule = get_injector(SchoolRule)

            await school_rule.add_school_from_planning_school(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db

    async def update_planning_school_byargs(self, planning_school,ctype=1):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()

        if exists_planning_school.status== PlanningSchoolStatus.DRAFT.value:
            planning_school.status= PlanningSchoolStatus.OPENING.value
            planning_school.status= PlanningSchoolStatus.OPENING.value
        else:
            pass
        need_update_list = []
        for key, value in planning_school.__dict__.items():
            if key.startswith('_'):
                continue
            if value:
                need_update_list.append(key)


        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(planning_school, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        return planning_school_db


    async def query_planning_schools(self,planning_school_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(PlanningSchool).where(PlanningSchool.planning_school_name.like(f'%{planning_school_name}%') ))
        res= result.scalars().all()
        print(res)
        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, PlanningSchoolModel)
            lst.append(planning_school)
        return lst


    # 向工作流中心发送申请
    async def add_planning_school_work_flow(self, planning_school_flow: PlanningSchoolModel,planning_school_baseinfo: PlanningSchoolBaseInfo):
        # planning_school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] =   planning_school_flow.founder_type_lv3
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['apply_user'] =  'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
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
        # 节点实例id todo  自动获取
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


    async def add_planning_school_close_work_flow(self, planning_school_flow: PlanningSchoolModel,planning_school_baseinfo: PlanningSchoolBaseInfo,action_reason,related_license_upload):
        # planning_school_flow.id=0
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] =   planning_school_flow.founder_type_lv3
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['apply_user'] =  'tester'
        dicta = planning_school_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload

        dicta['planning_school_id'] = planning_school_flow.id


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

        datadict = audit_info.__dict__
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
            res2 = await self.deal_planning_school(audit_info.process_instance_id, action)
        # 终态的处理

        await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)


        return response
        pass

    async def deal_planning_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        planning_school = await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if not planning_school:
            print('未查到规划信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_planning_school_status(planning_school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
        if action=='close':
            res = await self.update_planning_school_status(planning_school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # 读取流程的原始信息  更新到数据库

            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass


            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            needdel= []
            # planning_school_op = PlanningSchoolBaseInfoOptional()
            #
            # for key,value in json_data.items():
            #     if not hasattr(planning_school_op,key):
            #         needdel.append(key)
            # for key in needdel:
            #     json_data.pop(key)

            planning_school_orm = PlanningSchoolKeyInfo(**json_data)
            planning_school_orm.id= planning_school.id

            res = await self.update_planning_school_byargs(  planning_school_orm)
            pass

        # res = await self.update_planning_school_status(planning_school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass

    async def set_transaction_end(self,process_instance_id,status):
        tinfo=await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status=status.value
            await self.update_planning_school_byargs(tinfo)


        pass

    async def add_planning_school_keyinfo_change_work_flow(self, planning_school_flow: PlanningSchoolKeyInfo,):
        # planning_school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_no'] = planning_school_flow.planning_school_no

        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['planning_school_edu_level'] =   planning_school_flow.planning_school_edu_level
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['planning_school_category'] =   planning_school_flow.planning_school_category
        datadict['planning_school_operation_type'] =   planning_school_flow.planning_school_operation_type
        datadict['planning_school_org_type'] =   planning_school_flow.planning_school_org_type

        datadict['apply_user'] =  'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
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