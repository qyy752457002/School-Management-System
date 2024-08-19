from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select, func, update, desc

from models.planning_school import PlanningSchool
from models.planning_school_communication import PlanningSchoolCommunication
from views.models.extend_params import ExtendParams
from views.models.school_and_teacher_sync import SchoolSyncQueryModel


class PlanningSchoolDAO(DAOBase):

    async def get_planning_school_by_id(self, planning_school_id):
        planning_school_id = int(planning_school_id)
        session = await self.slave_db()
        result = await session.execute(select(PlanningSchool).where(PlanningSchool.id == planning_school_id))
        return result.scalar_one_or_none()

    async def get_planning_school_by_process_instance_id(self, planning_school_id):
        planning_school_id = int(planning_school_id)

        session = await self.slave_db()
        result = await session.execute(
            select(PlanningSchool).where(PlanningSchool.process_instance_id == planning_school_id))
        return result.scalar()

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        session = await self.slave_db()
        result = await session.execute(
            select(PlanningSchool).where(PlanningSchool.planning_school_name == planning_school_name).where(
                PlanningSchool.is_deleted == False))
        return result.first()

    async def get_planning_school_by_args(self,obj=None, **kwargs):
        """
        """
        session = await self.slave_db()
        query = select(PlanningSchool)
        for key, value in kwargs.items():
            query = query.where(getattr(PlanningSchool, key) == value)
        if obj is not None and hasattr(obj, 'id'):
            query = query.where(PlanningSchool.id != obj.id)
        result = await session.execute(query)
        return result.scalar()

    async def add_planning_school(self, planning_school):
        session = await self.master_db()
        session.add(planning_school)
        await session.commit()
        await session.refresh(planning_school)
        return planning_school

    async def update_planning_school(self, planning_school, ctype=1):
        session = await self.master_db()
        # session.add(planning_school)
        if ctype == 1:
            update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
                planning_school_no=planning_school.planning_school_no,
                planning_school_name=planning_school.planning_school_name,
                block=planning_school.block,
                borough=planning_school.borough,
                # planning_school_type=planning_school.planning_school_type,
                planning_school_edu_level=planning_school.planning_school_edu_level,
                planning_school_category=planning_school.planning_school_category,
                planning_school_operation_type=planning_school.planning_school_operation_type,
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
                planning_school_edu_level=planning_school.planning_school_edu_level,
                planning_school_org_form=planning_school.planning_school_org_form,
                planning_school_category=planning_school.planning_school_category,
                planning_school_operation_type=planning_school.planning_school_operation_type,
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
        deleted_status = 1
        update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
            is_deleted=deleted_status,
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

    async def query_planning_school_with_page(self, page_request: PageRequest, planning_school_name, planning_school_no,
                                              planning_school_code,
                                              block, planning_school_level, borough, status, founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3, extend_params: ExtendParams = None) -> Paging:
        query = select(PlanningSchool).where(PlanningSchool.is_deleted == False).order_by(desc(PlanningSchool.id))
        if extend_params is not None and len(block) == 0 and len(borough) == 0:
            if extend_params.county_id:
                block = extend_params.county_id
                # query = query.where(PlanningSchool.city == extend_params.city)
            pass

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

        if len(founder_type_lv3) > 0:
            query = query.where(PlanningSchool.founder_type_lv3.in_(founder_type_lv3))

        paging = await self.query_page(query, page_request)
        return paging

    async def update_planning_school_status(self, planning_school, status):
        session = await self.master_db()
        next_status = 1
        if status == 1:
            next_status = '正常'
        else:
            next_status = '已关闭'

        update_stmt = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(
            status=next_status,
        )
        await session.execute(update_stmt)
        # await session.delete(planning_school)
        await session.commit()
        return planning_school

    async def update_planning_school_byargs(self, planning_school: PlanningSchool, *args, is_commit: bool = True):
        planning_school.id = int(planning_school.id)
        if hasattr(planning_school, 'process_instance_id') and planning_school.process_instance_id:
            planning_school.process_instance_id = int(planning_school.process_instance_id)
        session = await self.master_db()
        update_contents = get_update_contents(planning_school, *args)
        # id unset
        if 'id' in update_contents.keys():
            update_contents.pop('id')
        query = update(PlanningSchool).where(PlanningSchool.id == planning_school.id).values(**update_contents)
        # 这里会
        return await self.update(session, query, planning_school, update_contents, is_commit=is_commit)

    async def query_sync_planning_school_with_page(self, query_model: SchoolSyncQueryModel,
                                                   page_request: PageRequest) -> Paging:
        query_campus = select(PlanningSchool.planning_school_no.label("school_no"), PlanningSchool.social_credit_code,
                              PlanningSchool.planning_school_name.label("school_name"),
                              PlanningSchool.borough,
                              PlanningSchool.block, PlanningSchool.founder_type, PlanningSchool.founder_type_lv2,
                              PlanningSchool.founder_type_lv3).where(
            PlanningSchool.is_deleted == False, PlanningSchool.status == "normal")
        if query_model.social_credit_code:
            query_campus = query_campus.where(PlanningSchool.social_credit_code == query_model.social_credit_code)
        if query_model.school_name:
            query_campus = query_campus.where(
                PlanningSchool.planning_school_name.label("school_name").like(f"%{query_model.school_name}%"))
        if query_model.borough:
            query_campus = query_campus.where(PlanningSchool.borough == query_model.borough)
        if query_model.block:
            query_campus = query_campus.where(PlanningSchool.block == query_model.block)
        if query_model.school_edu_level:
            query_campus = query_campus.where(PlanningSchool.planning_school_edu_level == query_model.school_edu_level)
        if query_model.school_category:
            query_campus = query_campus.where(PlanningSchool.planning_school_category == query_model.school_category)
        if query_model.school_operation_type:
            query_campus = query_campus.where(
                PlanningSchool.planning_school_operation_type == query_model.school_operation_type)
        paging = await self.query_page(query_campus, page_request)
        return paging

    async def get_sync_school(self, planning_school_no):
        session = await self.slave_db()
        query = select(PlanningSchool).where(
            PlanningSchool.is_deleted == False, PlanningSchool.status == "normal",
            PlanningSchool.planning_school_no == planning_school_no)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_planning_school_by_school_no(self, school_no):
        session = await self.slave_db()
        query_planning_school = select(PlanningSchool.planning_school_name.label("school_name"),
                                       PlanningSchool.planning_school_no.label("school_no"),
                                       PlanningSchool.borough.label("borough"), PlanningSchool.block.label("block"),
                                       PlanningSchool.planning_school_org_type.label("school_org_type"),
                                       PlanningSchool.planning_school_short_name.label("school_short_name"),
                                       PlanningSchool.planning_school_en_name.label("school_en_name"),
                                       PlanningSchool.social_credit_code.label("social_credit_code"),
                                       PlanningSchool.urban_rural_nature.label("urban_rural_nature"),
                                       PlanningSchool.planning_school_org_form.label("school_org_form"),
                                       PlanningSchool.planning_school_edu_level.label("school_edu_level"),
                                       PlanningSchool.planning_school_category.label("school_category"),
                                       PlanningSchool.planning_school_operation_type.label("school_operation_type"),
                                       PlanningSchool.sy_zones.label("sy_zones"),
                                       PlanningSchoolCommunication.postal_code.label("postal_code"),
                                       PlanningSchoolCommunication.detailed_address.label("detailed_address")).join(
            PlanningSchoolCommunication,
            PlanningSchoolCommunication.planning_school_id == PlanningSchool.id).where(
            PlanningSchool.is_deleted == False, PlanningSchool.status == "normal",
            PlanningSchoolCommunication.is_deleted == False, PlanningSchool.planning_school_no == school_no)
        result = await session.execute(query_planning_school)
        return result.first()

