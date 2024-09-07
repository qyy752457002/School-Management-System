import math
from datetime import date, datetime
from enum import Enum

from fastapi.params import Query
from id_validator import validator
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.design_patterns.singleton import singleton
from mini_framework.multi_tenant.registry import tenant_registry
from mini_framework.web.request_context import request_context_manager

from business_exceptions.tenant import TenantNotFoundOrUnActiveError
from daos.enum_value_dao import EnumValueDAO
from rules.tenant_rule import TenantRule
from views.common.constant import Constant
from views.models.extend_params import ExtendParams
from views.models.system import UnitType, OrgCenterApiStatus
import json
import logging

frontend_enum_mapping = {'preSchoolEducation': '学前教育', 'kindergarten': '幼儿园',
                         'attachedKindergartenClass': '附设幼儿班',
                         'primaryEducation': '初等教育', 'primarySchool': '小学',
                         'primarySchoolTeachingPoint': '小学教学点',
                         'attachedPrimarySchoolClass': '附设小学班', 'adultPrimarySchool': '成人小学',
                         'staffPrimarySchool': '职工小学', 'migrantWorkerPrimarySchool': '农民工小学',
                         'primarySchoolClass': '小学班', 'literacyClass': '扫盲班', 'secondaryEducation': '中等教育',
                         'ordinaryJuniorHigh': '普通初中', 'vocationalJuniorHigh': '职业初中',
                         'attachedVocationalJuniorHighClass': '附设职业初中班',
                         'adultEmployeeJuniorHigh': '成人职工初中',
                         'adultFarmerJuniorHigh': '成人农民初中', 'adultJuniorHigh': '成人初中',
                         'ordinaryHighSchool': '普通高中',
                         'comprehensiveHighSchool': '完全中学', 'seniorHighSchool': '高级中学',
                         'twelveYearSystemSchool': '十二年一贯制学校',
                         'attachedOrdinaryHighSchoolClass': '附设普通高中班',
                         'adultHighSchool': '成人高中', 'adultEmployeeHighSchool': '成人职工高中',
                         'adultFarmerHighSchool': '成人农民高中', 'secondaryVocationalSchool': '中等职业学校',
                         'adjustedSecondaryVocationalSchool': '调整后中等职业学校',
                         'secondaryTechnicalSchool': '中等技术学校',
                         'secondaryNormalSchool': '中等师范学校',
                         'adultSecondaryProfessionalSchool': '成人中等专业学校',
                         'vocationalHighSchool': '职业高中学校', 'technicalSchool': '技工学校',
                         'attachedVocationalClass': '附设中职班', 'otherVocationalInstitutions': '其他中职机构',
                         'workStudySchool': '工读学校', 'specialEducation': '特殊教育',
                         'specialEducationSchool': '特殊教育学校',
                         'schoolForBlind': '盲人学校', 'schoolForDeaf': '聋人学校',
                         'schoolForIntellectuallyDisabled': '培智学校',
                         'otherSpecialEducationSchools': '其他特教学校',
                         'attachedSpecialEducationClasses': '附设特教班',
                         'otherEducation': '其他教育', 'jinxingInstitution': '进修机构',
                         'researchInstitution': '研究机构',
                         'educationResearchInstitute': '教育研究院', 'practiceInstitution': '实践机构',
                         'practiceBase': '实践基地', 'trainingInstitution': '培训机构', 'PublicOwnership': '公办',
                         'PrivateOwnership': '民办', '1': '一星', '2': '二星', '3': '三星', '4': '四星', '5': '五星',
                         'resident_id_card': '居民身份证', 'military_officer_id': '军官证', 'soldier_id': '士兵证',
                         'civilian_officer_id': '文职干部证', 'military_retiree_id': '部队离退休证',
                         'hong_kong_passport_id': '香港特区护照/身份证明', 'macau_passport_id': '澳门特区护照/身份证明',
                         'taiwan_resident_travel_permit': '台湾居民来往大陆通行证',
                         'overseas_permanent_residence_permit': '境外永久居住证', 'passport': '护照',
                         'birth_certificate': '出生证明', 'household_register': '户口薄', 'other': '其他', 'male': '男',
                         'female': '女'}


def compare_modify_fields(view_model, orm_model):
    """
    比较两个对象  返回需要更新的字段
    :param view_model:
    :param orm_model:
    :return:
    """
    changeitems = dict()
    # 使用视图模型
    vd = view_model.__dict__
    if not orm_model:
        return changeitems
    od = orm_model.__dict__
    vd = convert_dates_to_strings(vd)
    od = convert_dates_to_strings(od)
    # 定义要转换的值的map
    key_map = frontend_enum_mapping

    for key, value in vd.items():
        if key == 'id':
            continue
        if value:
            if key in od and od[key] != value:
                print(key, value, od[key])
                # changeitems.append(key)
                key_cn = ''
                if key in view_model.model_fields.keys():
                    key_cn = view_model.model_fields[key].title
                    if not key_cn:
                        key_cn = view_model.model_fields[key].description
                if not key_cn and key in orm_model.model_fields.keys():
                    key_cn = orm_model.model_fields[key].title
                    if not key_cn:
                        key_cn = orm_model.model_fields[key].description

                valueold = od[key]
                if isinstance(valueold, date):
                    valueold = valueold.strftime('%Y-%m-%d')
                if isinstance(value, date):
                    value = value.strftime('%Y-%m-%d')

                if valueold in key_map.keys():
                    valueold = key_map[valueold]
                if value in key_map.keys():
                    value = key_map[value]

                # 枚举类型的转换
                if isinstance(valueold, Enum):
                    valueold = valueold.value
                if isinstance(value, Enum):
                    value = value.value
                changeitems[key_cn] = {"before": valueold, "after": value}
                # pass
    print('比叫变更域', changeitems)
    return changeitems


def page_none_deal(paging):
    """
    比较两个对象  返回需要更新的字段
    :param planning_school:
    :param orm_model:
    :return:
    """
    for item in paging.items:

        for key, value in item.items():
            if value is None:
                item[key] = ''

    # print(paging.items)

    return paging


def check_id_number(id_number: str):
    is_valid = validator.is_valid(id_number)
    print(is_valid, )
    return is_valid


async def get_extend_params(request) -> ExtendParams:
    headers = request.headers
    obj = ExtendParams()

    if 'Extendparams' in headers:
        extparam = headers['Extendparams']
        if isinstance(extparam, str):
            extparam = eval(extparam)
        obj = ExtendParams(**extparam)
        if obj.unit_type == UnitType.CITY.value:
            obj.city = Constant.CURRENT_CITY
        if obj.county_id:
            # 区的转换   or todo
            enuminfo = await (EnumValueDAO()).get_enum_value_by_value(obj.county_id, 'country')
            if enuminfo:
                obj.county_name = enuminfo.description
    print('Extendparams', obj)

    tenant_code = request_context_manager.current().tenant_code
    tenant =await tenant_registry.get_tenant(tenant_code)
    obj.tenant = tenant

    return obj


def get_client_ip(request):
    client_ip = request.headers.get("X-Forwarded-For", request.client.host)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()

    return client_ip


@singleton
class WorkflowServiceConfig:
    def __init__(self):
        from mini_framework.configurations import config_injection
        manager = config_injection.get_config_manager()
        # 读取 配置
        workflow_service_dict = manager.get_domain_config("workflow_service")
        if not workflow_service_dict:
            raise ValueError('workflow_service configuration is required')
        self.workflow_config = workflow_service_dict


workflow_service_config = WorkflowServiceConfig()

@singleton
class SystemConfig:
    def __init__(self):
        from mini_framework.configurations import config_injection
        manager = config_injection.get_config_manager()
        # 读取 配置
        workflow_service_dict = manager.get_domain_config("system_config")
        if not workflow_service_dict:
            raise ValueError('system_config configuration is required')
        self.system_config = workflow_service_dict


system_config = SystemConfig()


@singleton
class OrgcenterServiceConfig:
    def __init__(self):
        from mini_framework.configurations import config_injection
        manager = config_injection.get_config_manager()
        # 读取 配置
        orgcenter_service_dict = manager.get_domain_config("orgcenter_service")
        if not orgcenter_service_dict:
            raise ValueError('orgcenter_service configuration is required')
        self.orgcenter_config = orgcenter_service_dict


orgcenter_service_config = OrgcenterServiceConfig()


def convert_dates_to_strings(stuinfoadddict):
    for key, value in stuinfoadddict.items():
        if isinstance(value, (date, datetime)):
            stuinfoadddict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value, Query) or isinstance(value, tuple):
            stuinfoadddict[key] = None
        # if isinstance(value,InstanceState):
        #     stuinfoadddict[key] = value.value
    return stuinfoadddict


def convert_snowid_to_strings(paging_result, extra_colums=None):
    """
    将传入的 items 中每个元素的 id 属性转换为字符串类型。

    :param items: 包含可迭代对象的列表或元组，其中每个对象都有 'id' 属性。
    """
    items = paging_result.items
    for item in items:
        convert_snowid_in_model(item, extra_colums)


def convert_snowid_in_model(item, extra_colums=None):
    """
    将传入的 items 中每个元素的 id 属性转换为字符串类型。

    :param items: 包含可迭代对象的列表或元组，其中每个对象都有 'id' 属性。
    """

    if hasattr(item, 'id') and isinstance(item.id, int):
        item.id = str(item.id)
    if extra_colums:
        for col in extra_colums:
            if hasattr(item, col) and isinstance(getattr(item, col), int):
                setattr(item, col, str(getattr(item, col)))


from sqlalchemy.orm import class_mapper


def serialize(model):
    """
    将SQLAlchemy模型实例序列化为字典。
    """
    # 获取模型的映射器
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


# 假设你有一个SQLAlchemy模型实例
# model_instance = MyModel()

# 将模型实例转换为字典
# model_dict = serialize(model_instance)

# 将字典转换为JSON
# model_json = json.dumps(model_dict)


# 函数来处理键名映射  对于josn里的  每个 根据映射提换键名
def map_keys(data, key_map):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            new_key = key_map.get(key, key)  # 如果键在映射中，使用新键，否则使用原键
            new_data[new_key] = map_keys(value, key_map)  # 递归处理嵌套的字典
        return new_data
    elif isinstance(data, list):
        return [map_keys(item, key_map) for item in data]  # 处理列表中的每个元素
    else:
        return data  # 如果是基本类型，直接返回


import requests


def download_file(url, local_filepath):
    """
    从指定的URL下载文件并保存到本地路径。

    :param url: 要下载的文件的URL
    :param local_filepath: 本地文件保存路径
    :return: None
    """
    try:
        # 发送GET请求下载文件
        response = requests.get(url, stream=True)  # 使用stream=True可以处理大文件

        # 检查请求是否成功
        if response.status_code == 200:
            # 打开本地文件路径以写入二进制内容
            with open(local_filepath, 'wb') as file:
                # 将下载的内容写入文件
                for chunk in response.iter_content(chunk_size=8192):  # 逐块写入文件，可以有效处理大文件
                    file.write(chunk)
            print(f'文件已保存到 {local_filepath}')
        else:
            print(f'请求失败，状态码：{response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'请求异常：{e}')


# 使用函数
# download_file('http://example.com/file.pdf', 'path/to/your/local/file.pdf')
# 定义函数 针对 对象里每个属性 如果类型是 pydantic的QUERY 则设置为None
def convert_query_to_none(obj):
    """
    将pydantic的Query类型属性设置为None。

    :param obj: 要转换的对象
    :return: 转换后的对象
    """
    for field_name, field in obj.__fields__.items():
        field = getattr(obj, field_name)
        if isinstance(field, Query) or isinstance(field, tuple):
            setattr(obj, field_name, None)
        if isinstance(field, float):
            if math.isnan(field):
                setattr(obj, field_name, None)
    return obj


def check_result_org_center_api(result):
    """

    """
    is_check_force = False

    if result.get("status") == OrgCenterApiStatus.ERROR.value and is_check_force:
        raise Exception(f"orgcenter api error {result.get('msg')}")



# 配置日志
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

def log_json(json_data, log_file='app.log'):
    """
    将JSON数据记录到日志文件中

    :param json_data: 要记录的JSON数据
    :param log_file: 日志文件的名称，默认为'app.log'
    """
    try:
        # 确保json_data是字符串类型
        if not isinstance(json_data, str):
            json_data = json.dumps(json_data)

        # 尝试解析JSON数据以验证其有效性
        json.loads(json_data)

        # 记录JSON数据到日志文件
        logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s - %(message)s')
        logging.info(json_data)

    except json.JSONDecodeError as e:
        # 如果JSON数据无效，记录错误信息
        logging.error(f"Invalid JSON data: {e}")
    except Exception as e:
        # 记录其他可能的错误
        logging.error(f"An error occurred: {e}")


import json
from datetime import date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # 或者 obj.strftime('%Y-%m-%d')
        return super(DateEncoder, self).default(obj)

# sample_dict = {"name": "Alice", "birthdate": date(1990, 5, 17)}
import json
from datetime import date

def json_date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = date.fromisoformat(value)
        except (ValueError, TypeError):
            pass
    return json_dict

def write_json_to_log( data_list,filename='a.log'):
    with open(filename, 'a') as file:  # 使用 'a' 模式来追加数据
        for data in data_list:
            # 将字典转换为 JSON 格式字符串，并确保每条记录后换行
            file.write(json.dumps(data,cls=DateEncoder) + '\n')

from mini_framework.multi_tenant.tenant import Tenant, TenantStatus


async def get_tenant_by_code(code: str):
    rule = get_injector(TenantRule)
    tenant = await rule.get_tenant_by_code(code)
    print('解析到租户',tenant)
    if tenant is None and code=='210100':
        tenant =  Tenant(
        code=code,
        name="租户1",
        description="租户1",
        status=TenantStatus.active,
        client_id="9c49aa8d79c97951c242",
        client_secret="b83838efbd8669d325fdc5b5e7ce1173aacb85a4",
        redirect_url= "",
        home_url="http://localhost:8000",
        )
    # print(tt)
    print('解析到租户最终',tenant)

    if tenant is None:
        raise TenantNotFoundOrUnActiveError()

    return tenant
async def get_tenant_current( ):
    tenant_code = request_context_manager.current().tenant_code
    tenant =await tenant_registry.get_tenant(tenant_code)

    return tenant
