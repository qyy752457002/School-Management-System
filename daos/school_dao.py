from sqlalchemy import select, func, update, desc

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.planning_school import PlanningSchool
from models.school import School


class SchoolDAO(DAOBase):


    async def get_school_by_process_instance_id(self, process_instance_id):
        session = await self.slave_db()
        result = await session.execute(select(School).where(School.process_instance_id == process_instance_id))
        return result.scalar()

    async def get_school_by_id(self, school_id):
        session = await self.slave_db()
        result = await session.execute(select(School).where(School.id == school_id))
        return result.scalar_one_or_none()

    async def get_school_by_school_name(self, school_name):
        session = await self.slave_db()
        result = await session.execute(
            select(School).where(School.school_name == school_name))
        return result.first()

    async def add_school(self, school):
        session = await self.master_db()
        session.add(school)
        await session.commit()
        await session.refresh(school)
        return school

    async def update_school_byargs(self, school: School, *args, is_commit: bool = True):
        session =await self.master_db()
        update_contents = get_update_contents(school, *args)
        query = update(School).where(School.id == school.id).values(**update_contents)
        return await self.update(session, query, school, update_contents, is_commit=is_commit)

    async def update_school(self, school,ctype=1):
        session = await self.master_db()
        # session.add(school)
        if ctype == 1:
            update_stmt = update(School).where(School.id == school.id).values(
                school_no=school.school_no,
                school_name=school.school_name,
                block=school.block,
                borough=school.borough,
                # school_type=school.school_type,
                school_edu_level=school.school_edu_level,
                school_category=school.school_category,
                school_operation_type=school.school_operation_type,
                school_org_type=school.school_org_type,
                school_level=school.school_level,

            )
        else:
            update_stmt = update(School).where(School.id == school.id).values(
                school_name=school.school_name,
                school_short_name=school.school_short_name,
                school_code=school.school_code,
                create_school_date=school.create_school_date,
                founder_type=school.founder_type,
                founder_name=school.founder_name,
                urban_rural_nature=school.urban_rural_nature,
                school_edu_level=school.school_edu_level,
                school_org_form=school.school_org_form,
                school_category=school.school_category,
                school_operation_type=school.school_operation_type,
                department_unit_number=school.department_unit_number,
                sy_zones=school.sy_zones,
                historical_evolution=school.historical_evolution,
            )


        await session.execute(update_stmt)
        await session.commit()
        return school

    async def delete_school(self, school):
        session = self.master_db()
        return await self.delete(session, school)

    async def softdelete_school(self, school):
        session = await self.master_db()
        deleted_status= 1
        update_stmt = update(School).where(School.id == school.id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        # await session.delete(school)
        await session.commit()
        return school

    async def get_all_schools(self):
        session = await self.slave_db()
        result = await session.execute(select(School))
        return result.scalars().all()

    async def get_school_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(School))
        return result.scalar()



    async def query_school_with_page(self, page_request: PageRequest, school_name,school_no,school_code,
                                              block,school_level,borough,status,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ,planning_school_id,province,city,institution_category,social_credit_code,school_org_type) -> Paging:
        query = select(School).join(PlanningSchool, PlanningSchool.id == School.planning_school_id, isouter=True).order_by(desc(School.id))
        query = query.where(School.is_deleted == False)

        if school_org_type:
            query = query.where(School.school_org_type == school_org_type)
        if social_credit_code:
            query = query.where(School.social_credit_code == social_credit_code)
        if institution_category:
            query = query.where(School.institution_category == institution_category)
        if school_name:
            query = query.where(School.school_name == school_name)
        if planning_school_id:
            query = query.where(School.planning_school_id == planning_school_id)

        if school_no:
            query = query.where(School.school_no == school_no)
        if school_code:
            query = query.where(School.school_code == school_code)
        if block:
            query = query.where(School.block == block)
        if school_level:
            query = query.where(School.school_level == school_level)
        if borough:
            query = query.where(School.borough == borough)

        if status:
            query = query.where(School.status == status)
        if province:
            query = query.where(PlanningSchool.province == province)
        if city:
            query = query.where(PlanningSchool.city == city)

        if founder_type_lv3 and  len(founder_type_lv3)>0:
            query = query.where(School.founder_type_lv3.in_(founder_type_lv3))


        paging = await self.query_page(query, page_request)
        return paging


    async def update_school_status(self, school,status):
        session = await self.master_db()
        next_status= 1
        if status == 1:
            next_status= '正常'
        else:
            next_status= '已关闭'

        update_stmt = update(School).where(School.id == school.id).values(
            status= next_status,
        )
        await session.execute(update_stmt)
        # await session.delete(school)
        await session.commit()
        return school
