from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.grade_dao import GradeDAO
from models.grade import Grade
from views.models.grades import Grades as GradeModel


@dataclass_inject
class GradeRule(object):
    grade_dao: GradeDAO

    async def get_grade_by_id(self, grade_id):
        grade_db = await self.grade_dao.get_grade_by_id(grade_id)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def get_grade_by_grade_name(self, grade_name):
        grade_db = await self.grade_dao.get_grade_by_grade_name(grade_name)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def add_grade(self, grade: GradeModel):
        exists_grade = await self.grade_dao.get_grade_by_grade_name(grade.grade_name)
        if exists_grade:
            raise Exception(f"年级{grade.grade_name}已存在")
        grade_db = Grade()
        grade_db.grade_name = grade.grade_name
        grade_db.school_id = grade.school_id
        grade_db.grade_no = grade.grade_no
        grade_db.grade_alias = grade.grade_alias
        grade_db.description = grade.description

        grade_db = await self.grade_dao.add_grade(grade_db)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def update_grade(self, grade):
        exists_grade = await self.grade_dao.get_grade_by_id(grade.id)
        if not exists_grade:
            raise Exception(f"年级{grade.id}不存在")
        grade_db = await self.grade_dao.update_grade(grade)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def delete_grade(self, grade_id):
        exists_grade = await self.grade_dao.get_grade_by_id(grade_id)
        if not exists_grade:
            raise Exception(f"年级{grade_id}不存在")
        grade_db = await self.grade_dao.delete_grade(exists_grade)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def get_all_grades(self):
        return await self.grade_dao.get_all_grades()

    async def get_grade_count(self):
        return await self.grade_dao.get_grade_count()

    async def query_grade_with_page(self, grade_name, page_request: PageRequest):
        paging = await self.grade_dao.query_grade_with_page(grade_name, page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, GradeModel)
        return paging_result
