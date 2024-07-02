from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

# from models.institution import Institution
from models.institution import Institution

class InstitutionDAO(DAOBase):


    async def get_institution_by_process_instance_id(self, process_instance_id):
        session = await self.slave_db()
        result = await session.execute(select(Institution).where(Institution.process_instance_id == process_instance_id))
        return result.scalar()
    async def get_institution_by_id(self, institution_id):
        session = await self.slave_db()
        result = await session.execute(select(Institution).where(Institution.id == institution_id))
        return result.scalar_one_or_none()

    async def add_institution(self, institution):
        session = await self.master_db()
        session.add(institution)
        await session.commit()
        await session.refresh(institution)
        return institution

    async def update_institution(self, institution,ctype=1):
        session = await self.master_db()
        # session.add(institution)
        if ctype == 1:
            update_stmt = update(Institution).where(Institution.id == institution.id).values(
                institution_no=institution.institution_no,
                institution_name=institution.institution_name,
                block=institution.block,
                borough=institution.borough,
                institution_type=institution.institution_type,
                institution_operation_type=institution.institution_operation_type,
                institution_operation_type_lv2=institution.institution_operation_type_lv2,
                institution_operation_type_lv3=institution.institution_operation_type_lv3,
                institution_org_type=institution.institution_org_type,
                institution_level=institution.institution_level,

            )
        else:
            update_stmt = update(Institution).where(Institution.id == institution.id).values(
                institution_name=institution.institution_name,
                institution_short_name=institution.institution_short_name,
                institution_code=institution.institution_code,
                create_institutiondate=institution.create_institutiondate,
                founder_type=institution.founder_type,
                founder_name=institution.founder_name,
                urban_rural_nature=institution.urban_rural_nature,
                institution_operation_type=institution.institution_operation_type,
                institution_org_form=institution.institution_org_form,
                institution_operation_type_lv2=institution.institution_operation_type_lv2,
                institution_operation_type_lv3=institution.institution_operation_type_lv3,
                department_unit_number=institution.department_unit_number,
                sy_zones=institution.sy_zones,
                historical_evolution=institution.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return institution


    async def softdelete_institution(self, institution):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(Institution).where(Institution.id == institution.id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(institution)
        await session.commit()
        return institution


    async def get_institution_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Institution))
        return result.scalar()

    async def query_institution_with_page(self, institution_name, institution_id, institution_no,
                                              page_request: PageRequest,institution_category=None,institution_org_type=None,block=None,borough=None,social_credit_code=None) -> Paging:
        query = select(Institution)
        if block:
            query = query.where(Institution.block == block)
        if borough:
            query = query.where(Institution.borough == borough)
        if social_credit_code:
            query = query.where(Institution.social_credit_code == social_credit_code)
        if institution_org_type:
            query = query.where(Institution.institution_type == institution_org_type)

        if institution_category:
            query = query.where(Institution.institution_category == institution_category.value)
        if institution_name:
            query = query.where(Institution.institution_name == institution_name)
        if institution_id:
            query = query.where(Institution.id == institution_id)
        if institution_no:
            query = query.where(Institution.institution_no == institution_no)
        paging = await self.query_page(query, page_request)
        return paging


    async def update_institution_byargs(self, school: Institution, *args, is_commit: bool = True):
        session =await self.master_db()
        update_contents = get_update_contents(school, *args)
        query = update(Institution).where(Institution.id == school.id).values(**update_contents)
        return await self.update(session, query, school, update_contents, is_commit=is_commit)
