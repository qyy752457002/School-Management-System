from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.campus_eduinfo import CampusEduinfo


class CampusEduinfoDAO(DAOBase):

    async def get_campus_eduinfo_by_id(self, campus_eduinfo_id):
        session = await self.slave_db()
        result = await session.execute(select(CampusEduinfo).where(CampusEduinfo.id == campus_eduinfo_id))
        return result.scalar_one_or_none()

    async def get_campus_eduinfo_by_campus_id(self, campus_eduinfo_id):
        session = await self.slave_db()
        result = await session.execute(select(CampusEduinfo).where(CampusEduinfo.campus_id == campus_eduinfo_id))
        return result.scalar_one_or_none()

    async def add_campus_eduinfo(self, campus_eduinfo):
        session = await self.master_db()
        session.add(campus_eduinfo)
        await session.commit()
        await session.refresh(campus_eduinfo)
        return campus_eduinfo

    async def update_campus_eduinfo(self, campus_eduinfo,ctype=1):
        session = await self.master_db()
        # session.add(campus_eduinfo)
        if ctype == 1:
            update_stmt = update(CampusEduinfo).where(CampusEduinfo.id == campus_eduinfo.id).values(
                campus_eduinfo_no=campus_eduinfo.campus_eduinfo_no,
                campus_eduinfo_name=campus_eduinfo.campus_eduinfo_name,
                block=campus_eduinfo.block,
                borough=campus_eduinfo.borough,
                campus_eduinfo_type=campus_eduinfo.campus_eduinfo_type,
                campus_eduinfo_operation_type=campus_eduinfo.campus_eduinfo_operation_type,
                campus_eduinfo_operation_type_lv2=campus_eduinfo.campus_eduinfo_operation_type_lv2,
                campus_eduinfo_operation_type_lv3=campus_eduinfo.campus_eduinfo_operation_type_lv3,
                campus_eduinfo_org_type=campus_eduinfo.campus_eduinfo_org_type,
                campus_eduinfo_level=campus_eduinfo.campus_eduinfo_level,

            )
        else:
            update_stmt = update(CampusEduinfo).where(CampusEduinfo.id == campus_eduinfo.id).values(
                campus_eduinfo_name=campus_eduinfo.campus_eduinfo_name,
                campus_eduinfo_short_name=campus_eduinfo.campus_eduinfo_short_name,
                campus_eduinfo_code=campus_eduinfo.campus_eduinfo_code,
                create_campus_eduinfo_date=campus_eduinfo.create_campus_eduinfo_date,
                founder_type=campus_eduinfo.founder_type,
                founder_name=campus_eduinfo.founder_name,
                urban_rural_nature=campus_eduinfo.urban_rural_nature,
                campus_eduinfo_operation_type=campus_eduinfo.campus_eduinfo_operation_type,
                campus_eduinfo_org_form=campus_eduinfo.campus_eduinfo_org_form,
                campus_eduinfo_operation_type_lv2=campus_eduinfo.campus_eduinfo_operation_type_lv2,
                campus_eduinfo_operation_type_lv3=campus_eduinfo.campus_eduinfo_operation_type_lv3,
                department_unit_number=campus_eduinfo.department_unit_number,
                sy_zones=campus_eduinfo.sy_zones,
                historical_evolution=campus_eduinfo.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return campus_eduinfo


    async def softdelete_campus_eduinfo(self, campus_eduinfo):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(CampusEduinfo).where(CampusEduinfo.id == campus_eduinfo.id).values(
            deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(campus_eduinfo)
        await session.commit()
        return campus_eduinfo


    async def get_campus_eduinfo_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(CampusEduinfo))
        return result.scalar()

    async def query_campus_eduinfo_with_page(self, campus_eduinfo_name, campus_eduinfo_id, campus_eduinfo_no,
                                              page_request: PageRequest) -> Paging:
        query = select(CampusEduinfo)
        if campus_eduinfo_name:
            # query = query.where(CampusEduinfo.campus_eduinfo_name == campus_eduinfo_name)
            pass
        if campus_eduinfo_id:
            query = query.where(CampusEduinfo.id == campus_eduinfo_id)
        if campus_eduinfo_no:
            # query = query.where(CampusEduinfo.campus_eduinfo_no == campus_eduinfo_no)
            pass
        paging = await self.query_page(query, page_request)
        return paging

    async def update_campus_eduinfo_byargs(self, campus_eduinfo: CampusEduinfo, *args, is_commit: bool = True):
        session =await self.master_db()
        update_contents = get_update_contents(campus_eduinfo, *args)
        if campus_eduinfo.campus_id>0:
            # update_contents['planning_campus_id'] = planning_campus_eduinfo.planning_campus_id
            query = update(CampusEduinfo).where(CampusEduinfo.campus_id == campus_eduinfo.campus_id).values(**update_contents)

        else:

            query = update(CampusEduinfo).where(CampusEduinfo.id == campus_eduinfo.id).values(**update_contents)
        return await self.update(session, query, campus_eduinfo, update_contents, is_commit=is_commit)

