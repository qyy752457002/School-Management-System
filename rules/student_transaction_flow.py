# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import json
from urllib.parse import urlencode

from fastapi.params import Query
from mini_framework.utils.json import JsonUtils

# from fastapi import Query

from distribute_transaction_lib.transaction import TransactionNode

from distribute_transaction_lib import DistributedTransactionCore
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from daos.student_transaction_flow_dao import StudentTransactionFlowDAO
from models.student_transaction import AuditAction
from models.student_transaction_flow import StudentTransactionFlow
from rules.student_transaction import StudentTransactionRule
from rules.students_rule import StudentsRule
from views.common.common_view import workflow_service_config
from views.models.student_transaction import StudentTransactionFlow as StudentTransactionFlowModel, StudentEduInfo, \
    StudentTransactionAudit, StudentTransaction
from views.models.students import StudentsKeyinfoDetail
from views.models.system import STUDENT_TRANSFER_WORKFLOW_CODE


@dataclass_inject
class StudentTransactionFlowRule(object):
    student_transaction_flow_dao: StudentTransactionFlowDAO

    async def get_student_transaction_flow_by_id(self, student_transaction_flow_id):
        student_transaction_flow_db = await self.student_transaction_flow_dao.get_studenttransactionflow_by_id(
            student_transaction_flow_id)
        # 可选 , exclude=[""]
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel)
        return student_transaction_flow

    async def get_student_transaction_flow_by_student_transaction_flow_name(self, student_transaction_flow_name):
        student_transaction_flow_db = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_studenttransaction_flow_name(
            student_transaction_flow_name)
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel,
                                                           exclude=[""])
        return student_transaction_flow

    async def add_student_transaction_flow(self, student_transaction_flow: StudentTransactionFlowModel):

        # 定义 视图和model的映射关系
        original_dict_map_view_orm = {
            # "transfer_in_type": "out_type",
            "natural_edu_no": "country_no",
            "grade_name": "in_grade",
            "classes": "in_class",
            "transferin_time": "in_date",
            "transferin_reason": "reason",
            "school_id": "in_school_id",

        }

        student_transaction_flow_db = view_model_to_orm_model(student_transaction_flow, StudentTransactionFlow,
                                                              exclude=["id"])

        student_transaction_flow_db = await self.student_transaction_flow_dao.add_studenttransactionflow(
            student_transaction_flow_db)

        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}

        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel,
                                                           exclude=[""], other_mapper=flipped_dict)
        return student_transaction_flow

    async def update_student_transaction_flow(self, student_transaction_flow):
        exists_student_transaction_flow = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_id(
            student_transaction_flow.id)
        if not exists_student_transaction_flow:
            raise Exception(f"转学申请{student_transaction_flow.id}不存在")

        need_update_list = []
        for key, value in student_transaction_flow.dict().items():
            if value:
                need_update_list.append(key)

        student_transaction_flow_db = await self.student_transaction_flow_dao.update_studenttransaction_flow(
            student_transaction_flow, *need_update_list)
        # student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionModel, exclude=[""])
        return student_transaction_flow_db

    async def delete_student_transaction_flow(self, student_transaction_flow_id):
        exists_student_transaction_flow = await self.student_transaction_flow_dao.get_studenttransaction_flow_by_id(
            student_transaction_flow_id)
        if not exists_student_transaction_flow:
            raise Exception(f"转学申请{student_transaction_flow_id}不存在")
        student_transaction_flow_db = await self.student_transaction_flow_dao.delete_student_transaction_flow(
            exists_student_transaction_flow)
        student_transaction_flow = orm_model_to_view_model(student_transaction_flow_db, StudentTransactionFlowModel,
                                                           exclude=[""])
        return student_transaction_flow

    async def get_all_student_transaction_flows(self):
        return await self.student_transaction_flow_dao.get_all_student_transaction_flows()

    async def get_student_transaction_flow_count(self):
        return await self.student_transaction_flow_dao.get_studenttransaction_flow_count()

    async def query_student_transaction_flow_with_page(self, page_request: PageRequest,
                                                       student_transaction_flow_name=None,
                                                       school_id=None, ):
        paging = await self.student_transaction_flow_dao.query_studenttransaction_flow_with_page(
            student_transaction_flow_name,
            school_id, page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, StudentTransactionFlowModel)
        return paging_result

    async def query_student_transaction_flowbiz(self, apply_id,stage=None):

        session = await db_connection_manager.get_async_session("default", True)
        query = select(StudentTransactionFlow).where(StudentTransactionFlow.apply_id == apply_id  )
        if stage:
            query= query.where(StudentTransactionFlow.stage == stage)
        result = await session.execute(query)
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, StudentTransactionFlowModel)

            lst.append(planning_school)
        return lst

    async def query_student_transaction_flow(self, apply_id,stage=None):
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        datadict=dict()
        datadict['process_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        datadict['process_instance_id'] = apply_id
        # datadict['per_page'] =  page_request.per_page

        apiname = '/api/school/v1/teacher-workflow/work-flow-node-log'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.get_json(url,headerdict)
            # print(response)
        except Exception as e:
            print(e)
        return response

    # 向工作流中心发送申请
    async def add_student_transaction_work_flow(self, student_transaction_flow: StudentEduInfo,stuinfo: StudentsKeyinfoDetail,stuinfoadd,stubaseinfo):
        student_transaction_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= student_transaction_flow
        datadict =  data.__dict__
        datadict['process_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['student_name'] = stuinfo.student_name
        datadict['student_gender'] = stuinfo.student_gender
        datadict['edu_number'] =   student_transaction_flow.edu_number
        datadict['school_name'] =   student_transaction_flow.school_name
        datadict['apply_user'] =  'tester'
        datadict['student_info'] =  stuinfoadd.__dict__
        datadict['student_base_info'] =  stubaseinfo.__dict__
        dicta = student_transaction_flow.__dict__
        # 检查字典  如果哪个值为query 则设为none birthday registration_date enrollment_date
        for key, value in dicta.items():
            if isinstance(value,Query) or isinstance(value,tuple):
                dicta[key] = None
        print('999', dicta)
        # jsonutils.print_dict(datadict)
        datadict= {**datadict,**dicta}
        print('总字典', datadict)

        # datadict['jason_data'] =  json.dumps(dicta, ensure_ascii=False)
        datadict['jason_data'] =  JsonUtils.dict_to_json_str(datadict)
        # datadict['workflow_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
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
            print(response)
        except Exception as e:
            print(e)
        return response

    # 处理流程审批 的 操作
    async def exe_student_transaction(self,audit_info):
        # 如果存在出 读取出的信息
            # 处理  更新数据

        res_flow = await self.req_workflow_ultra(audit_info)
        return res_flow
    async def req_workflow_ultra(self,audit_info:StudentTransactionAudit,):

        # 发起审批流的 处理
        # student_transaction_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        # data= student_transaction_flow
        datadict = dict()
        # datadict['process_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        # 节点实例id
        datadict['node_instance_id'] =  audit_info.transferin_audit_id

        # datadict['workflow_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        url+=  ('?' +urlencode(datadict))

        print('参数', url, datadict,headerdict)
        # 字典参数
        datadict ={"user_id":"11","action":"approved"}
        if audit_info.transferin_audit_action== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if audit_info.transferin_audit_action== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await httpreq.post_json(url,datadict,headerdict)
        print(response,'接口响应')
        if audit_info.transferin_audit_action== AuditAction.PASS.value:
            # 成功则写入数据
            transrule = get_injector(StudentTransactionRule)
            # await transrule.deal_student_transaction(student_edu_info)

            student_transaciton = StudentTransaction(id=audit_info.transferin_audit_id,
                                                     status=audit_info.transferin_audit_action.value,process_instance_id=audit_info.process_instance_id, )
            if student_transaciton.process_instance_id>0:

                res2 = await transrule.deal_student_transaction(student_transaciton)
            else:
                print('请传流程ID前段或者工作流返回它必须 ')

            pass


        return response
        pass

    async def req_workflow_cancel(self,transferin_id,):

        # 发起审批流的 处理
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        datadict = dict()
        # 节点实例id
        datadict['node_instance_id'] =  transferin_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url = url + apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        url += ('?' + urlencode(datadict))

        print('参数', url, datadict, headerdict)
        # 字典参数
        datadict ={"user_id":"11","action":"revoke"}

        response = await httpreq.post_json(url,datadict,headerdict)
        print(response,'接口响应')
        return response
        pass
