from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.students_dao import StudentsDao
from models.students import Student
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel


@dataclass_inject
class StudentsRule(object):
    students_dao: StudentsDao

    async def get_students_by_id(self, students_id):
        """
        获取单个学生信息
        """
        students_db = await self.students_dao.get_students_by_id(students_id)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        return students

    async def add_students(self, students: StudentsKeyinfoModel):
        """
        新增学生关键信息
        """
        students_db = view_model_to_orm_model(students, Student, exclude=[""])
        students_db = await self.students_dao.add_students(students_db)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        return students

    async def update_students(self, students):
        """
        编辑学生关键信息
        """
        exists_students = await self.students_dao.get_students_by_id(students.student_id)
        if not exists_students:
            raise Exception(f"编号为{students.student_id}学生不存在")
        need_update_list = []
        for key, value in students.dict().items():
            if value:
                need_update_list.append(key)
        students = await self.students_dao.update_students(students, *need_update_list)
        return students

    async def delete_students(self, students_id):
        """
        删除学生关键信息
        """
        exists_students = await self.students_dao.get_students_by_id(students_id)
        if not exists_students:
            raise Exception(f"编号为{students_id}学生不存在")
        students_db = await self.students_dao.delete_students(exists_students)
        return students_db
