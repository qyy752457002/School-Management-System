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
from pydantic import BaseModel, Field
from views.models.work_flow import WorkFlowInstanceCreateModel, WorkFlowInstanceModel, WorkFlowInstanceQueryModel, \
    WorkFlowInstanceQueryReModel
from mini_framework.utils.json import JsonUtils
from mini_framework.databases.queries.pages import Paging

from views.models.teachers import TeachersCreatModel
from typing import Type


@dataclass_inject
class TeacherWorkFlowRule(object):

    async def add_teacher_work_flow(self, model: Type[BaseModel], params: dict):
        """
        parameters = {"process_code": process_code,"applicant_name": applicant_name}
        """
        work_instance_instance = await self.create_workflow_from_model(model, params)
        parameters = work_instance_instance.dict()
        params_data = JsonUtils.dict_to_json_str(parameters)
        print(parameters)
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        # url += ('?' + urlencode(parameters))

        result = await httpreq.post(url, params_data, headerdict)
        result = JsonUtils.json_str_to_dict(result)

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
        next_node_instance = await httpreq.post(url, data, headerdict)
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

    async def delete_teacher_save_work_flow_instance(self, teacher_id: int):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"teacher_id": teacher_id}
        api_name = '/api/school/v1/teacher-workflow/teacher-save-work-flow-instance'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.delete(url, headerdict)
        return result

    async def query_work_flow_instance_with_page(self, page_request: PageRequest, query_model: Type[BaseModel],
                                                 query_re_model: Type[BaseModel], params: dict):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        query_model_instance = await self.create_work_flow_query_model_from_model(query_model, params)
        parameters = query_model_instance.dict()
        parameters["page"] = page_request.page
        parameters["per_page"] = page_request.per_page
        query_parmas = {k: v for k, v in parameters.items() if v is not None}
        params_data = JsonUtils.dict_to_json_str(parameters)
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(query_parmas))
        result = await httpreq.get(url, headerdict)
        result = JsonUtils.json_str_to_dict(result)
        page_result = PaginatedResponse(**result)
        print(f'结果是{page_result}')
        print(type(page_result))
        page_response = await self.create_page_response_from_workflow(query_re_model, page_result)
        return page_response

    async def create_workflow_from_model(self, base_model: Type[BaseModel],
                                         params: dict) -> WorkFlowInstanceCreateModel:
        base_model = base_model.dict()
        workflow_fields = WorkFlowInstanceCreateModel.__fields__.keys()
        workflow_data = {}
        json_data = {}
        for field, value in params.items():
            if field in workflow_fields:
                workflow_data[field] = value
        for field, value in base_model.items():
            if field in workflow_fields:
                workflow_data[field] = value
            else:
                json_data[field] = value
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceCreateModel(**workflow_data)
        return work_flow_instance

    async def create_model_from_workflow(self, work_flow_instance: WorkFlowInstanceModel, model: Type[BaseModel]):
        work_flow_instance_dic = work_flow_instance.dict()
        model_fields = model.__fields__.keys()
        model_data = {}
        for field in model_fields:
            if field in work_flow_instance_dic.keys():
                model_data[field] = work_flow_instance[field]
            elif "json_data" in work_flow_instance_dic and field in work_flow_instance_dic["json_data"]:
                model_data[field] = work_flow_instance_dic["json_data"][field]
        model_instance = model(**model_data)
        return model_instance

    async def create_work_flow_query_model_from_model(self, base_model: Type[BaseModel],
                                                      params: dict) -> WorkFlowInstanceQueryModel:
        base_model = base_model.dict()
        workflow_fields = WorkFlowInstanceQueryModel.__fields__.keys()
        workflow_data = {}
        json_data = {}
        for field, value in params.items():
            if field in workflow_fields:
                workflow_data[field] = value
        for field, value in base_model.items():
            if field in workflow_fields:
                workflow_data[field] = value
            else:
                json_data[field] = value
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceQueryModel(**workflow_data)
        return work_flow_instance

    async def create_page_response_from_workflow(self, target_model: Type[BaseModel],
                                                 page_response: PaginatedResponse,
                                                 other_mapper: dict[str, str] = None) -> PaginatedResponse:

        result_items = []
        for item in page_response.items:
            inst = orm_model_to_view_model(item, target_model, other_mapper)
            result_items.append(inst)
        page_response = PaginatedResponse(
            has_next=page_response.has_next,
            has_prev=page_response.has_prev,
            page=page_response.page,
            pages=page_response.pages,
            per_page=page_response.per_page,
            total=page_response.total,
            items=result_items
        )
        return page_response
