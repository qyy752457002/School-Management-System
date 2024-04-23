from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.students import Student
from models.students_base_info import StudentBaseInfo


class StudentsBaseInfoDao(DAOBase):
    async def add_students_base_info(self, students_base_info):
        """
        新增学生基本信息
        """
        session = await self.master_db()
        session.add(students_base_info)
        await session.commit()
        await session.refresh(students_base_info)
        return students_base_info

    async def update_students_base_info(self, students_base_info: Student, *args, is_commit: bool = True):
        """
        编辑学生基本信息
        """
        session = await self.master_db()
        update_contents = get_update_contents(students_base_info, *args)
        query = update(StudentBaseInfo).where(StudentBaseInfo.student_id == students_base_info.student_id).values(**update_contents)
        return await self.update(session, query, students_base_info, update_contents, is_commit=is_commit)

    async def get_students_base_info_by_id(self, students_id):
        """
        获取单个学生基本信息
        """
        session = await self.slave_db()
        result = await session.execute(select(Student).where(Student.student_id == students_id))
        return result.scalar_one_or_none()

    async def delete_students_base_info(self, students: Student):
        """
        删除单个学生基本信息
        """
        session = self.master_db()
        return await self.delete(session, students)

    async def query_students_with_page(self, page_request: PageRequest, condition) -> Paging:
        query = select(Student.student_name, Student.id_type, Student.id_number, Student.enrollment_number,
                       Student.gender, Student.approval_status, StudentBaseInfo.residence_district,
                       StudentBaseInfo.school).select_from(Student).join(StudentBaseInfo,
                                                                         Student.student_id == StudentBaseInfo.student_id)
        properties = vars(condition)
        conditions = []
        for key, value in properties.items():
            if hasattr(Student, key):
                conditions.append(getattr(Student, key) == value)
            if hasattr(StudentBaseInfo, key):
                conditions.append(getattr(StudentBaseInfo, key) == value)
        if conditions:
            query = query.where(*conditions)
        paging = await self.query_page(query, page_request)
        return paging

    async def get_all_students_base_info(self):
        session = await self.slave_db()
        result = await session.execute(select(StudentBaseInfo))
        return result.scalars().all()

    async def get_student_base_info_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(StudentBaseInfo))
        return result.scalar()