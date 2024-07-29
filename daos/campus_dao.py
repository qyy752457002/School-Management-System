from sqlalchemy import select, func, update, desc

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.campus import Campus


class CampusDAO(DAOBase):

    async def get_campus_by_id(self, campus_id):
        session = await self.slave_db()
        campus_id = int(campus_id)
        result = await session.execute(select(Campus).where(Campus.id == campus_id))
        return result.scalar_one_or_none()

    async def get_campus_by_campus_name(self, campus_name):
        session = await self.slave_db()
        result = await session.execute(
            select(Campus).where(Campus.campus_name == campus_name))
        return result.first()

    async def add_campus(self, campus):
        session = await self.master_db()
        session.add(campus)
        await session.commit()
        await session.refresh(campus)
        return campus

    async def update_campus_byargs(self, campus: Campus, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(campus, *args)
        query = update(Campus).where(Campus.id == campus.id).values(**update_contents)
        return await self.update(session, query, campus, update_contents, is_commit=is_commit)

    async def update_campus(self, campus, ctype=1):
        session = await self.master_db()
        # session.add(campus)
        if ctype == 1:
            update_stmt = update(Campus).where(Campus.id == campus.id).values(
                campus_no=campus.campus_no,
                campus_name=campus.campus_name,
                block=campus.block,
                borough=campus.borough,
                campus_type=campus.campus_type,
                campus_operation_type=campus.campus_operation_type,
                campus_operation_type_lv2=campus.campus_operation_type_lv2,
                campus_operation_type_lv3=campus.campus_operation_type_lv3,
                campus_org_type=campus.campus_org_type,
                campus_level=campus.campus_level,

            )
        else:
            update_stmt = update(Campus).where(Campus.id == campus.id).values(
                campus_name=campus.campus_name,
                campus_short_name=campus.campus_short_name,
                campus_code=campus.campus_code,
                create_campus_date=campus.create_campus_date,
                founder_type=campus.founder_type,
                founder_name=campus.founder_name,
                urban_rural_nature=campus.urban_rural_nature,
                campus_operation_type=campus.campus_operation_type,
                campus_org_form=campus.campus_org_form,
                campus_operation_type_lv2=campus.campus_operation_type_lv2,
                campus_operation_type_lv3=campus.campus_operation_type_lv3,
                department_unit_number=campus.department_unit_number,
                sy_zones=campus.sy_zones,
                historical_evolution=campus.historical_evolution,
            )

        await session.execute(update_stmt)
        await session.commit()
        return campus

    async def delete_campus(self, campus):
        session = self.master_db()
        return await self.delete(session, campus)

    async def softdelete_campus(self, campus):
        session = await self.master_db()
        campus.id = int(campus.id)
        deleted_status = 1
        update_stmt = update(Campus).where(Campus.id == campus.id).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(campus)
        await session.commit()
        return campus

    async def get_all_campuss(self):
        session = await self.slave_db()
        result = await session.execute(select(Campus))
        return result.scalars().all()

    async def get_campus_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Campus))
        return result.scalar()

    async def query_campus_with_page(self, page_request: PageRequest, campus_name, campus_no, campus_code,
                                     block, campus_level, borough, status, founder_type,
                                     founder_type_lv2,
                                     founder_type_lv3, school_id) -> Paging:
        query = select(Campus).order_by(desc(Campus.id))
        query = query.where(Campus.is_deleted == False)

        if campus_name:
            query = query.where(Campus.campus_name == campus_name)
        if school_id:
            query = query.where(Campus.school_id == school_id)

        if campus_no:
            query = query.where(Campus.campus_no == campus_no)
        if campus_code:
            query = query.where(Campus.campus_code == campus_code)
        if block:
            query = query.where(Campus.block == block)
        if campus_level:
            query = query.where(Campus.campus_level == campus_level)
        if borough:
            query = query.where(Campus.borough == borough)

        if status:
            query = query.where(Campus.status == status)

        if len(founder_type_lv3) > 0:
            query = query.where(Campus.founder_type_lv3.in_(founder_type_lv3))

        paging = await self.query_page(query, page_request)
        return paging

    async def update_campus_status(self, campus, status):
        session = await self.master_db()
        next_status = 1
        if status == 1:
            next_status = '正常'
        else:
            next_status = '已关闭'

        update_stmt = update(Campus).where(Campus.id == campus.id).values(
            status=next_status,
        )
        await session.execute(update_stmt)
        # await session.delete(campus)
        await session.commit()
        return campus
