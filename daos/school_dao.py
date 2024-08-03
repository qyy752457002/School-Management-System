from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select, func, update, desc

from models.campus import Campus
from models.planning_school import PlanningSchool
from models.school import School
from models.school_communication import SchoolCommunication
from views.models.extend_params import ExtendParams
from views.models.school_and_teacher_sync import SchoolSyncQueryModel
from views.models.system import InstitutionType


class SchoolDAO(DAOBase):

    async def get_school_by_process_instance_id(self, process_instance_id):
        session = await self.slave_db()
        result = await session.execute(select(School).where(School.process_instance_id == process_instance_id))
        return result.scalar()

    async def get_school_by_id(self, school_id):
        school_id = int(school_id)
        session = await self.slave_db()
        result = await session.execute(select(School).where(School.id == school_id))
        return result.scalar_one_or_none()

    async def get_school_by_school_name(self, school_name):
        session = await self.slave_db()
        result = await session.execute(
            select(School).where(School.school_name == school_name).where(School.is_deleted == False))
        return result.first()

    async def get_school_by_args(self, **kwargs):
        """
        """
        session = await self.slave_db()
        query = select(School)
        for key, value in kwargs.items():
            query = query.where(getattr(School, key) == value)
        result = await session.execute(query)
        return result.scalar()

    async def add_school(self, school):
        session = await self.master_db()
        session.add(school)
        await session.commit()
        await session.refresh(school)
        return school

    async def update_school_byargs(self, school: School, *args, is_commit: bool = True):
        school.id = int(school.id)
        session = await self.master_db()
        update_contents = get_update_contents(school, *args)
        # 遍历 检查如果模型里没有这个属性 则 删除
        for key in list(update_contents.keys()):
            if not hasattr(School, key):
                del update_contents[key]
        query = update(School).where(School.id == school.id).values(**update_contents)
        return await self.update(session, query, school, update_contents, is_commit=is_commit)

    async def update_school(self, school, ctype=1):
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
        school.id = int(school.id)
        session = await self.master_db()
        deleted_status = 1
        update_stmt = update(School).where(School.id == school.id).values(
            is_deleted=deleted_status,
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

    async def query_school_with_page(self, page_request: PageRequest, school_name, school_no, school_code,
                                     block, school_level, borough, status, founder_type,
                                     founder_type_lv2,
                                     founder_type_lv3, planning_school_id, province, city, institution_category,
                                     social_credit_code, school_org_type, extend_params: ExtendParams = None) -> Paging:

        query = (select(
            School.id, School.planning_school_id, School.institution_category, School.school_name, School.school_no,
            School.school_code, School.school_operation_license_number, School.block, School.borough,
            School.school_edu_level, School.school_category, School.school_operation_type, School.school_org_type,
            School.school_level, School.status, School.kg_level, School.school_short_name, School.school_en_name,
            School.create_school_date, School.social_credit_code, School.founder_type, School.founder_type_lv2,
            School.founder_type_lv3, School.founder_name, School.founder_code, School.location_economic_attribute,
            School.urban_ethnic_nature, School.leg_repr_certificatenumber, School.urban_rural_nature,
            School.school_org_form, School.school_closure_date, School.department_unit_number, School.sy_zones,
            School.historical_evolution, School.sy_zones_pro, School.primary_school_system,
            School.primary_school_entry_age, School.junior_middle_school_system, School.junior_middle_school_entry_age,
            School.senior_middle_school_system, School.membership_no, School.is_entity, School.process_instance_id,
            School.workflow_status, School.created_uid, School.updated_uid, School.created_at, School.updated_at,
            School.is_deleted,

            SchoolCommunication.leg_repr_name).select_from(School).join(PlanningSchool,
                                                                        PlanningSchool.id == School.planning_school_id,
                                                                        isouter=True)
        .join(SchoolCommunication, SchoolCommunication.school_id == School.id, isouter=True).order_by(
            desc(School.id)))
        query = query.where(School.is_deleted == False)
        if extend_params is not None and len(block) == 0 and len(borough) == 0:
            if extend_params.county_id:
                block = extend_params.county_id
                # query = query.where(PlanningSchool.city == extend_params.city)
            pass
        if extend_params is not None and planning_school_id is None:
            if extend_params.school_id:
                planning_school_id = extend_params.school_id
            pass

        if school_org_type:
            query = query.where(School.school_org_type == school_org_type)
        if social_credit_code:
            query = query.where(School.social_credit_code == social_credit_code)
        if institution_category:
            if isinstance(institution_category, list):
                query = query.where(School.institution_category.in_(institution_category))
            else:
                query = query.where(School.institution_category == institution_category)
        else:
            query = query.where( School.institution_category.not_in([InstitutionType.INSTITUTION, InstitutionType.ADMINISTRATION, ]))
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

        if founder_type_lv3 and len(founder_type_lv3) > 0:
            query = query.where(School.founder_type_lv3.in_(founder_type_lv3))

        paging = await self.query_page(query, page_request)
        return paging

    async def update_school_status(self, school, status):
        session = await self.master_db()
        next_status = 1
        if status == 1:
            next_status = '正常'
        else:
            next_status = '已关闭'

        update_stmt = update(School).where(School.id == school.id).values(
            status=next_status,
        )
        await session.execute(update_stmt)
        # await session.delete(school)
        await session.commit()
        return school

    async def query_sync_school_with_page(self, query_model: SchoolSyncQueryModel,
                                          page_request: PageRequest) -> Paging:
        query_school = select(School.school_no, School.social_credit_code, School.school_name, School.borough,
                              School.block,
                              School.founder_type, School.founder_type_lv2, School.founder_type_lv3).where(
            School.is_deleted == False, School.status == "normal")
        if query_model.social_credit_code:
            query_school = query_school.where(School.social_credit_code == query_model.social_credit_code)
        if query_model.school_name:
            query_school = query_school.where(School.school_name.like(f"%{query_model.school_name}%"))
        if query_model.borough:
            query_school = query_school.where(School.borough == query_model.borough)
        if query_model.block:
            query_school = query_school.where(School.block == query_model.block)
        if query_model.school_edu_level:
            query_school = query_school.where(School.school_edu_level == query_model.school_edu_level)
        if query_model.school_category:
            query_school = query_school.where(School.school_category == query_model.school_category)
        if query_model.school_operation_type:
            query_school = query_school.where(School.school_operation_type == query_model.school_operation_type)

        query_campus = select(Campus.campus_no, Campus.social_credit_code, Campus.campus_name.label("school_name"),
                              Campus.borough,
                              Campus.block, Campus.founder_type, Campus.founder_type_lv2,
                              Campus.founder_type_lv3).where(
            Campus.is_deleted == False, Campus.status == "opening")
        if query_model.social_credit_code:
            query_campus = query_campus.where(Campus.social_credit_code == query_model.social_credit_code)
        if query_model.school_name:
            query_campus = query_campus.where(
                Campus.campus_name.label("school_name").like(f"%{query_model.school_name}%"))
        if query_model.borough:
            query_campus = query_campus.where(Campus.borough == query_model.borough)
        if query_model.block:
            query_campus = query_campus.where(Campus.block == query_model.block)
        if query_model.school_edu_level:
            query_campus = query_campus.where(Campus.campus_operation_type == query_model.school_edu_level)
        if query_model.school_category:
            query_campus = query_campus.where(Campus.campus_operation_type_lv2 == query_model.school_category)
        if query_model.school_operation_type:
            query_campus = query_campus.where(Campus.campus_operation_type_lv3 == query_model.school_operation_type)

        query_planning_school = select(School.school_no, School.social_credit_code, School.school_name, School.borough,
                              School.block,
                              School.founder_type, School.founder_type_lv2, School.founder_type_lv3).where(
            School.is_deleted == False, School.status == "normal")

        if query_model.type == "planning_school":
            query = query_planning_school
        elif query_model.type == "school":
            query = query_school
        elif query_model.type == "campus":
            query = query_campus

        paging = await self.query_page(query, page_request)
        return paging

    async def get_sync_school(self, school_no):
        session = await self.slave_db()
        query = select(School).where(
            School.is_deleted == False, School.status == "normal",
            School.school_no == school_no)
        result = await session.execute(query)
        return result.scalar_one_or_none()
