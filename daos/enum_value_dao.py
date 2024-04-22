from sqlalchemy import select, func

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.enum_value import EnumValue


class EnumValueDAO(DAOBase):

    async def get_enum_value_by_id(self, enum_value_id):
        session = await self.slave_db()
        result = await session.execute(select(EnumValue).where(EnumValue.id == enum_value_id))
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

    async def query_enum_value_with_page(self, enum_value_name,id, page_request: PageRequest) -> Paging:
        query = select(EnumValue)
        if enum_value_name:
            query = query.where(EnumValue.enum_name == enum_value_name)
        if id:
            query = query.where(EnumValue.id == id)
        paging = await self.query_page(query, page_request)
        return paging
