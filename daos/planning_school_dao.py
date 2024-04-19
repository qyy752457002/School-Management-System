from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.planning_school import PlanningSchool


class PlanningSchoolDAO(DAOBase):

    async def get_planning_school_by_id(self, planning_school_id):
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchool).where(PlanningSchool.id == planning_school_id))
        return result.scalar_one_or_none()

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        session = await self.slave_db()
        result = await session.execute(
            select(PlanningSchool).where(PlanningSchool.planning_school_name == planning_school_name))
        return result.first()

    async def add_planning_school(self, planning_school):
        session = await self.master_db()
        session.add(planning_school)
        await session.commit()
        await session.refresh(planning_school)
        return planning_school

    async def update_planning_school(self, planning_school,ctype=1):
        session = await self.master_db()
        # session.add(planning_school)
        if ctype == 1:
            update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
                planning_school_no=planning_school.planning_school_no,
                planning_school_name=planning_school.planning_school_name,
                block=planning_school.block,
                borough=planning_school.borough,
                planning_school_type=planning_school.planning_school_type,
                planning_school_operation_type=planning_school.planning_school_operation_type,
                planning_school_operation_type_lv2=planning_school.planning_school_operation_type_lv2,
                planning_school_operation_type_lv3=planning_school.planning_school_operation_type_lv3,
                planning_school_org_type=planning_school.planning_school_org_type,
                planning_school_level=planning_school.planning_school_level,

            )
        else:
            update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
                planning_school_name=planning_school.planning_school_name,
                planning_school_short_name=planning_school.planning_school_short_name,
                planning_school_code=planning_school.planning_school_code,
                create_planning_school_date=planning_school.create_planning_school_date,
                founder_type=planning_school.founder_type,
                founder_name=planning_school.founder_name,
                urban_rural_nature=planning_school.urban_rural_nature,
                planning_school_operation_type=planning_school.planning_school_operation_type,
                planning_school_org_form=planning_school.planning_school_org_form,
                planning_school_operation_type_lv2=planning_school.planning_school_operation_type_lv2,
                planning_school_operation_type_lv3=planning_school.planning_school_operation_type_lv3,
                department_unit_number=planning_school.department_unit_number,
                sy_zones=planning_school.sy_zones,
                historical_evolution=planning_school.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return planning_school

    async def delete_planning_school(self, planning_school):
        session = await self.master_db()
        await session.delete(planning_school)
        await session.commit()
        return planning_school

    async def softdelete_planning_school(self, planning_school):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(planning_school)
        await session.commit()
        return planning_school

    async def get_all_planning_schools(self):
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchool))
        return result.scalars().all()

    async def get_planning_school_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(PlanningSchool))
        return result.scalar()

    async def query_planning_school_with_page(self, page_request: PageRequest, planning_school_name,planning_school_no,planning_school_code,
                                              block,planning_school_level,borough,status,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ) -> Paging:
        query = select(PlanningSchool)



        if planning_school_name:
            query = query.where(PlanningSchool.planning_school_name == planning_school_name)
        if planning_school_no:
            query = query.where(PlanningSchool.planning_school_no == planning_school_no)
        if planning_school_code:
            query = query.where(PlanningSchool.planning_school_code == planning_school_code)
        if block:
            query = query.where(PlanningSchool.block == block)
        if planning_school_level:
            query = query.where(PlanningSchool.planning_school_level == planning_school_level)
        if borough:
            query = query.where(PlanningSchool.borough == borough)

        if status:
            query = query.where(PlanningSchool.status == status)


        paging = await self.query_page(query, page_request)
        return paging

    async def update_planning_school_status(self, planning_school,status):
        session = await self.master_db()
        next_status= 1
        if status == 1:
            next_status= '正常'
        else:
            next_status= '已关闭'

        update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
            status= next_status,
        )
        await session.execute(update_stmt)
        # await session.delete(planning_school)
        await session.commit()
        return planning_school


    async def update_planning_school_byargs(self, planning_school: PlanningSchool, *args, is_commit: bool = True):
        session =await self.master_db()
        update_contents = get_update_contents(planning_school, *args)
        query = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(**update_contents)
        return await self.update(session, query, planning_school, update_contents, is_commit=is_commit)
