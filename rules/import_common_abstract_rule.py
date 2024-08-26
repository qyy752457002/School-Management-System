# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from abc import ABC

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector

from daos.campus_dao import CampusDAO
from daos.school_dao import SchoolDAO
from rules.enum_value_rule import EnumValueRule
from views.models.system import ID_TYPE_ENUM_KEY, CLASS_SYSTEM_ENUM_KEY, ENROLLMENT_METHOD_ENUM_KEY


@dataclass_inject
class ImportCommonAbstractRule(ABC):
    campus_dao: CampusDAO
    p_school_dao: SchoolDAO
    id_types= {}
    class_systems= None
    enrollment_methods= {}

    async def convert_import_format_to_view_model(self, data):
        # 默认实现细节...
        print("默认实现细节...")
        pass
    async def init_enum_value(self):
        enum_value_rule = get_injector(EnumValueRule)
        self.id_types =await enum_value_rule.query_enum_values(ID_TYPE_ENUM_KEY, None,return_keys='description')
        self.class_systems =await enum_value_rule.query_enum_values(CLASS_SYSTEM_ENUM_KEY, None,return_keys='description')
        self.enrollment_methods =await enum_value_rule.query_enum_values(ENROLLMENT_METHOD_ENUM_KEY, None,return_keys='description')
        return self


