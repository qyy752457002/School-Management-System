import datetime

from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from daos import enum_value_dao
from daos.enum_value_dao import EnumValueDAO
from views.common.constant import Constant
from views.models.extend_params import ExtendParams
from views.models.grades import Grades

from fastapi import Query, Depends, Body
from sqlalchemy import select
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.grade import Grade
from rules.grade_rule import GradeRule
from views.models.grades import Grades
from id_validator import validator

from views.models.system import UnitType


def compare_modify_fields( planning_school,orm_model):
    """
    比较两个对象  返回需要更新的字段
    :param planning_school:
    :param orm_model:
    :return:
    """
    # print(1111111,planning_school,222222222,orm_model,33333333)
    changeitems = dict()
    for key, value in planning_school.__dict__.items():
        if value:
            if key in orm_model.__dict__ and orm_model.__dict__[key] != value:
                print(key,value,orm_model.__dict__[key])
                # changeitems.append(key)
                changeitems[key] = [ orm_model.__dict__[key],value ]
                # pass
    print(changeitems)
    #
    # # 创建类的实例
    # planning_school_key_info = PlanningSchoolKeyInfo()
    # print(planning_school_key_info.__fields__)
    #
    # # 提取每个属性里 title 后面的值
    # titles = {attr: planning_school_key_info.__fields__[attr].title for attr in planning_school_key_info.__fields__}
    #
    # print(titles)

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
    obj= None
    if 'Extendparams'  in headers:
        extparam= headers['Extendparams']
        if isinstance(extparam, str):
            extparam = eval(extparam)
        obj = ExtendParams(**extparam)
        if obj.unit_type == UnitType.CITY.value:
            obj.city = Constant.CURRENT_CITY
        # if obj.unit_type == UnitType.COUNTRY.value:
        #     obj.county_id = Constant.CURRENT_CITY
        if obj.county_id:
            # 区的转换   or todo
            enuminfo = await (  EnumValueDAO()).get_enum_value_by_value(obj.county_id, 'country' )
            if enuminfo:
                obj.county_name = enuminfo.description


    return obj
