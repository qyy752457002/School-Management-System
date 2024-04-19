from typing import List

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select
from business_exceptions.enum_value import EnumValueNotFoundError
from daos.enum_value_dao import EnumValueDAO
from models.enum_value import EnumValue
from views.models.enum_value import EnumValue as EnumValueModel
from mini_framework.databases.conn_managers.db_manager import db_connection_manager

@dataclass_inject
class EnumValueRule(object):
    enum_value_dao: EnumValueDAO

    async def get_enum_value_by_id(self, enum_value_id):
        enum_value_db = await self.enum_value_dao.get_enum_value_by_id(enum_value_id)
        if not enum_value_db:
            raise EnumValueNotFoundError()
        # 可选 , exclude=[""]
        enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel)
        return enum_value

    async def get_enum_value_by_enum_value_name(self, enum_value_name):
        enum_value_db = await self.enum_value_dao.get_enum_value_by_enum_value_name(
            enum_value_name)
        enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=[""])
        return enum_value

    async def add_enum_value(self, enum_value: EnumValueModel):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_enum_value_name(
            enum_value.enum_value_name)
        if exists_enum_value:
            raise Exception(f"枚举值{enum_value.enum_value_name}已存在")
        enum_value_db = view_model_to_orm_model(enum_value, EnumValue,    exclude=["id"])
        # enum_value_db.status =  EnumValueStatus.DRAFT.value
        enum_value_db.created_uid = 0
        enum_value_db.updated_uid = 0

        enum_value_db = await self.enum_value_dao.add_enum_value(enum_value_db)
        enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=["created_at",'updated_at'])
        return enum_value

    async def update_enum_value(self, enum_value,ctype=1):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_id(enum_value.id)
        if not exists_enum_value:
            raise EnumValueNotFoundError()
        if ctype==1:
            enum_value_db = EnumValue()
            enum_value_db.id = enum_value.id
            enum_value_db.enum_value_no = enum_value.enum_value_no
            enum_value_db.enum_value_name = enum_value.enum_value_name
            enum_value_db.block = enum_value.block
            enum_value_db.borough = enum_value.borough
            enum_value_db.enum_value_type = enum_value.enum_value_type
            enum_value_db.enum_value_operation_type = enum_value.enum_value_operation_type
            enum_value_db.enum_value_operation_type_lv2 = enum_value.enum_value_operation_type_lv2
            enum_value_db.enum_value_operation_type_lv3 = enum_value.enum_value_operation_type_lv3
            enum_value_db.enum_value_org_type = enum_value.enum_value_org_type
            enum_value_db.enum_value_level = enum_value.enum_value_level
        else:
            enum_value_db = EnumValue()
            enum_value_db.id = enum_value.id
            enum_value_db.enum_value_name=enum_value.enum_value_name
            enum_value_db.enum_value_short_name=enum_value.enum_value_short_name
            enum_value_db.enum_value_code=enum_value.enum_value_code
            enum_value_db.create_enum_value_date=enum_value.create_enum_value_date
            enum_value_db.founder_type=enum_value.founder_type
            enum_value_db.founder_name=enum_value.founder_name
            enum_value_db.urban_rural_nature=enum_value.urban_rural_nature
            enum_value_db.enum_value_operation_type=enum_value.enum_value_operation_type
            enum_value_db.enum_value_org_form=enum_value.enum_value_org_form
            enum_value_db.enum_value_operation_type_lv2=enum_value.enum_value_operation_type_lv2
            enum_value_db.enum_value_operation_type_lv3=enum_value.enum_value_operation_type_lv3
            enum_value_db.department_unit_number=enum_value.department_unit_number
            enum_value_db.sy_zones=enum_value.sy_zones
            enum_value_db.historical_evolution=enum_value.historical_evolution


        enum_value_db = await self.enum_value_dao.update_enum_value(enum_value_db)
        # 更新不用转换   因为得到的对象不熟全属性
        # enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=[""])
        return enum_value_db

    async def delete_enum_value(self, enum_value_id):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_id(enum_value_id)
        if not exists_enum_value:
            raise EnumValueNotFoundError()
        enum_value_db = await self.enum_value_dao.delete_enum_value(exists_enum_value)
        enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=[""],)
        return enum_value

    async def softdelete_enum_value(self, enum_value_id):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_id(enum_value_id)
        if not exists_enum_value:
            raise EnumValueNotFoundError()
        enum_value_db = await self.enum_value_dao.softdelete_enum_value(exists_enum_value)
        # enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=[""],)
        return enum_value_db

    async def get_all_enum_values(self):
        return await self.enum_value_dao.get_all_enum_values()

    async def get_enum_value_count(self):
        return await self.enum_value_dao.get_enum_value_count()

    async def query_enum_value_with_page(self, page_request: PageRequest,  enum_value_name,enum_value_no,enum_value_code,
                                              block,enum_value_level,borough,status ,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ):
        paging = await self.enum_value_dao.query_enum_value_with_page(  page_request, enum_value_name,enum_value_no,enum_value_code,
                                                                                  block,enum_value_level,borough,status,founder_type,
                                                                                  founder_type_lv2,
                                                                                  founder_type_lv3 )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, EnumValueModel)
        return paging_result


    async def update_enum_value_status(self, enum_value_id, status):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_id(enum_value_id)
        if not exists_enum_value:
            raise EnumValueNotFoundError()


        need_update_list = []
        need_update_list.append('status')

        print(exists_enum_value.status,2222222)
        enum_value_db = await self.enum_value_dao.update_enum_value_byargs(exists_enum_value,*need_update_list)
        # enum_value = orm_model_to_view_model(enum_value_db, EnumValueModel, exclude=[""],)
        return enum_value_db

    async def update_enum_value_byargs(self, enum_value,ctype=1):
        exists_enum_value = await self.enum_value_dao.get_enum_value_by_id(enum_value.id)
        if not exists_enum_value:
            raise EnumValueNotFoundError()
        need_update_list = []
        for key, value in enum_value.dict().items():
            if value:
                need_update_list.append(key)


        enum_value_db = await self.enum_value_dao.update_enum_value_byargs(enum_value, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # enum_value = orm_model_to_view_model(enum_value_db, SchoolModel, exclude=[""])
        return enum_value_db


    async def query_enum_values(self,enum_value_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(EnumValue).where(EnumValue.enum_value_name.like(f'{enum_value_name}%') ))
        res= result.scalars().all()
        lst = []
        for row in res:
            enum_value = orm_model_to_view_model(row, EnumValueModel)
            lst.append(enum_value)
        return lst

    async def get_next_level_enum_values(self,enum_value_name,enum_values:List[str]):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(
            select(EnumValue).where(EnumValue.enum_value.in_( enum_values ) ) .where(EnumValue.enum_name== enum_value_name )
        )

        res= result.scalars().all()
        lst = []
        for row in res:
            enum_value = orm_model_to_view_model(row, EnumValueModel,exclude=["sort_number"])
            lst.append(enum_value)
        return lst
