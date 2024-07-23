from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.utils.http import HTTPRequest
from urllib.parse import urlencode
from views.common.common_view import workflow_service_config
from pydantic import BaseModel
from views.models.work_flow import WorkFlowInstanceCreateModel, WorkFlowInstanceModel, WorkFlowInstanceQueryModel
from mini_framework.utils.json import JsonUtils
from daos.teachers_dao import TeachersDao
from datetime import date, datetime
from typing import Type


@dataclass_inject
class TeacherOrganisation(object):
    teachers_dao: TeachersDao
    async def add_educate_user_teacher(self, teacher_id):
        """
        新接组织中心相关内容添加用户
        """
        educate_user = await self.teachers_dao.get_teachers_by_id(teacher_id)
        educate_user = orm_model_to_view_model(educate_user, EducateUserTeacherModel, exclude=[""])
        params_data = JsonUtils.dict_to_json_str(educate_user)

        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        api_name = '/api/add-educate-user'
        url += api_name
        headerdict = {
            "accept": "application/json",
            # "Authorization": "{{bear}}",
            "Content-Type": "application/json"
        }
        # url += ('?' + urlencode(parameters))
        result = await httpreq.post(url, params_data, headerdict)
        return result
