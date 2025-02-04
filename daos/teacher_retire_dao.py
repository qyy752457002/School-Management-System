from mini_framework.databases.entities.dao_base import DAOBase
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select

from models.school import School
from models.teacher_retire import TeacherRetire
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from views.models.extend_params import ExtendParams
from views.models.teacher_transaction import TeacherRetireQuery
from views.models.teachers import TeacherMainStatus
from views.models.system import UnitType
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from mini_framework.design_patterns.depend_inject import get_injector


class TeachersRetireDao(DAOBase):
    # 新增教师基本信息
    async def add_teacher_retire(self, teacher_retire):
        """
        传入的参数
        """
        session = await self.master_db()
        session.add(teacher_retire)
        await session.commit()
        await session.refresh(teacher_retire)
        return teacher_retire

    # 获取单个教师基本信息
    async def get_teacher_retire_by_id(self, teacher_retire_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherRetire).join(Teacher, Teacher.teacher_id == TeacherRetire.teacher_id).where(
                TeacherRetire.teacher_retire_id == teacher_retire_id))
        return result.scalar_one_or_none()

    async def get_teachers_info_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherRetire).join(Teacher, Teacher.teacher_id == TeacherRetire.teacher_id).where(
                TeacherRetire.teacher_id == teacher_id, TeacherRetire.is_deleted == False))
        return result.scalar_one_or_none()

    async def query_retire_teacher_with_page(self, query_model: TeacherRetireQuery,
                                             page_request: PageRequest, extend_params: ExtendParams = None) -> Paging:
        query = select(TeacherRetire.retire_date, TeacherRetire.retire_number, Teacher.teacher_id,
                       Teacher.teacher_main_status,
                       Teacher.teacher_sub_status,
                       Teacher.teacher_name, Teacher.teacher_id_number,
                       Teacher.teacher_gender,
                       Teacher.teacher_employer, TeacherInfo.highest_education,
                       TeacherInfo.political_status, TeacherInfo.in_post,
                       School.school_name,
                       TeacherInfo.enter_school_time).join(TeacherRetire,
                                                           Teacher.teacher_id == TeacherRetire.teacher_id).join(
            TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id, isouter=True
        ).join(School, Teacher.teacher_employer == School.id,
               )
        # if extend_params:
        #     if extend_params.unit_type == UnitType.SCHOOL.value:
        #         query = query.where(Teacher.teacher_employer == extend_params.school_id)
        #     elif extend_params.unit_type == UnitType.COUNTRY.value:
        #         query = query.where(School.borough == extend_params.county_id)
        #     else:
        #         pass
        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao = get_injector(TenantDAO)
            school_dao = get_injector(SchoolDAO)
            tenant = await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)
            if tenant.tenant_type == "school":
                school = await school_dao.get_school_by_id(tenant.origin_id)
                # 如果是事业单位，则就是自己查询自己事业单位的信息
                if school.institution_category == "institution":
                    query = query.where(School.borough == school.borough)
                else:
                    query = query.where(Teacher.teacher_employer == school.id)
        if query_model.in_post != None:
            query = query.where(Teacher.teacher_main_status == TeacherMainStatus.RETIRED.value,
                                TeacherInfo.in_post == query_model.in_post)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender.value)
        if query_model.teacher_employer:
            if query_model.teacher_employer != 0:
                query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
            else:
                pass
        if query_model.highest_education:
            query = query.where(TeacherInfo.highest_education == query_model.highest_education)
        if query_model.political_status:
            query = query.where(TeacherInfo.political_status == query_model.political_status)
        if query_model.in_post is not None:
            query = query.where(TeacherInfo.in_post == query_model.in_post)
        if query_model.enter_school_time_s and query_model.enter_school_time_e:
            query = query.where(
                TeacherInfo.enter_school_time >= query_model.enter_school_time_s,
                TeacherInfo.enter_school_time <= query_model.enter_school_time_e)
        #     非在职时间的筛选
        if query_model.retire_date_s and query_model.retire_date_e:
            query = query.where(
                TeacherRetire.retire_date >= query_model.retire_date_s,
                TeacherRetire.retire_date <= query_model.retire_date_e)
        query = query.order_by(Teacher.teacher_id.desc())
        paging = await self.query_page(query, page_request)
        return paging
