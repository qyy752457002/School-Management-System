from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.major import Major


class MajorDAO(DAOBase):

    async def add_major(self, major: Major):
        session = await self.master_db()
        if major.school_id:
            major.school_id = int(major.school_id)
        session.add(major)
        await session.commit()
        await session.refresh(major)
        return major

    async def get_major_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Major))
        return result.scalar()

    async def delete_major(self, major: Major):
        session = await self.master_db()
        await session.delete(major)
        await session.commit()

    async def softdelete_major(self, major):
        session = await self.master_db()
        deleted_status = True
        update_stmt = update(Major).where(Major.id == int(major.id)).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return major

    async def softdelete_major_by_school_id(self, school_id):
        session = await self.master_db()
        deleted_status = True
        update_stmt = update(Major).where(Major.school_id == int(school_id)).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return school_id

    async def get_major_by_id(self, id):
        session = await self.slave_db()
        result = await session.execute(select(Major).where(Major.id == int(id)))
        return result.scalar_one_or_none()

    async def get_major_by_school_id(self, id):
        session = await self.slave_db()
        result = await session.execute(select(Major).where(Major.school_id == int(id)).where(Major.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_major_by_name(self, name, major=None):
        session = await self.slave_db()
        query = select(Major).where(Major.major_name == name)
        if major:
            if major.school_id:
                query = query.where(Major.school_id == major.school_id)
        # query = query.where(Major.id != major.id)

        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def query_major_with_page(self, page_request: PageRequest, **kwargs, ):
        query = select(Major)
        for key, value in kwargs.items():
            query = query.where(getattr(Major, key) == value)
        paging = await self.query_page(query, page_request)
        return paging

    async def query_major_with_page_param(self, page_request: PageRequest, school_id):
        query = select(Major).where(Major.school_id == int(school_id), Major.is_deleted == False)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_major(self, major, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(major, *args)
        query = update(Major).where(Major.id == major.id).values(**update_contents)
        return await self.update(session, query, major, update_contents, is_commit=is_commit)
