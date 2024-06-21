from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_transaction_dao import TeacherTransactionDAO
from daos.teachers_dao import TeachersDao
from models.teacher_transaction import TeacherTransaction
from views.models.teacher_transaction import TeacherTransactionModel, TeacherTransactionUpdateModel, \
    TeacherTransactionQueryModel, TeacherTransactionApproval, TeacherTransactionGetModel
from business_exceptions.teacher import TeacherNotFoundError, TeacherExistsError
from business_exceptions.teacher_transction import TransactionApprovalError
from rules.work_flow_instance_rule import WorkFlowNodeInstanceRule
from mini_framework.utils.http import HTTPRequest
from urllib.parse import urlencode
from views.common.common_view import workflow_service_config


@dataclass_inject
class TeacherWorkFlowRule(object):

    async def add_teacher_work_flow(self, parameters: dict):
        """
        parameters = {"process_code": process_code, "teacher_id": teacher_id, "applicant_name": applicant_name}
        """
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance-initiate'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(parameters))
        result = await httpreq.post_json(url, parameters, headerdict)
        work_flow_instance = result[0]
        next_node_instance = result[1]
        return work_flow_instance, next_node_instance

    async def process_transaction_work_flow(self, node_instance_id: int, parameters: dict):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"node_instance_id": node_instance_id}
        data = parameters
        # data = {"parameters": parameters}
        api_name = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        next_node_instance = await httpreq.post_json(url, data, headerdict)
        print(next_node_instance)
        return next_node_instance

    async def get_teacher_work_flow_log_by(self, process_instance_id):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/work-flow-node-log'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.get_json(url, headerdict)
        return result

    async def get_teacher_work_flow_current_node(self, process_instance_id):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/current-node-by-process-instance-id'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.get_json(url, headerdict)
        return result
