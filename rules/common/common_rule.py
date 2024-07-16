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
from daos.enum_value_dao import EnumValueDAO

from typing import Type, List
from pydantic import BaseModel


async def send_request(apiname, datadict, method='get', is_need_query_param=False):
    # 发起审批流的 处理
    httpreq = HTTPRequest()
    url = workflow_service_config.workflow_config.get("url")

    url = url + apiname
    headerdict = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    # 如果是query 需要拼接参数
    if method == 'get' or is_need_query_param:
        from urllib.parse import urlencode
        url += ('?' + urlencode(datadict))

    print('参数', url, datadict, headerdict)
    if method == 'get':
        response = await httpreq.get_json(url, headerdict)
    else:
        response = await httpreq.post_json(url, datadict, headerdict)
    print(response, '接口响应')
    if response is None:
        return {}
    if isinstance(response, str):
        return {response}
    return response
    pass


async def convert_fields_to_str(model_instance: Type[BaseModel], fields_to_convert: List[str]):
    # 遍历字段列表，将 int 类型字段转换为 str 类型
    for field in fields_to_convert:
        if hasattr(model_instance, field):
            value = getattr(model_instance, field)
            if isinstance(value, int):
                setattr(model_instance, field, str(value))
    # 返回修改后的模型实例
    return model_instance


async def excel_fields_to_enum(data: dict, import_type):
    bool_type_fields = ["in_post", "full_time_special_education_major_graduate",
                        "received_preschool_education_training", "full_time_normal_major_graduate",
                        "received_special_education_training", "has_special_education_certificate",
                        "free_normal_college_student", "participated_in_basic_service_project",
                        "special_education_teacher", "dual_teacher", "has_occupational_skill_level_certificate",
                        "county_level_backbone", "psychological_health_education_teacher", "is_major_graduate",
                        "representative_or_project", "is_major_normal", "is_concurrent_other_positions"]

    enum_type_fields = ["hukou_type", "hmotf", "nationality", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", ]
    teacher_info_fields = {"hukou_type": "hukou_type", "hmotf": "hmotf_type", "nationality": "nationality",
                           "ethnicity": "ethnicity", "marital_status": "marital_status",
                           "political_status": "political_status", "health_condition": "health_status",
                           "source_of_staff": "staff_source", "staff_category": "staff_type",
                           "employment_form": "staffing_arrangement", "contract_signing_status": "singin_contract_type",
                           "information_technology_application_ability": "information_ability",
                           "highest_education": "highest_education",
                           "highest_education_level": "highest_education_level",
                           "highest_degree_name": "education_name", "current_post_level": "position_level",
                           "current_technical_position": "professional_technical_position",
                           "main_teaching_level": "main_teaching_level_type", "teaching_discipline": "subject_category",
                           "language": "language", "language_proficiency_level": "proficiency",
                           "language_certificate_name": "language_certificate_names",
                           "contact_address": "contact_address"}
    teacher_learn_experience = {}

    model_map = {"import_teacher": teacher_info_fields, "import_teacher_learn_experience": teacher_learn_experience}
    fields = model_map.get(import_type)
    for key, value in data.items():
        if value:
            if key in bool_type_fields:
                if value == "是":
                    data[key] = True
                elif value == "否":
                    data[key] = False
            if key in fields:
                if key == "contact_address":
                    data[key] = await get_address_by_description(value)

                else:
                    data[key] = await get_enum_value(value, fields[key])

    return data


async def get_enum_value(description: str, enum_name: str):
    # 通过规则获取枚举值
    parts = description.split('-')
    level = len(parts)
    last_part = parts[-1]
    enum_name = f"{enum_name}_lv{level}"
    enum_value_rule = get_injector(EnumValueRule)
    enum_value = await enum_value_rule.get_enum_value_by_description_and_name(last_part, enum_name)
    return enum_value


async def get_address_by_description(description: str):
    enum_value_rule = get_injector(EnumValueRule)
    enum_value = await enum_value_rule.get_address_by_description(description)
    return enum_value
