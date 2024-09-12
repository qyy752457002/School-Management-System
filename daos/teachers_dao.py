from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from sqlalchemy import and_
from sqlalchemy import select, func, update

from models.organization import Organization
from models.organization_members import OrganizationMembers
from models.school import School
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from views.models.teacher_transaction import TeacherTransactionQuery


class TeachersDao(DAOBase):
    # 新增教师关键信息
    async def add_teachers(self, teachers):
        session = await self.master_db()
        session.add(teachers)
        await session.commit()
        await session.refresh(teachers)
        return teachers

    async def update_teachers(self, teachers, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers, *args)
        query = update(Teacher).where(Teacher.teacher_id == teachers.teacher_id).values(**update_contents)
        return await self.update(session, query, teachers, update_contents, is_commit=is_commit)

    # 获取单个教师信息
    async def get_teachers_by_id(self, teachers_id):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id == teachers_id, Teacher.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_teachers_arg_by_id(self, teachers_id, org_id):
        session = await self.slave_db()
        query = select(Teacher.teacher_avatar.label("avatar"),
                       Teacher.teacher_date_of_birth.label("birthDate"),
                       Teacher.teacher_name.label("realName"),
                       Teacher.teacher_id_type.label("idCardType"),
                       Teacher.teacher_id_number.label("idCardNumber"),
                       func.coalesce(School.org_center_info, '').label("currentUnit"),
                       Organization.org_name.label("departmentId"),
                       Teacher.teacher_gender.label("gender"),
                       OrganizationMembers.identity.label("identity"),
                       OrganizationMembers.member_type.label("identityType"),
                       Teacher.mobile.label("name"),
                       Teacher.teacher_id.label("userId"),
                       School.school_no.label("owner")
                       ).join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id).join(Organization,
                                                                                              TeacherInfo.org_id == Organization.id).join(
            School, School.id == Teacher.teacher_employer, isouter=True).join(OrganizationMembers, and_(
            OrganizationMembers.org_id == Organization.id, OrganizationMembers.teacher_id == Teacher.teacher_id
        ))
        query = query.where(Teacher.teacher_id == teachers_id,
                            Teacher.is_deleted == False,
                            TeacherInfo.org_id == org_id,
                            Organization.id == org_id, OrganizationMembers.is_deleted == False,
                            Teacher.is_deleted == False)
        result = await session.execute(query)
        return result.first()

    # 根据身份证号获取教师信息

    async def get_teachers_by_teacher_id_number(self, teacher_id_number):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher).where(Teacher.teacher_id_number == teacher_id_number, Teacher.is_deleted == False))
        return result.scalar_one_or_none()

    # 删除单个教师信息
    async def delete_teachers(self, teachers: Teacher):
        session = await self.master_db()
        print(teachers.teacher_id, teachers.is_deleted)
        return await self.delete(session, teachers)

    # 获取所有教师信息
    async def get_all_teachers(self):
        session = await self.slave_db()
        result = await session.execute(select(Teacher))
        return result.scalars().all()

    async def get_all_teachers_id_list(self):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher.teacher_id).where(Teacher.is_deleted == False, Teacher.is_approval == False,
                                             Teacher.teacher_main_status == 'employed'))
        return result.scalars().all()

    async def get_all_teachers_id_list_by_school_id(self, school_id):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher.teacher_id).where(Teacher.is_deleted == False, Teacher.is_approval == False,
                                             Teacher.teacher_main_status == 'employed',
                                             Teacher.teacher_employer == school_id))
        return result.scalars().all()

    # 获取教师数量
    async def get_teachers_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Teacher))
        return result.scalar()

    async def query_teacher_transfer(self, teacher_transaction: TeacherTransactionQuery):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_name == teacher_transaction.teacher_name,
                                      Teacher.teacher_id_type == teacher_transaction.teacher_id_type,
                                      Teacher.teacher_id_number == teacher_transaction.teacher_id_number,
                                      Teacher.is_deleted == False
                                      )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_teacher_by_params(self, teacher_id_number, teacher_id_type, teacher_name):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_id_number == teacher_id_number,
                                      Teacher.teacher_id_type == teacher_id_type,
                                      Teacher.teacher_name == teacher_name,
                                      Teacher.is_deleted == False, Teacher.teacher_main_status == 'employed',
                                      Teacher.is_approval == False)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_teachers_info_by_prams(self, teacher_id_number, teacher_id_type, teacher_name, teacher_gender):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_id_number == teacher_id_number,
                                      Teacher.teacher_id_type == teacher_id_type,
                                      Teacher.teacher_name == teacher_name,
                                      Teacher.teacher_gender == teacher_gender,Teacher.is_deleted == False)
        result = await session.execute(query)
        length = len(result.scalars().all())
        return length

    async def get_teachers_info_by_prams_school_id(self, teacher_id_number, teacher_id_type, teacher_name,
                                                   teacher_employer):
        session = await self.slave_db()
        query = select(Teacher).where(Teacher.teacher_id_number == teacher_id_number,
                                      Teacher.teacher_id_type == teacher_id_type,
                                      Teacher.teacher_name == teacher_name,
                                      Teacher.teacher_employer == teacher_employer,Teacher.is_deleted == False)
        result = await session.execute(query)
        length = len(result.scalars().all())
        return length
