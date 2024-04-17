from sqlalchemy import select, func

from mini_framework.databases.entities.dao_base import DAOBase
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
        result = await session.execute(select(PlanningSchool).where(PlanningSchool.planning_school_name == planning_school_name))
        return result.first()

    async def add_planning_school(self, grade):
        session = await self.master_db()
        session.add(grade)
        await session.commit()
        await session.refresh(grade)
        return grade

    async def update_planning_school(self, grade):
        session = await self.master_db()
        session.add(grade)
        await session.commit()
        return grade

    async def delete_planning_school(self, grade):
        session = await self.master_db()
        await session.delete(grade)
        await session.commit()
        return grade

    async def get_all_planning_schools(self):
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchool))
        return result.scalars().all()

    async def get_planning_school_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(PlanningSchool))
        return result.scalar()

    async def query_planning_school_with_page(self, planning_school_name,school_id, page_request: PageRequest) -> Paging:
        query = select(PlanningSchool)
        if planning_school_name:
            query = query.where(PlanningSchool.planning_school_name == planning_school_name)
        if school_id:
            query = query.where(PlanningSchool.school_id == school_id)
        paging = await self.query_page(query, page_request)
        return paging
