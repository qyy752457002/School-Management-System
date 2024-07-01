from datetime import date, datetime

from fastapi.params import Query
from mini_framework.design_patterns.singleton import singleton
from daos.enum_value_dao import EnumValueDAO
from views.common.constant import Constant
from views.models.extend_params import ExtendParams

from id_validator import validator

from views.models.system import UnitType


def compare_modify_fields( view_model,orm_model):
    """
    比较两个对象  返回需要更新的字段
    :param view_model:
    :param orm_model:
    :return:
    """
    changeitems = dict()
    # 使用视图模型
    vd = view_model.__dict__
    od = orm_model.__dict__
    vd = convert_dates_to_strings(vd)
    od = convert_dates_to_strings(od)
    for key, value in vd.items():
        if value:
            if key in od  and od[key] != value:
                print(key,value,od[key])
                # changeitems.append(key)
                key_cn=''
                if key in view_model.model_fields.keys():
                    key_cn = view_model.model_fields[key].title
                    if not key_cn:
                        key_cn =view_model.model_fields[key].description
                if not key_cn and  key in orm_model.model_fields.keys():
                    key_cn = orm_model.model_fields[key].title
                    if not key_cn:
                        key_cn =orm_model.model_fields[key].description

                valueold= od[key]
                if isinstance(valueold,date):
                    valueold=valueold.strftime('%Y-%m-%d')
                if isinstance(value,date):
                    value=value.strftime('%Y-%m-%d')
                changeitems[key_cn] ={"before":  valueold,"after":value }
                # pass
    print('比叫变更域',changeitems)
    return changeitems

def page_none_deal( paging):
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
async def get_extend_params(request):
    headers = request.headers
    obj = ExtendParams()

    if 'Extendparams'  in headers:
        extparam= headers['Extendparams']
        if isinstance(extparam, str):
            extparam = eval(extparam)
        obj = ExtendParams(**extparam)
        if obj.unit_type == UnitType.CITY.value:
            obj.city = Constant.CURRENT_CITY

        if obj.county_id:
            # 区的转换   or todo
            enuminfo = await (  EnumValueDAO()).get_enum_value_by_value(obj.county_id, 'country' )
            if enuminfo:
                obj.county_name = enuminfo.description
    print('Extendparams', obj)


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
        self.workflow_config =  workflow_service_dict



workflow_service_config = WorkflowServiceConfig()



def convert_dates_to_strings(stuinfoadddict):
    for key, value in stuinfoadddict.items():
        if isinstance(value, (date, datetime)):
            stuinfoadddict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(value,Query) or isinstance(value,tuple):
            stuinfoadddict[key] = None
    return stuinfoadddict