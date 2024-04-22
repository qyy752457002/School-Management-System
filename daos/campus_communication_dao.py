from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.campus_communication import CampusCommunication


class CampusCommunicationDAO(DAOBase):

    async def get_campus_communication_by_id(self, campus_communication_id):
        session = await self.slave_db()
        result = await session.execute(select(CampusCommunication).where(CampusCommunication.id == campus_communication_id))
        return result.scalar_one_or_none()


    async def get_campus_communication_by_campus_id(self, campus_communication_id):
        session = await self.slave_db()
        result = await session.execute(select(CampusCommunication).where(CampusCommunication.campus_id == campus_communication_id))
        return result.scalar_one_or_none()

    async def add_campus_communication(self, campus_communication):
        session = await self.master_db()
        session.add(campus_communication)
        await session.commit()
        await session.refresh(campus_communication)
        return campus_communication

    async def update_campus_communication(self, campus_communication,ctype=1):
        session = await self.master_db()
        # session.add(campus_communication)
        if ctype == 1:
            update_stmt = update(CampusCommunication).where(CampusCommunication.id == campus_communication.id).values(
                campus_communication_no=campus_communication.campus_communication_no,
                campus_communication_name=campus_communication.campus_communication_name,
                block=campus_communication.block,
                borough=campus_communication.borough,
                campus_communication_type=campus_communication.campus_communication_type,
                campus_communication_operation_type=campus_communication.campus_communication_operation_type,
                campus_communication_operation_type_lv2=campus_communication.campus_communication_operation_type_lv2,
                campus_communication_operation_type_lv3=campus_communication.campus_communication_operation_type_lv3,
                campus_communication_org_type=campus_communication.campus_communication_org_type,
                campus_communication_level=campus_communication.campus_communication_level,

            )
        else:
            update_stmt = update(CampusCommunication).where(CampusCommunication.id == campus_communication.id).values(
                campus_communication_name=campus_communication.campus_communication_name,
                campus_communication_short_name=campus_communication.campus_communication_short_name,
                campus_communication_code=campus_communication.campus_communication_code,
                create_campus_communication_date=campus_communication.create_campus_communication_date,
                founder_type=campus_communication.founder_type,
                founder_name=campus_communication.founder_name,
                urban_rural_nature=campus_communication.urban_rural_nature,
                campus_communication_operation_type=campus_communication.campus_communication_operation_type,
                campus_communication_org_form=campus_communication.campus_communication_org_form,
                campus_communication_operation_type_lv2=campus_communication.campus_communication_operation_type_lv2,
                campus_communication_operation_type_lv3=campus_communication.campus_communication_operation_type_lv3,
                department_unit_number=campus_communication.department_unit_number,
                sy_zones=campus_communication.sy_zones,
                historical_evolution=campus_communication.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return campus_communication


    async def softdelete_campus_communication(self, campus_communication):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(CampusCommunication).where(CampusCommunication.id == campus_communication.id).values(
            deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(campus_communication)
        await session.commit()
        return campus_communication


    async def get_campus_communication_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(CampusCommunication))
        return result.scalar()

    async def query_campus_communication_with_page(self, campus_communication_name, campus_communication_id, campus_communication_no,
                                              page_request: PageRequest) -> Paging:
        query = select(CampusCommunication)
        if campus_communication_name:
            pass
            # query = query.where(CampusCommunication.campus_communication_name == campus_communication_name)

        if campus_communication_id:
            query = query.where(CampusCommunication.id == campus_communication_id)
        if campus_communication_no:
            pass
            # query = query.where(CampusCommunication.campus_communication_no == campus_communication_no)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_campus_communication_byargs(self, campus_communication: CampusCommunication, *args, is_commit: bool = True):
        session =await self.master_db()
        update_contents = get_update_contents(campus_communication, *args)
        if campus_communication.campus_id>0:
            # update_contents['planning_campus_id'] = planning_campus_communication.planning_campus_id
            query = update(CampusCommunication).where(CampusCommunication.campus_id == campus_communication.campus_id).values(**update_contents)

        else:

            query = update(CampusCommunication).where(CampusCommunication.id == campus_communication.id).values(**update_contents)
        return await self.update(session, query, campus_communication, update_contents, is_commit=is_commit)

