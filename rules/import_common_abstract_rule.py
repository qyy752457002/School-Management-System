# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from abc import ABC

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
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
from views.models.campus import Campus as CampusModel

from views.models.campus import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.planning_school_dao import PlanningSchoolDAO
from views.models.school import School as SchoolModel
from views.models.system import DISTRICT_ENUM_KEY, ID_TYPE_ENUM_KEY, CLASS_SYSTEM_ENUM_KEY


@dataclass_inject
class ImportCommonAbstractRule(ABC):
    campus_dao: CampusDAO
    p_school_dao: SchoolDAO
    id_types= {}
    class_systems= None

    async def convert_import_format_to_view_model(self, data):
        # 默认实现细节...
        print("默认实现细节...")
        pass
    async def init_enum_value(self):
        enum_value_rule = get_injector(EnumValueRule)
        self.id_types =await enum_value_rule.query_enum_values(ID_TYPE_ENUM_KEY, None,return_keys='description')
        self.class_systems =await enum_value_rule.query_enum_values(CLASS_SYSTEM_ENUM_KEY, None,return_keys='description')
        return self


