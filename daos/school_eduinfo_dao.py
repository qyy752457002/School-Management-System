from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.school_eduinfo import SchoolEduinfo


class SchoolEduinfoDAO(DAOBase):

    async def get_school_eduinfo_by_id(self, school_eduinfo_id):
        session = await self.slave_db()
        result = await session.execute(select(SchoolEduinfo).where(SchoolEduinfo.id == school_eduinfo_id))
        return result.scalar_one_or_none()

    async def get_school_eduinfo_by_school_id(self, school_eduinfo_id):
        session = await self.slave_db()
        result = await session.execute(select(SchoolEduinfo).where(SchoolEduinfo.school_id == school_eduinfo_id))
        return result.scalar_one_or_none()

    async def add_school_eduinfo(self, school_eduinfo):
        if hasattr(school_eduinfo, 'school_id'):
            school_eduinfo.school_id = int(school_eduinfo.school_id)
        session = await self.master_db()
        session.add(school_eduinfo)
        await session.commit()
        await session.refresh(school_eduinfo)
        return school_eduinfo

    async def update_school_eduinfo(self, school_eduinfo, ctype=1):
        session = await self.master_db()
        # session.add(school_eduinfo)
        if ctype == 1:
            update_stmt = update(SchoolEduinfo).where(SchoolEduinfo.id == school_eduinfo.id).values(
                school_eduinfo_no=school_eduinfo.school_eduinfo_no,
                school_eduinfo_name=school_eduinfo.school_eduinfo_name,
                block=school_eduinfo.block,
                borough=school_eduinfo.borough,
                school_eduinfo_type=school_eduinfo.school_eduinfo_type,
                school_eduinfo_operation_type=school_eduinfo.school_eduinfo_operation_type,
                school_eduinfo_operation_type_lv2=school_eduinfo.school_eduinfo_operation_type_lv2,
                school_eduinfo_operation_type_lv3=school_eduinfo.school_eduinfo_operation_type_lv3,
                school_eduinfo_org_type=school_eduinfo.school_eduinfo_org_type,
                school_eduinfo_level=school_eduinfo.school_eduinfo_level,

            )
        else:
            update_stmt = update(SchoolEduinfo).where(SchoolEduinfo.id == school_eduinfo.id).values(
                school_eduinfo_name=school_eduinfo.school_eduinfo_name,
                school_eduinfo_short_name=school_eduinfo.school_eduinfo_short_name,
                school_eduinfo_code=school_eduinfo.school_eduinfo_code,
                create_school_eduinfo_date=school_eduinfo.create_school_eduinfo_date,
                founder_type=school_eduinfo.founder_type,
                founder_name=school_eduinfo.founder_name,
                urban_rural_nature=school_eduinfo.urban_rural_nature,
                school_eduinfo_operation_type=school_eduinfo.school_eduinfo_operation_type,
                school_eduinfo_org_form=school_eduinfo.school_eduinfo_org_form,
                school_eduinfo_operation_type_lv2=school_eduinfo.school_eduinfo_operation_type_lv2,
                school_eduinfo_operation_type_lv3=school_eduinfo.school_eduinfo_operation_type_lv3,
                department_unit_number=school_eduinfo.department_unit_number,
                sy_zones=school_eduinfo.sy_zones,
                historical_evolution=school_eduinfo.historical_evolution,
            )

        await session.execute(update_stmt)
        await session.commit()
        return school_eduinfo

    async def softdelete_school_eduinfo(self, school_eduinfo):
        session = await self.master_db()
        deleted_status = 1
        update_stmt = update(SchoolEduinfo).where(SchoolEduinfo.id == school_eduinfo.id).values(
            deleted=deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(school_eduinfo)
        await session.commit()
        return school_eduinfo

    async def get_school_eduinfo_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(SchoolEduinfo))
        return result.scalar()

    async def query_school_eduinfo_with_page(self, school_eduinfo_name, school_eduinfo_id, school_eduinfo_no,
                                             page_request: PageRequest) -> Paging:
        query = select(SchoolEduinfo)
        if school_eduinfo_name:
            # query = query.where(SchoolEduinfo.school_eduinfo_name == school_eduinfo_name)
            pass
        if school_eduinfo_id:
            query = query.where(SchoolEduinfo.id == school_eduinfo_id)
        if school_eduinfo_no:
            # query = query.where(SchoolEduinfo.school_eduinfo_no == school_eduinfo_no)
            pass
        paging = await self.query_page(query, page_request)
        return paging

    async def update_school_eduinfo_byargs(self, school_eduinfo: SchoolEduinfo, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(school_eduinfo, *args)
        if school_eduinfo.school_id > 0:
            # update_contents['planning_school_id'] = planning_school_eduinfo.planning_school_id
            query = update(SchoolEduinfo).where(SchoolEduinfo.school_id == school_eduinfo.school_id).values(
                **update_contents)

        else:

            query = update(SchoolEduinfo).where(SchoolEduinfo.id == school_eduinfo.id).values(**update_contents)
        return await self.update(session, query, school_eduinfo, update_contents, is_commit=is_commit)
