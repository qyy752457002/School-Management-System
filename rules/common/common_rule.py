# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import json
import random
import traceback
from datetime import datetime
from typing import List, Type, Dict

from mini_framework.authentication.config import authentication_config
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.web.middlewares.auth import get_auth_url
from mini_framework.web.request_context import request_context_manager
from pydantic import BaseModel

from business_exceptions.common import SocialCreditCodeExistError, SschoolNoExistError
from daos.campus_dao import CampusDAO
from daos.class_dao import ClassesDAO
from daos.grade_dao import GradeDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from models.public_enum import IdentityType
from rules.enum_value_rule import EnumValueRule
from views.common.common_view import workflow_service_config, orgcenter_service_config, check_result_org_center_api, \
    log_json, write_json_to_log, convert_dates_to_strings, json_date_hook

APP_CODE = "1238914398508736"

from datetime import datetime, timedelta

# 缓存数据和过期时间
user_info_cache = {}
cache_expiry = timedelta(minutes=30)  # 缓存过期时间设置为30分钟

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
    # print(response, '接口响应')
    # 示例使用
    json_data = response
    log_json(json_data)
    # 示例数据
    data = [
        response
    ]

    # 调用函数
    write_json_to_log(  data)
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
    research_achievements_patent = {"type": "patent_type", "role": "patent_role"}
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


async def send_orgcenter_request(apiname, datadict, method='get', is_need_query_param=False):
    # 发起审批流的 处理
    httpreq = HTTPRequest()
    url = orgcenter_service_config.orgcenter_config.get("url")

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
    try:
        if method == 'get':
            response = await httpreq.get_json(url, headerdict)
        else:
            # print(type(datadict), "数据类型")
            response = await httpreq.post_json(url, datadict, headerdict)

        # print( '接口响应',response)
        # print(type(response), "数据类型")

        # json_data =  JsonUtils.json_str_to_dict( response)

        # logger.info('接口响应',response)
        response=convert_dates_to_strings(response)
        # 示例数据
        data = [
            response
        ]
        write_json_to_log(  data)

        # 示例使用
        json_data = response
        log_json(json_data)


        # 调用函数

        if response is None:
            return {}
        if isinstance(response, str):
            return {response}
        check_result_org_center_api(response)
        return response
        pass
    except Exception as e:
        print('发生异常', e)
        traceback.print_exc()
        # raise Exception(e)
        return {}

    pass


async def get_identity_by_job(school_operation_type: List, post_type=None):
    identity = ""

    staff_student_map = {"preSchoolEducation_kindergarten": "kindergarten_student",
                         "primaryEducation_primarySchool": "primary_school_student",
                         "secondaryEducation_ordinaryJuniorHigh_ordinaryJuniorHighSchool": "middle_school_student",
                         "secondaryEducation_ordinaryHighSchool": "high_school_student",
                         "secondaryEducation_secondaryVocationalSchool": "vocational_student"}
    staff_teacher_map = {"preSchoolEducation_kindergarten": "kindergarten_teacher",
                         "primaryEducation_primarySchool": "primary_school_teacher",
                         "secondaryEducation_ordinaryJuniorHigh_ordinaryJuniorHighSchool": "middle_school_teacher",
                         "secondaryEducation_ordinaryHighSchool": "high_school_teacher",
                         "secondaryEducation_secondaryVocationalSchool": "vocational_teacher",
                         "secondaryEducation_ordinaryJuniorHigh_nineYearSystemSchool": "nine_year_teacher",
                         "secondaryEducation_ordinaryHighSchool_twelveYearSystemSchool": "twelve_year_teacher",
                         "specialEducation_specialEducationSchool": "special_education_teacher"}
    staff_map = {"preSchoolEducation_kindergarten": "kindergarten_staff",
                 "primaryEducation_primarySchool": "primary_school_staff",
                 "secondaryEducation_ordinaryJuniorHigh_ordinaryJuniorHighSchool": "middle_school_staff",
                 "secondaryEducation_ordinaryHighSchool": "high_school_staff",
                 "secondaryEducation_secondaryVocationalSchool": "vocational_staff",
                 "secondaryEducation_ordinaryJuniorHigh_nineYearSystemSchool": "nine_year_staff",
                 "secondaryEducation_ordinaryHighSchool_twelveYearSystemSchool": "twelve_year_staff",
                 "specialEducation_specialEducationSchool": "special_education_staff"}
    staff_manager_map = {"preSchoolEducation_kindergarten": "kindergarten_principal",
                         "primaryEducation_primarySchool": "primary_school_principal",
                         "secondaryEducation_ordinaryJuniorHigh_ordinaryJuniorHighSchool": "middle_school_principal",
                         "secondaryEducation_ordinaryHighSchool": "high_school_principal",
                         "secondaryEducation_secondaryVocationalSchool": "vocational_principal",
                         "secondaryEducation_ordinaryJuniorHigh_nineYearSystemSchool": "nine_year_principal",
                         "secondaryEducation_ordinaryHighSchool_twelveYearSystemSchool": "twelve_year_principal",
                         "specialEducation_specialEducationSchool": "special_education_principal"}
    parent_map = {"preSchoolEducation_kindergarten": "kindergarten_parent",
                  "primaryEducation_primarySchool": "primary_school_parent",
                  "secondaryEducation_ordinaryJuniorHigh_ordinaryJuniorHighSchool": "middle_school_parent",
                  "secondaryEducation_ordinaryHighSchool": "high_school_parent",
                  "secondaryEducation_secondaryVocationalSchool": "vocational_parent"},
    if post_type is None :
        identity_type = IdentityType.STAFF.value
        identity = "education_unit_staff"
        return identity_type, identity

    parts = post_type.split(',')
    if parts[0] == "student":
        identity_type = IdentityType.STUDENT.value
        for i in range(len(school_operation_type), 0, -1):
            key = '_'.join(school_operation_type[:i])
            if key in staff_student_map:
                identity = staff_student_map.get(key)
                break
    elif parts[0].strip() == '1':  # 表示是专任教师
        identity_type = IdentityType.STAFF.value
        for i in range(len(school_operation_type), 0, -1):
            key = '_'.join(school_operation_type[:i])
            if key in staff_teacher_map:
                identity = staff_teacher_map.get(key)
                break
    elif post_type == "2,21":  # 表示是校园长
        identity_type = IdentityType.MANAGER.value
        for i in range(len(school_operation_type), 0, -1):
            key = '_'.join(school_operation_type[:i])
            if key in staff_manager_map:
                identity = staff_manager_map.get(key)
                break
    elif parts[0] == "parent":
        identity_type = IdentityType.PARENT.value
        for i in range(len(school_operation_type), 0, -1):
            key = '_'.join(school_operation_type[:i])
            if key in parent_map:
                identity = parent_map.get(key)
                break
    else:
        identity_type = IdentityType.STAFF.value
        identity = "education_unit_staff"
        for i in range(len(school_operation_type), 0, -1):
            key = '_'.join(school_operation_type[:i])
            if key in staff_map:
                identity = staff_map.get(key)
                break

    return identity_type, identity


async def get_school_map(keycolum: str, ):
    school_dao = get_injector(SchoolDAO)
    schools = await school_dao.get_all_schools()
    dic = {}
    for row in schools:
        dic[getattr(row, keycolum)] = row
    schools = dic
    return schools


async def get_session_map(keycolum: str, ):
    school_dao = get_injector(StudentSessionDao)
    schools = await school_dao.get_all_student_sessions()
    dic = {}
    for row in schools:
        dic[getattr(row, keycolum)] = row
    schools = dic
    return schools


async def get_grade_map(keycolum: str, ):
    school_dao = get_injector(GradeDAO)
    schools = await school_dao.get_all_grades()
    dic = {}
    for row in schools:
        dic[getattr(row, keycolum)] = row
    schools = dic
    return schools


async def get_class_map(keycolum: str, ):
    school_dao = get_injector(ClassesDAO)
    schools = await school_dao.get_all_class()
    dic = {}
    for row in schools:
        dic[getattr(row, keycolum)] = row
    schools = dic
    return schools


async def check_social_credit_code(social_credit_code: str | None,current_school=None  ):
    if social_credit_code is None or social_credit_code == "":
        return
    pschool_dao = get_injector(PlanningSchoolDAO)
    school_dao = get_injector(SchoolDAO)
    campus_dao = get_injector(CampusDAO)
    exist = await pschool_dao.get_planning_school_by_args(current_school,social_credit_code=social_credit_code, is_deleted=False)
    if exist:
        print("唯一检测1", social_credit_code, exist)
        raise SocialCreditCodeExistError()
    not_equal_age = dict()
    # if current_school is not None:
    #     not_equal_age = {'id !=': current_school.id}

        # users_not_30 = query_users(**not_equal_age, school_id=current_school.id)

    # users_not_30 = query_users(**not_equal_age)
    exist = await school_dao.get_school_by_args(current_school,social_credit_code=social_credit_code, is_deleted=False)
    if exist:
        print("唯一检测2", social_credit_code, exist)

        raise SocialCreditCodeExistError()
    exist = await campus_dao.get_campus_by_args(social_credit_code=social_credit_code, is_deleted=False)
    if exist:
        print("唯一检测3", social_credit_code, exist)

        raise SocialCreditCodeExistError()


async def check_school_no(school_no: str | None, ):
    if school_no is None or school_no == "":
        return
    school_dao = get_injector(SchoolDAO)

    exist = await school_dao.get_school_by_args(school_no=school_no, is_deleted=False)
    if exist:
        print("唯一检测2", school_no, exist)

        raise SschoolNoExistError()


async def get_org_center_userinfo():
    """
Get the user from Casdoor providing the user_id.
:param user_id: the id of the user
:return: a dict that contains user's info
"""

    try:
        account = request_context_manager.current().current_login_account
        # print(account)
        # 目前的  full_account_info是灭有的  会异常 现在临时写固定值  todo  应该加到 框架里
        # full_account = request_context_manager.current().full_account_info

        endpoint = "https://org-center.f123.pub"
        apiname = "/api/get-user"
        # authentication_config
        owner = "sysjyyjyorg"
        params = {
            "id": f"{owner}/{account.name}",
            "clientId": authentication_config.oauth2.client_id,
            "clientSecret": authentication_config.oauth2.client_secret,
        }
        # r = requests.get(url, params)
        # response = r.json()

        # datadict

        datadict = params

        response = await send_orgcenter_request(apiname, datadict, 'get', False)
        # print(' 接口响应', response, )

        if response["status"] != "ok":
            raise Exception(response["msg"])
        # print(response['data2'].keys())

        info = response['data2']
        print(' 解析结果', type(info), )
        # 将字典转换为JSON格式的字符串
        json_string = json.dumps(info, ensure_ascii=False)

        # 打印JSON字符串
        # print(json_string)
        p = info['policies']
        role = info['roles'][0]['roleCode']
        # 遍历列表里的每个
        import csv
        resource_codes = []
        resource_codes_actions = []

        for i, value in enumerate(p):
            data = []
            # print(value['modelText'])
            # print(type(value['ruleCode']), value['ruleCode'])
            # 数据列表，每个子列表是一行数据 todo 调整返回给前段的按照 资源。json的格式来
            # 移除字符串首尾的方括号，并按逗号加空格分割
            data_str = value['ruleCode']
            # data_str.replace("\"", "'")
            # print(data_str)

            data = data_list = eval(data_str)
            # print(type(data_list), data_list)
            # pprint.pprint(data_list)
            # exit(1)
            # data_list = data_str.strip("[]").split("\",\"")

            # 去除每个元素两侧的双引号
            # data = [item.strip("\"") for item in data_list]
            # eval("data="+ value['ruleCode'])
            # data = value['ruleCode']

            # 指定 CSV 文件名
            filename = str(i) + 'policy.csv'
            print('写入文件：', filename)

            gstr = "g, alice, " + role

            # 打开文件，准备写入
            with open(filename, 'w', encoding='utf-8') as file:
                # 遍历列表，将每个元素写入文件的一行
                for item in data:
                    p_list = item.split(",")
                    resource_codes.append(p_list[1].strip(" "))
                    resource_codes_actions.append(','.join([p_list[1].strip(" "), p_list[2].strip(" ")]))
                    p_list.insert(1, role)
                    join_str = ','.join(p_list)
                    file.write(join_str + '\n')  # 写入元素，并添加换行符
                file.write(gstr + '\n')  # 写入元素，并添加换行符

            #
            # # 打开文件，'w' 表示写入模式
            # with open(filename, 'w', newline='') as csvfile:
            #     # 创建 csv 写入器
            #     csvwriter = csv.writer(csvfile)
            #
            #     # 写入数据
            #     for row in data:
            #         print('111',row)
            #         csvwriter.writerow(row)
            # if i == "identity":
            #     info[i] = json.loads(value)
            break

        print('资源编码', resource_codes)
        # 把资源编码里面的美格元素的逗号左边作为字典的键 右侧的放入列表 列表作为字典的键
        resource_codes_dict = {}
        for value in resource_codes_actions:
            # value = resource_codes[i]
            temp= value.split( ',')
            # print('temp',temp)
            key =  temp[0]
            action  = temp[1]
            if key not in resource_codes_dict.keys():
                resource_codes_dict[key] = []
                resource_codes_dict[key] .append(action)
            else:
                resource_codes_dict[key].append(action)
            # print('资源编码', resource_codes_dict)

        return info, resource_codes, resource_codes_dict

        # return response, datadict
    except Exception as e:
        print('获取用户权限信息异常', e)
        traceback.print_exc()
        # raise e
        return None, None, None

    return None


async def verify_auth(sub: str, obj, act):
    import casbin

    e = casbin.Enforcer("model.conf", "0policy.csv")

    # sub = "alice"  # the user that wants to access a resource.
    # obj = "grade"  # the resource that is going to be accessed.
    # act = "add"  # the operation that the user performs on the resource.

    if e.enforce(sub, obj, act):
        # permit alice to read data1
        print("permit alice to read data1")
        return True
        pass
    else:
        # deny the request, show an error
        print("deny the request, show an error")
        return False
        pass

    pass


async def verify_auth_by_obj_and_act(obj, act):
    """
    验证用户权限
    :param obj:
    :param act:
    :return:
    """
    account = request_context_manager.current().current_login_account
    account_name = account.name

    file_name = await process_userinfo(account_name)
    print( '验证结果',file_name,)
    if file_name is None:
        return False
    # 当abac是 这里是一个字典 包含了属性
    # 定义请求的属性

    token = request_context_manager.current()
    # query= token['query_params']
    # print(query)
    objattr = {
        "Age": 25,
        "department": "sales"
    }
    file_name = await verify_auth_by_file_name(account_name, obj, act, file_name)
    return file_name


async def process_userinfo(account_name):
    # print(222, authentication_config.oauth2)
    # appCode = authentication_config.oauth2.app_code
    appCode = orgcenter_service_config.orgcenter_config.get("app_code")

    user_info = await get_cached_userinfo(account_name)
    if user_info is None:
        return None
    lines = []  # 使用列表收集所有要写入的行
    filename = account_name + 'policy.csv'
    for rule in user_info['roles']:
        if rule["appCode"] == appCode:
            role = rule['roleCode']
            g_str = f"g, {account_name}, " + role
            role_policies = rule['rolepolicies']
            for policy in role_policies:
                if not policy:
                    continue
                json_str= policy['rule_code']
                if json_str.strip():
                    # data = json.loads(json_str)
                    try:
                        data_str = json.loads(policy['rule_code'], object_hook=json_date_hook)
                        for item in data_str:
                            p_list = item.split(",")
                            p_list.insert(1, role)
                            join_str = ','.join(p_list)
                            lines.append(join_str + '\n')

                    except json.JSONDecodeError as e:
                        print(f"解析错误：{e}")


                else:
                    print("字符串为空或只包含空白字符")

            lines.append(g_str + '\n')
        else:
            continue
    if not lines:
        return None
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)
    print('策略文件',filename)
    return filename


async def get_cached_userinfo(account_name: str):
    now = datetime.now()
    cache_entry = user_info_cache.get(account_name)
    if cache_entry:
        user_info, timestamp = cache_entry
        if now - timestamp < cache_expiry:
            return user_info  # 返回缓存的数据
    user_info = await get_org_center_user_info()
    if user_info is not None:
        user_info_cache[account_name] = (user_info, now)
    return user_info


async def get_org_center_user_info():
    try:
        account = request_context_manager.current().current_login_account
        apiname = "/api/get-user"
        owner = "sysjyyjyorg"
        params = {
            "id": f"{owner}/{account.name}",
            "clientId": authentication_config.oauth2.client_id,
            "clientSecret": authentication_config.oauth2.client_secret,
        }
        datadict = params
        response = await send_orgcenter_request(apiname, datadict, 'get', False)
        print('获取用户权限信息 status',response["status"])
        # print(response)
        if response["status"] != "ok":
            raise Exception(response["msg"])
        info = response['data2']
        if len(info['roles']) == 0:
            return None
        else:
            for i in range(len(info['roles'])):
                role_policies = len(info['roles'][i]["rolepolicies"])
                if role_policies > 0:
                    return info
            return None
    except Exception as e:
        print('获取用户权限信息异常', e)
        return None

async def verify_auth_by_file_name(sub: str|dict, obj, act, file_name):
    import casbin
    e = casbin.Enforcer("model.conf", file_name)
    print("校验权限  ", sub, obj, act)

    if e.enforce(sub, obj, act):
        print("permit 允许")
        return True
    else:
        print("deny the request, 权限 不足")
        return False
    pass
async def filter_action_by_file_name( item , processed_dict):
    #读取文件 获取数据 匹配里面的内容
    print(11,item,)
    if item['action'] and item['resource_code']:
        if  item['resource_code']  in processed_dict.keys():
            listtt = item['action'].split(',')
            newlist = []
            for action in  listtt:
                if action in processed_dict[item['resource_code']]:
                    print('匹配到权限', action)
                    newlist.append(action)
                    continue
                    # return True
                else:
                    listtt.remove(action)
                    print('移除这个权限 ',action, processed_dict[item['resource_code']])
            # print('匹配到权限', item)
            item['action']= ','.join(newlist)
            print('过滤后res',item)
            return True
        else:
            return False


    pass
def read_file_to_permission_dict(file_content):
    # 初始化一个空字典
    result_dict = {}

    # 按行分割文件内容并遍历每一行
    for line in file_content.strip().split('\n'):
        # 用逗号分割每一行，并去除多余的空格
        parts = [part.strip() for part in line.split(',')]

        # 检查行是否有足够的部分
        if len(parts) >= 4:
            key = parts[2]
            value = parts[3]

            # 如果键已经在字典中，将值追加到列表中
            if key in result_dict:
                result_dict[key].append(value)
            else:
                # 否则，创建一个包含值的新的列表
                result_dict[key] = [value]

    return result_dict




# 退出
async def login_out():
    """

    """
    # account = request_context_manager.current().current_login_account
    # account_name = account.name

    # file_name = await process_userinfo(account_name)
    user_info = await request_org_center_login_out()

    print( '验证结果',user_info,)
    request=request_context_manager.current()

    auth_uri = await get_auth_url(request)



    return auth_uri
async def request_org_center_login_out():
    try:
        token = request_context_manager.current().token
        apiname = "/api/logout"
        # owner = "sysjyyjyorg"
        params = {
            # "id": f"{owner}/{account.name}",
            # "clientId": authentication_config.oauth2.client_id,
            # "clientSecret": authentication_config.oauth2.client_secret,
            "state":  'application-center',
            "post_logout_redirect_uri":  '', #如果是要跳转 传入要跳的url
            "id_token_hint": token,
        }
        datadict = params
        response = await send_orgcenter_request(apiname, datadict, 'get', True)
        print('登出res',response)
        if response["status"] == "ok":
            # raise Exception(response["msg"])
            pass
        return True


    except Exception as e:
        print('获取登出异常', e)
        return None
