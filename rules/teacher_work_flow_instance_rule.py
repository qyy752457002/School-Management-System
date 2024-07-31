from datetime import date, datetime
from typing import Type
from urllib.parse import urlencode

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from pydantic import BaseModel

from views.common.common_view import workflow_service_config
from views.models.work_flow import WorkFlowInstanceCreateModel, WorkFlowInstanceModel, WorkFlowInstanceQueryModel


@dataclass_inject
class TeacherWorkFlowRule(object):

    async def add_teacher_work_flow(self, model: Type[BaseModel], params: dict):
        """
        parameters = {"process_code": process_code,"applicant_name": applicant_name}
        """
        work_instance_instance = await self.create_workflow_from_model(model, params)
        parameters = work_instance_instance.dict()
        params_data = JsonUtils.dict_to_json_str(parameters)

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
        print(work_flow_instance)
        return work_flow_instance

    async def add_work_flow_by_multi_model(self, model_list: list[Type[BaseModel]], params: dict):
        """
        parameters = {"process_code": process_code,"applicant_name": applicant_name}
        """
        work_instance_instance = await self.create_work_flow_model_from_multi_model(model_list, params)
        parameters = work_instance_instance.dict()
        params_data = JsonUtils.dict_to_json_str(parameters)
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
        return work_flow_instance

    async def update_teacher_work_flow(self, model: Type[BaseModel]):
        work_instance_instance = await self.update_workflow_from_model(model)
        parameters = work_instance_instance.dict()
        params_data = JsonUtils.dict_to_json_str(parameters)
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        api_name = '/api/school/v1/teacher-workflow/work-flow-insatnce'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        print(f"参数是{parameters}")
        result = await httpreq.patch(url, params_data, headerdict)
        print(f"result的结果是{result}")

    async def process_transaction_work_flow(self, node_instance_id: int, parameters: dict):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"node_instance_id": node_instance_id}
        params_data = JsonUtils.dict_to_json_str(parameters)
        # data = {"parameters": parameters}
        api_name = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        next_node_instance_wf = await httpreq.post(url, params_data, headerdict)
        next_node_instance = JsonUtils.json_str_to_dict(next_node_instance_wf)
        return next_node_instance

    async def update_work_flow_by_param(self, process_instance_id: int, parameters: dict):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params_data = JsonUtils.dict_to_json_str(parameters)
        api_name = "/api/school/v1/teacher-workflow/work-flow-status-by-params"
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        params = {"process_instance_id": process_instance_id}
        url += ('?' + urlencode(params))
        await httpreq.patch(url, params_data, headerdict)
        return

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

    async def get_work_flow_define(self, process_instance_id):
        """
        获取整个审批有哪些节点
        """
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/work-flow-define'
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

    async def get_work_flow_instance_by_process_instance_id(self, process_instance_id: int):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        params = {"process_instance_id": process_instance_id}
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance-by-process-instance-id'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(params))
        result = await httpreq.get_json(url, headerdict)
        # result = JsonUtils.json_str_to_dict(result)
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
        print('拼装参数', parameters)
        query_parmas = {k: v for k, v in parameters.items() if v is not None and v != ''}
        print('查询参数', query_parmas)
        # params_data = JsonUtils.dict_to_json_str(parameters)
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance'
        url += api_name
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(query_parmas))
        print('发起调用', url)
        result = await httpreq.get(url, headerdict)
        result = JsonUtils.json_str_to_dict(result)
        page_result = PaginatedResponse(**result)
        print(f'结果是{page_result}')
        page_response = await self.create_page_response_from_workflow(query_re_model, page_result)
        return page_response
    async def get_work_flow_instance_by_query_model(self, query_model: Type[BaseModel],query_re_model: Type[BaseModel]):
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        query_model_instance = query_model.dict()
        parameters = query_model_instance
        api_name = '/api/school/v1/teacher-workflow/work-flow-instance-by-query-model'
        url += api_name
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        url += ('?' + urlencode(parameters))
        result = await httpreq.get_json(url, headerdict)
        # result = JsonUtils.json_str_to_dict(result)
        result_list=[]
        if result:
            for item in result:
                item = await self.create_model_from_workflow(item, query_re_model)
                result_list.append(item)
        return result_list

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
        json_data = JsonUtils.dict_to_json_str(json_data)
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceCreateModel(**workflow_data)
        return work_flow_instance

    async def update_workflow_from_model(self, base_model: Type[BaseModel],
                                         ) -> WorkFlowInstanceModel:
        base_model = base_model.dict()
        workflow_fields = WorkFlowInstanceModel.__fields__.keys()
        workflow_data = {}
        json_data = {}
        for field, value in base_model.items():
            if field in workflow_fields:
                workflow_data[field] = value
            else:
                json_data[field] = value
        json_data = JsonUtils.dict_to_json_str(json_data)
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceModel(**workflow_data)
        return work_flow_instance

    async def create_model_from_workflow(self, work_flow_instance: dict, model: Type[BaseModel]):
        model_fields = model.__fields__.keys()
        model_data = {}
        if work_flow_instance["json_data"] != "":
            work_flow_instance["json_data"] = JsonUtils.json_str_to_dict(work_flow_instance["json_data"])
        for key, value in work_flow_instance.items():
            if isinstance(value, (date, datetime)):
                work_flow_instance[key] = value.strftime("%Y-%m-%d %H:%M:%S")

        for field in model_fields:
            if field in work_flow_instance.keys():
                model_data[field] = work_flow_instance[field]
            elif "json_data" in work_flow_instance and field in work_flow_instance["json_data"]:
                model_data[field] = work_flow_instance["json_data"][field]
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
                if isinstance(value, tuple):
                    workflow_data[field] = None
        for field, value in base_model.items():
            if field in workflow_fields:
                workflow_data[field] = value
                if isinstance(value, tuple):
                    workflow_data[field] = None
            else:
                json_data[field] = value
        json_data = JsonUtils.dict_to_json_str(json_data)
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceQueryModel(**workflow_data)
        return work_flow_instance

    async def create_page_response_from_workflow(self, target_model: Type[BaseModel],
                                                 page_response: PaginatedResponse,
                                                 other_mapper: dict[str, str] = None) -> PaginatedResponse:

        result_items = []
        for item in page_response.items:
            if target_model is None:
                inst = item
                pass
            else:
                inst = await self.create_model_from_workflow(item, target_model)
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

    async def create_work_flow_model_from_multi_model(self, base_model_list: list[Type[BaseModel]],
                                                      params: dict) -> WorkFlowInstanceCreateModel:
        base_model = {}
        for item in base_model_list:
            base_model.update(item.dict())
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
        json_data = JsonUtils.dict_to_json_str(json_data)
        workflow_data["json_data"] = json_data
        print(workflow_data)
        work_flow_instance = WorkFlowInstanceCreateModel(**workflow_data)
        return work_flow_instance
