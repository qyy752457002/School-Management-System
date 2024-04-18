from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.school_communication import SchoolCommunication


class SchoolCommunicationDAO(DAOBase):

    async def get_school_communication_by_id(self, school_communication_id):
        session = await self.slave_db()
        result = await session.execute(select(SchoolCommunication).where(SchoolCommunication.id == school_communication_id))
        return result.scalar_one_or_none()

    async def add_school_communication(self, school_communication):
        session = await self.master_db()
        session.add(school_communication)
        await session.commit()
        await session.refresh(school_communication)
        return school_communication

    async def update_school_communication(self, school_communication,ctype=1):
        session = await self.master_db()
        # session.add(school_communication)
        if ctype == 1:
            update_stmt = update(SchoolCommunication).where(SchoolCommunication.id == school_communication.id).values(
                school_communication_no=school_communication.school_communication_no,
                school_communication_name=school_communication.school_communication_name,
                block=school_communication.block,
                borough=school_communication.borough,
                school_communication_type=school_communication.school_communication_type,
                school_communication_operation_type=school_communication.school_communication_operation_type,
                school_communication_operation_type_lv2=school_communication.school_communication_operation_type_lv2,
                school_communication_operation_type_lv3=school_communication.school_communication_operation_type_lv3,
                school_communication_org_type=school_communication.school_communication_org_type,
                school_communication_level=school_communication.school_communication_level,

            )
        else:
            update_stmt = update(SchoolCommunication).where(SchoolCommunication.id == school_communication.id).values(
                school_communication_name=school_communication.school_communication_name,
                school_communication_short_name=school_communication.school_communication_short_name,
                school_communication_code=school_communication.school_communication_code,
                create_school_communication_date=school_communication.create_school_communication_date,
                founder_type=school_communication.founder_type,
                founder_name=school_communication.founder_name,
                urban_rural_nature=school_communication.urban_rural_nature,
                school_communication_operation_type=school_communication.school_communication_operation_type,
                school_communication_org_form=school_communication.school_communication_org_form,
                school_communication_operation_type_lv2=school_communication.school_communication_operation_type_lv2,
                school_communication_operation_type_lv3=school_communication.school_communication_operation_type_lv3,
                department_unit_number=school_communication.department_unit_number,
                sy_zones=school_communication.sy_zones,
                historical_evolution=school_communication.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return school_communication


    async def softdelete_school_communication(self, school_communication):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(SchoolCommunication).where(SchoolCommunication.id == school_communication.id).values(
            deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(school_communication)
        await session.commit()
        return school_communication


    async def get_school_communication_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(SchoolCommunication))
        return result.scalar()

    async def query_school_communication_with_page(self, school_communication_name, school_communication_id, school_communication_no,
                                              page_request: PageRequest) -> Paging:
        query = select(SchoolCommunication)
        if school_communication_name:
            pass
            # query = query.where(SchoolCommunication.school_communication_name == school_communication_name)

        if school_communication_id:
            query = query.where(SchoolCommunication.id == school_communication_id)
        if school_communication_no:
            pass
            # query = query.where(SchoolCommunication.school_communication_no == school_communication_no)
        paging = await self.query_page(query, page_request)
        return paging

