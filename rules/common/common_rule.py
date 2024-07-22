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

from rules.enum_value_rule import EnumValueRule
from views.common.common_view import workflow_service_config
from views.models.campus import Campus as CampusModel

from views.models.campus import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.planning_school_dao import PlanningSchoolDAO
from views.models.school import School as SchoolModel
from daos.enum_value_dao import EnumValueDAO

from typing import Type, List, Dict
from pydantic import BaseModel
from datetime import datetime


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


async def excel_fields_to_enum(data: dict, import_type) -> Dict:
    bool_type_fields = ["in_post", "full_time_special_education_major_graduate",
                        "received_preschool_education_training", "full_time_normal_major_graduate",
                        "received_special_education_training", "has_special_education_certificate",
                        "free_normal_college_student", "participated_in_basic_service_project",
                        "special_education_teacher", "dual_teacher", "has_occupational_skill_level_certificate",
                        "county_level_backbone", "psychological_health_education_teacher", "is_major_graduate",
                        "representative_or_project", "is_major_normal", "is_concurrent_other_positions"]

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
                           "contact_address": "contact_address", "current_post_type": "position_type",
                           "birth_place": "contact_address", "enterprise_work_experience": "seniority",
                           "recruitment_method": "staff_source"}
    teacher_learn_experience = {"type_of_institution": "type_of_institution", "study_mode": "learning_method",
                                "country_or_region_of_education": "nationality", "major_learned": "major",
                                "country_or_region_of_degree_obtained": "nationality",
                                "education_obtained": "highest_education", "degree_level": "highest_education_level",
                                "degree_name": "education_name", }
    teacher_work_experience = {"on_duty_position": "position_type",
                               "institution_nature_category": "institution_nature_category"}
    teacher_job_appointments = {"position_level": "position_level", "position_category": "job_category", }
    teacher_professional_titles = {"current_professional_title": "technical_position"}
    teacher_qualifications = {"teacher_qualification_type": "teacher_certificate_type"}
    teacher_skill_certificates = {"language": "language", "proficiency_level": "proficiency",
                                  "other_skill_level": "proficiency", "certificate_type": "certificate_type",
                                  "language_certificate_name": "language_certificate_names"}
    teacher_ethic_records_rewards = {"honor_level": "honor_level",
                                     "ethics_assessment_conclusion": "moral_assessment_conclusion"}
    teacher_ethic_records_disciplinary = {"disciplinary_reason": "punish_reason",
                                          "disciplinary_category": "punish_type"}
    educational_teaching = {"semester": "semester", "teaching_stage": "main_teaching_level_type", }
    talent_programs = {"talent_project_name": "talent_project_name"}
    domestic_training = {"training_type": "training_type", "training_mode": "training_mode"}
    overseas_study = {"country_region": "nationality"}
    annual_review = {"assessment_result": "assessment_result"}

    # 科研成果——项目
    research_achievements_project = {"type": "project_type", "role": "project_role", "source": "project_source", }
    # 科研成果——著作
    research_achievements_book = {"type": "book_type", "role": "book_role"}
    # 科研成果——论文
    research_achievements_paper = {"role": "paper_role", "indexing_status": "indexing_status"}
    # 科研成果——奖励
    research_achievements_reward = {"authorized_country": "nationality", "personal_rank": "personal_rank",
                                    "research_level": "reward_research_level", "type": "research_reward_type"}
    # 科研成果——文艺作品
    research_achievements_artwork = {"role": "artwork_role", "type": "artwork_type"}
    # 科研成果——专利
    research_achievements_patent = {"type": "patent_type"}
    # 科研成果——竞赛奖励
    research_achievements_competition = {"role": "competition_role"}
    # 科研成果——医药
    research_achievements_medicine = {"role": "artwork_role"}

    model_map = {"import_teacher": teacher_info_fields, "import_teacher_learn_experience": teacher_learn_experience,
                 "import_teacher_job_appointments": teacher_job_appointments,
                 "import_teacher_work_experience": teacher_work_experience,
                 "import_teacher_professional_titles": teacher_professional_titles,
                 "import_teacher_qualifications": teacher_qualifications,
                 "import_teacher_skill_certificates": teacher_skill_certificates,
                 "import_teacher_ethic_records_rewards": teacher_ethic_records_rewards,
                 "import_teacher_ethic_records_disciplinary": teacher_ethic_records_disciplinary,
                 "import_educational_teaching": educational_teaching,
                 "import_talent_programs": talent_programs,
                 "import_domestic_training": domestic_training,
                 "import_overseas_study": overseas_study,
                 "import_annual_review": annual_review,
                 "import_research_achievements_project": research_achievements_project,
                 "import_research_achievements_book": research_achievements_book,
                 "import_research_achievements_paper": research_achievements_paper,
                 "import_research_achievements_reward": research_achievements_reward,
                 "import_research_achievements_artwork": research_achievements_artwork,
                 "import_research_achievements_patent": research_achievements_patent,
                 "import_research_achievements_competition": research_achievements_competition,
                 "import_research_achievements_medicine": research_achievements_medicine
                 }
    fields = model_map.get(import_type)
    for key, value in data.items():
        if value:
            if key in bool_type_fields:
                if value == "是":
                    data[key] = True
                elif value == "否":
                    data[key] = False
            if key in fields:
                address_list = ["contact_address", "birth_place"]
                if key == "teaching_discipline":
                    continue
                if key in address_list:
                    data[key] = await get_address_by_description(value)
                else:
                    data[key] = await get_enum_value(value, fields[key])
    return data


async def get_enum_value(description: str, enum_name: str):
    # 通过规则获取枚举值
    values = []
    parts = description.split('-')
    level = len(parts)
    parent_id = 0
    for i in range(level):
        last_part = parts[i]
        enum_name_db = f"{enum_name}_lv{i + 1}"
        enum_value_rule = get_injector(EnumValueRule)
        enum_value, parent_id = await enum_value_rule.get_enum_value_by_description_and_name(last_part, enum_name_db,
                                                                                             parent_id)
        values.append(enum_value)
    value = ",".join(values)
    return value


async def get_address_by_description(description: str):
    enum_value_rule = get_injector(EnumValueRule)
    enum_value = await enum_value_rule.get_address_by_description(description)
    return enum_value
