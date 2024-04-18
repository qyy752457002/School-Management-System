from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.planning_school_communication import PlanningSchoolCommunication


class PlanningSchoolCommunicationDAO(DAOBase):

    async def get_planning_school_communication_by_id(self, planning_school_communication_id):
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchoolCommunication).where(PlanningSchoolCommunication.id == planning_school_communication_id))
        return result.scalar_one_or_none()

    async def add_planning_school_communication(self, planning_school_communication):
        session = await self.master_db()
        session.add(planning_school_communication)
        await session.commit()
        await session.refresh(planning_school_communication)
        return planning_school_communication

    async def update_planning_school_communication(self, planning_school_communication,ctype=1):
        session = await self.master_db()
        # session.add(planning_school_communication)
        if ctype == 1:
            update_stmt = update(PlanningSchoolCommunication).where(PlanningSchoolCommunication.id == planning_school_communication.id).values(
                planning_school_communication_no=planning_school_communication.planning_school_communication_no,
                planning_school_communication_name=planning_school_communication.planning_school_communication_name,
                block=planning_school_communication.block,
                borough=planning_school_communication.borough,
                planning_school_communication_type=planning_school_communication.planning_school_communication_type,
                planning_school_communication_operation_type=planning_school_communication.planning_school_communication_operation_type,
                planning_school_communication_operation_type_lv2=planning_school_communication.planning_school_communication_operation_type_lv2,
                planning_school_communication_operation_type_lv3=planning_school_communication.planning_school_communication_operation_type_lv3,
                planning_school_communication_org_type=planning_school_communication.planning_school_communication_org_type,
                planning_school_communication_level=planning_school_communication.planning_school_communication_level,

            )
        else:
            update_stmt = update(PlanningSchoolCommunication).where(PlanningSchoolCommunication.id == planning_school_communication.id).values(
                planning_school_communication_name=planning_school_communication.planning_school_communication_name,
                planning_school_communication_short_name=planning_school_communication.planning_school_communication_short_name,
                planning_school_communication_code=planning_school_communication.planning_school_communication_code,
                create_planning_school_communication_date=planning_school_communication.create_planning_school_communication_date,
                founder_type=planning_school_communication.founder_type,
                founder_name=planning_school_communication.founder_name,
                urban_rural_nature=planning_school_communication.urban_rural_nature,
                planning_school_communication_operation_type=planning_school_communication.planning_school_communication_operation_type,
                planning_school_communication_org_form=planning_school_communication.planning_school_communication_org_form,
                planning_school_communication_operation_type_lv2=planning_school_communication.planning_school_communication_operation_type_lv2,
                planning_school_communication_operation_type_lv3=planning_school_communication.planning_school_communication_operation_type_lv3,
                department_unit_number=planning_school_communication.department_unit_number,
                sy_zones=planning_school_communication.sy_zones,
                historical_evolution=planning_school_communication.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return planning_school_communication


    async def softdelete_planning_school_communication(self, planning_school_communication):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(PlanningSchoolCommunication).where(PlanningSchoolCommunication.id == planning_school_communication.id).values(
            deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(planning_school_communication)
        await session.commit()
        return planning_school_communication


    async def get_planning_school_communication_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(PlanningSchoolCommunication))
        return result.scalar()

    async def query_planning_school_communication_with_page(self, planning_school_communication_name, planning_school_communication_id, planning_school_communication_no,
                                              page_request: PageRequest) -> Paging:
        query = select(PlanningSchoolCommunication)
        if planning_school_communication_name:
            query = query.where(PlanningSchoolCommunication.planning_school_communication_name == planning_school_communication_name)
        if planning_school_communication_id:
            query = query.where(PlanningSchoolCommunication.id == planning_school_communication_id)
        if planning_school_communication_no:
            query = query.where(PlanningSchoolCommunication.planning_school_communication_no == planning_school_communication_no)
        paging = await self.query_page(query, page_request)
        return paging

