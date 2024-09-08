from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select, func, update

from models.school import School
from models.teacher_transaction import TeacherTransaction
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from views.models.extend_params import ExtendParams
from views.models.system import UnitType
from views.models.teacher_transaction import TeacherTransactionQueryModel
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from mini_framework.design_patterns.depend_inject import get_injector


class TeacherTransactionDAO(DAOBase):

    async def add_teacher_transaction(self, teacher_transaction: TeacherTransaction):
        session = await self.master_db()
        session.add(teacher_transaction)
        await session.commit()
        await session.refresh(teacher_transaction)
        return teacher_transaction

    async def get_teacher_transaction_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherTransaction))
        return result.scalar()

    async def delete_teacher_transaction(self, teacher_transaction: TeacherTransaction):
        session = await self.master_db()
        await session.delete(teacher_transaction)
        await session.commit()

    async def get_teacher_transaction_by_teacher_transaction_id(self, teacher_transaction_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherTransaction).where(TeacherTransaction.transaction_id == teacher_transaction_id,
                                             TeacherTransaction.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_teacher_transaction_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherTransaction).join(Teacher, TeacherTransaction.teacher_id == Teacher.teacher_id).where(
            TeacherTransaction.teacher_id == teacher_id).order_by(TeacherTransaction.transaction_time.desc()).limit(
            1)
        result = await session.execute(query)
        return result.one_or_none()

    async def update_teacher_transaction(self, teacher_transaction, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_transaction, *args)
        query = update(TeacherTransaction).where(
            TeacherTransaction.transaction_id == teacher_transaction.transaction_id).values(
            **update_contents)
        return await self.update(session, query, teacher_transaction, update_contents, is_commit=is_commit)

    async def query_transaction_with_page(self, query_model: TeacherTransactionQueryModel,
                                          page_request: PageRequest, extend_params: ExtendParams = None) -> Paging:
        """
        异动查询
        查询结果的内容
        流程审批id：process_instance_id
        教师姓名：teacher_name
        教师ID：teacher_id
        证件类型：teacher_id_type
        证件号：teacher_id_number
        所属机构：teacher_employer
        学校名称：school_name
        异动id：transaction_id
        教职工号： teacher_number
        教师性别：teacher_gender
        异动类型：transaction_type
        所在区县：teacher_district
        申请时间：transaction_time

        查询条件
        """

        query = select(TeacherTransaction.teacher_id, TeacherTransaction.transaction_type,
                       TeacherTransaction.transaction_time, TeacherTransaction.transaction_id,
                       TeacherTransaction.transaction_remark,
                       TeacherTransaction.transaction_type, Teacher.teacher_name, Teacher.teacher_id_type,
                       Teacher.teacher_gender,
                       Teacher.teacher_id_number,
                       TeacherInfo.teacher_number, School.borough, School.school_name).join(Teacher,
                                                                                            Teacher.teacher_id == TeacherTransaction.teacher_id,
                                                                                            ).join(TeacherInfo,
                                                                                                   TeacherInfo.teacher_id == TeacherTransaction.teacher_id,
                                                                                                   isouter=True).join(
            School,
            School.id == Teacher.teacher_employer)
        cond1 = Teacher.teacher_sub_status != "active"
        cond2 = Teacher.teacher_main_status == "employed"
        cond3 = TeacherTransaction.is_active == False
        query = query.where(cond1, cond2, cond3)

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
                if school.institution_category == "institution":
                    query = query.where(School.borough == school.borough)
                else:
                    query = query.where(Teacher.teacher_employer == school.id)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_number:
            query = query.where(TeacherInfo.teacher_number == query_model.teacher_number)
        if query_model.teacher_id_type:
            query = query.where(Teacher.teacher_id_type == query_model.teacher_id_type)
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.transaction_type:
            query = query.where(TeacherTransaction.transaction_type == query_model.transaction_type)
        if query_model.transaction_time_s and query_model.transaction_time_e:
            query = query.where(TeacherTransaction.transaction_time.between(query_model.transaction_time_s,
                                                                            query_model.transaction_time_e))
        if query_model.borough:
            query = query.where(School.borough == query_model.borough)
        if query_model.teacher_employer:
            query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
        query = query.order_by(TeacherTransaction.transaction_time.desc())
        paging = await self.query_page(query, page_request)
        return paging

    async def get_all_transfer(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherTransaction).where(
            TeacherTransaction.teacher_id == teacher_id, TeacherTransaction.is_deleted == False)
        result = await session.execute(query)
        return result.scalars().all()
