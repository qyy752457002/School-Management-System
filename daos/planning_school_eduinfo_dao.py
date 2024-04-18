from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.planning_school_eduinfo import PlanningSchoolEduinfo


class PlanningSchoolEduinfoDAO(DAOBase):

    async def get_planning_school_eduinfo_by_id(self, planning_school_eduinfo_id):
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchoolEduinfo).where(PlanningSchoolEduinfo.id == planning_school_eduinfo_id))
        return result.scalar_one_or_none()

    async def add_planning_school_eduinfo(self, planning_school_eduinfo):
        session = await self.master_db()
        session.add(planning_school_eduinfo)
        await session.commit()
        await session.refresh(planning_school_eduinfo)
        return planning_school_eduinfo

    async def update_planning_school_eduinfo(self, planning_school_eduinfo,ctype=1):
        session = await self.master_db()
        # session.add(planning_school_eduinfo)
        if ctype == 1:
            update_stmt = update(PlanningSchoolEduinfo).where(PlanningSchoolEduinfo.id == planning_school_eduinfo.id).values(
                planning_school_eduinfo_no=planning_school_eduinfo.planning_school_eduinfo_no,
                planning_school_eduinfo_name=planning_school_eduinfo.planning_school_eduinfo_name,
                block=planning_school_eduinfo.block,
                borough=planning_school_eduinfo.borough,
                planning_school_eduinfo_type=planning_school_eduinfo.planning_school_eduinfo_type,
                planning_school_eduinfo_operation_type=planning_school_eduinfo.planning_school_eduinfo_operation_type,
                planning_school_eduinfo_operation_type_lv2=planning_school_eduinfo.planning_school_eduinfo_operation_type_lv2,
                planning_school_eduinfo_operation_type_lv3=planning_school_eduinfo.planning_school_eduinfo_operation_type_lv3,
                planning_school_eduinfo_org_type=planning_school_eduinfo.planning_school_eduinfo_org_type,
                planning_school_eduinfo_level=planning_school_eduinfo.planning_school_eduinfo_level,

            )
        else:
            update_stmt = update(PlanningSchoolEduinfo).where(PlanningSchoolEduinfo.id == planning_school_eduinfo.id).values(
                planning_school_eduinfo_name=planning_school_eduinfo.planning_school_eduinfo_name,
                planning_school_eduinfo_short_name=planning_school_eduinfo.planning_school_eduinfo_short_name,
                planning_school_eduinfo_code=planning_school_eduinfo.planning_school_eduinfo_code,
                create_planning_school_eduinfo_date=planning_school_eduinfo.create_planning_school_eduinfo_date,
                founder_type=planning_school_eduinfo.founder_type,
                founder_name=planning_school_eduinfo.founder_name,
                urban_rural_nature=planning_school_eduinfo.urban_rural_nature,
                planning_school_eduinfo_operation_type=planning_school_eduinfo.planning_school_eduinfo_operation_type,
                planning_school_eduinfo_org_form=planning_school_eduinfo.planning_school_eduinfo_org_form,
                planning_school_eduinfo_operation_type_lv2=planning_school_eduinfo.planning_school_eduinfo_operation_type_lv2,
                planning_school_eduinfo_operation_type_lv3=planning_school_eduinfo.planning_school_eduinfo_operation_type_lv3,
                department_unit_number=planning_school_eduinfo.department_unit_number,
                sy_zones=planning_school_eduinfo.sy_zones,
                historical_evolution=planning_school_eduinfo.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return planning_school_eduinfo


    async def softdelete_planning_school_eduinfo(self, planning_school_eduinfo):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(PlanningSchoolEduinfo).where(PlanningSchoolEduinfo.id == planning_school_eduinfo.id).values(
            deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(planning_school_eduinfo)
        await session.commit()
        return planning_school_eduinfo


    async def get_planning_school_eduinfo_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(PlanningSchoolEduinfo))
        return result.scalar()

    async def query_planning_school_eduinfo_with_page(self, planning_school_eduinfo_name, planning_school_eduinfo_id, planning_school_eduinfo_no,
                                              page_request: PageRequest) -> Paging:
        query = select(PlanningSchoolEduinfo)
        if planning_school_eduinfo_name:
            query = query.where(PlanningSchoolEduinfo.planning_school_eduinfo_name == planning_school_eduinfo_name)
        if planning_school_eduinfo_id:
            query = query.where(PlanningSchoolEduinfo.id == planning_school_eduinfo_id)
        if planning_school_eduinfo_no:
            query = query.where(PlanningSchoolEduinfo.planning_school_eduinfo_no == planning_school_eduinfo_no)
        paging = await self.query_page(query, page_request)
        return paging

