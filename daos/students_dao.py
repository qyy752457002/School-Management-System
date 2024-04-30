from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.students import Student


class StudentsDao(DAOBase):
    async def add_students(self, students):
        """
        新增学生关键信息
        """
        session = await self.master_db()
        session.add(students)
        await session.commit()
        await session.refresh(students)
        return students

    async def update_students(self, students: Student, *args, is_commit: bool = True):
        """
        编辑学生关键信息
        """
        session = await self.master_db()
        update_contents = get_update_contents(students, *args)
        query = update(Student).where(Student.student_id == students.student_id).values(**update_contents)
        return await self.update(session, query, students, update_contents, is_commit=is_commit)

    async def get_students_by_id(self, students_id):
        """
        获取单个学生信息
        """
        session = await self.slave_db()
        result = await session.execute(select(Student).where(Student.student_id == students_id))
        return result.scalar_one_or_none()

    async def get_students_by_param(self, **kwargs):
        """
        获取单个学生信息
        """
        session = await self.slave_db()
        query = select(Student)
        for key, value in kwargs.items():
            query = query.where(getattr(Student, key) == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def delete_students(self, students: Student):
        """
        删除单个学生信息 无法自动识别主键  故手写
        """
        session = await self.master_db()
        deleted_status= True
        update_stmt = update(Student).where(Student.student_id == students.student_id).values(
            is_deleted= deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return students

    async def get_all_students(self):
        session = await self.slave_db()
        result = await session.execute(select(Student))
        return result.scalars().all()

    async def get_student_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Student))
        return result.scalar()
