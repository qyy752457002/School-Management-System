# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
import hashlib

import shortuuid
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.school import SchoolNotFoundError
from daos.campus_dao import CampusDAO
from daos.school_dao import SchoolDAO
from models.campus import Campus
from rules.enum_value_rule import EnumValueRule
from views.common.common_view import workflow_service_config
from views.models.campus import Campus as CampusModel

from views.models.campus import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.planning_school_dao import PlanningSchoolDAO
from views.models.school import School as SchoolModel



async def send_request(apiname,datadict,method='get'):

    # 发起审批流的 处理
    httpreq= HTTPRequest()
    url= workflow_service_config.workflow_config.get("url")

    url = url + apiname
    headerdict = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    # 如果是query 需要拼接参数
    if method == 'get':
        from urllib.parse import urlencode
        url += ('?' + urlencode(datadict))

    print('参数', url, datadict, headerdict)
    if method == 'get':
        response = await httpreq.get_json(url,headerdict)
    else:
        response = await httpreq.post_json(url,datadict,headerdict)
    print(response,'接口响应')
    if response is None:
        return {}
    if isinstance(response, str):
        return {response}
    return response
    pass