from sqlalchemy import select, func, or_, asc

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.enum_value import EnumValue


class EnumValueDAO(DAOBase):

    async def get_enum_value_by_id(self, enum_value_id):
        session = await self.slave_db()
        result = await session.execute(select(EnumValue).where(EnumValue.id == enum_value_id))
        return result.scalar_one_or_none()

    async def get_enum_value_by_value(self, enum_value,enum_name=None):
        session = await self.slave_db()
        query = select(EnumValue).where(EnumValue.enum_value == enum_value)
        if enum_name:
            query = query.where(EnumValue.enum_name == enum_name)
        result = await session.execute( query)
        return result.scalar_one_or_none()

    async def get_enum_value_by_enum_value_name(self, enum_value_name):
        session = await self.slave_db()
        result = await session.execute(select(EnumValue).where(EnumValue.enum_name == enum_value_name))
        return result.first()

    async def add_enum_value(self, enum_value):
        session = await self.master_db()
        session.add(enum_value)
        await session.commit()
        await session.refresh(enum_value)
        return enum_value

    async def update_enum_value(self, enum_value):
        session = await self.master_db()
        session.add(enum_value)
        await session.commit()
        return enum_value

    async def delete_enum_value(self, enum_value):
        session = await self.master_db()
        await session.delete(enum_value)
        await session.commit()
        return enum_value

    async def get_all_enum_values(self):
        session = await self.slave_db()
        result = await session.execute(select(EnumValue))
        return result.scalars().all()

    async def get_enum_value_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(EnumValue))
        return result.scalar()

    async def query_enum_value_with_page(self, page_request: PageRequest, enum_value_name, parent_code) -> Paging:
        query = select(EnumValue).order_by(asc(EnumValue.sort_number)).order_by(asc(EnumValue.id))
        if enum_value_name:
            if ',' in enum_value_name:
                enum_value_name = enum_value_name.split(',')
                if isinstance(enum_value_name, list):
                    query = query.where(EnumValue.enum_name.in_(enum_value_name))
            else:
                query = query.where(EnumValue.enum_name == enum_value_name)

        if parent_code:
            if ',' in parent_code:
                parent_code = parent_code.split(',')

            if isinstance(parent_code, list):
                # print(f"{var} 是一个列表")
                query = query.where(EnumValue.parent_id.in_(parent_code))

            else:
                # print(f"{var} 不是一个列表")
                if len(parent_code) > 0:
                    query = query.where(EnumValue.parent_id == parent_code)

        paging = await self.query_page(query, page_request)
        return paging

    async def get_enum_value_all(self, filterdict):
        session = await self.slave_db()
        temodel = select(EnumValue)
        if filterdict:
            for key, value in filterdict.items():
                temodel = temodel.where(getattr(EnumValue, key) == value)
            # result = await session.execute(select(EnumValue).where(getattr(EnumValue, key) == value))
            # return result.scalars().all()
        result = await session.execute(temodel)
        return result.scalars().all()
