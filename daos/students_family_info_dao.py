from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.students import Student
from models.students_family_info import StudentFamilyInfo


class StudentsFamilyInfoDao(DAOBase):
    async def add_students_family_info(self, students_family_info):
        """
        新增学生家庭信息
        """
        session = await self.master_db()
        session.add(students_family_info)
        await session.commit()
        await session.refresh(students_family_info)
        return students_family_info

    async def update_students_family_info(self, students_family_info, *args, is_commit: bool = True):
        """
        编辑学生家庭信息
        """
        session = await self.master_db()
        update_contents = get_update_contents(students_family_info, *args)
        query = update(StudentFamilyInfo).where(
            StudentFamilyInfo.student_family_info_id == students_family_info.student_family_info_id).values(
            **update_contents)
        return await self.update(session, query, students_family_info, update_contents, is_commit=is_commit)

    async def get_students_family_info_by_id(self, students_family_info_id):
        """
        获取单个学生单条家庭信息
        """
        session = await self.slave_db()
        result = await session.execute(
            select(StudentFamilyInfo).where(StudentFamilyInfo.student_family_info_id == int(students_family_info_id)))
        return result.scalar_one_or_none()

    async def delete_students_family_info(self, students: StudentFamilyInfo):
        """
        删除单个学生家庭信息
        """
        session = await self.master_db()
        return await self.delete(session, students)

    async def get_all_students_family_info(self, student_id):
        session = await self.slave_db()
        query = select(StudentFamilyInfo).join(Student, StudentFamilyInfo.student_id == Student.student_id).where(
            StudentFamilyInfo.student_id == int(student_id))
        result = await session.execute(query)
        return result.scalars().all()

    async def get_student_family_info_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(StudentFamilyInfo))
        return result.scalar()

    async def get_student_family_info_by_param(self, **kwargs):
        """
        获取单个学生信息
        """
        session = await self.slave_db()
        query = select(StudentFamilyInfo)
        for key, value in kwargs.items():
            query = query.where(getattr(StudentFamilyInfo, key) == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()
