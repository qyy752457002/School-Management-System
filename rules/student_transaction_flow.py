# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import json
from urllib.parse import urlencode

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
from views.models.student_transaction import StudentTransactionFlow as StudentTransactionFlowModel, StudentEduInfo
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
    async def add_student_transaction_work_flow(self, student_transaction_flow: StudentEduInfo,stuinfo: StudentsKeyinfoDetail):
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
        datadict['jason_data'] =  json.dumps(student_transaction_flow.__dict__, ensure_ascii=False)
        # datadict['workflow_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
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
    async def exe_student_transaction(self,student_transaction:StudentEduInfo, student_transaction_flow: StudentTransactionFlowModel):
        # 如果存在出 读取出的信息
        student_transaction_out=None
        if student_transaction.relation_id:
            stu_rule= get_injector(StudentTransactionRule)
            student_transaction_out = await stu_rule.get_student_transaction_by_id(student_transaction.relation_id)

        # todo  分布式  A校修改学生 出  B校修改学生入
        transfer_data =            student_transaction.__dict__


        # todo 3个业务接口的地址的定义  和业务流程编码 有关
        # print(222222222222,student_transaction,student_transaction_out,)
        flow_data=[
            TransactionNode(transaction_name='a校转入',prepare_url='/api/school/v1/public/current-student/student-transaction-prepare',precommit_url='/api/school/v1/public/current-student/student-transaction-precommit',commit_url='/api/school/v1/public/current-student/student-transaction-commit',
            rollback_url='/api/school/v1/public/current-student/student-transaction-rollback',
                            transaction_code= student_transaction.school_id),

            TransactionNode(transaction_name='b校转出',
                            prepare_url='/api/school/v1/public/current-student/student-transaction-prepare',precommit_url='/api/school/v1/public/current-student/student-transaction-precommit',commit_url='/api/school/v1/public/current-student/student-transaction-commit',
                            rollback_url='/api/school/v1/public/current-student/student-transaction-rollback',
                            transaction_code= student_transaction_out.school_id),


        ]

        res_trans= await DistributedTransactionCore().execute_transaction(111,transfer_data,flow_data)
        if res_trans:
            print('事务执行成功')
            # 处理  更新数据

            res_flow = await self.req_workflow_ultra(student_transaction,student_transaction_flow)
            return True
        return False
    async def req_workflow_ultra(self,student_transaction,student_transaction_flow):

        # 读取 节点ID
        trans_flow =await self.query_student_transaction_flow(student_transaction_flow.apply_id,stage='apply_submit')
        json_object = json.loads(trans_flow[0].description)



        # 发起审批流的 处理
        student_transaction_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= student_transaction_flow
        datadict = dict()
        # datadict['process_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        # 节点实例id
        datadict['node_instance_id'] =  json_object[1]['node_instance_id']

        # datadict['workflow_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        url+=  ('?' +urlencode(datadict))

        print('参数', url, datadict,headerdict)
        # 字典参数
        datadict ={"user_id":"11","action":"approved"}
        if student_transaction.status== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if student_transaction.status== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await httpreq.post_json(url,datadict,headerdict)
        print(response,'接口响应')
        pass

    async def req_workflow_cancel(self,student_transaction,student_transaction_flow):

        # 读取 节点ID
        trans_flow =await self.query_student_transaction_flow(student_transaction_flow.apply_id,stage='apply_submit')
        json_object = json.loads(trans_flow[0].description)

        # 发起审批流的 处理
        student_transaction_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= student_transaction_flow
        datadict = dict()
        # datadict['process_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        # 节点实例id
        datadict['node_instance_id'] =  json_object[1]['node_instance_id']

        # datadict['workflow_code'] = STUDENT_TRANSFER_WORKFLOW_CODE
        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        url+=  ('?' +urlencode(datadict))

        print('参数', url, datadict,headerdict)
        # 字典参数
        datadict ={"user_id":"11","action":"approved"}
        if student_transaction.status== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if student_transaction.status== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await httpreq.post_json(url,datadict,headerdict)
        print(response,'接口响应')
        pass
