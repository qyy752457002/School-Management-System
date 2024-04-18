from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase,get_update_contents
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

    async def delete_students(self,students:Student):
        """
        删除单个学生信息
        """
        session = self.master_db()
        return await self.delete(session, students)


