# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from datetime import datetime

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.grade import GradeAlreadyExistError
from daos.grade_dao import GradeDAO
from models.grade import Grade
from views.models.grades import Grades as GradeModel


@dataclass_inject
class GradeRule(object):
    grade_dao: GradeDAO

    async def get_grade_by_id(self, grade_id):
        grade_db = await self.grade_dao.get_grade_by_id(grade_id)
        # 可选 , exclude=[""]
        grade = orm_model_to_view_model(grade_db, GradeModel)
        return grade

    async def get_grade_by_grade_name(self, grade_name):
        grade_db = await self.grade_dao.get_grade_by_grade_name(grade_name)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def add_grade(self, grade: GradeModel,obj=None):
        exists_grade = await self.grade_dao.get_grade_by_grade_name(grade.grade_name,grade)
        if exists_grade:
            raise GradeAlreadyExistError()

        grade_db = view_model_to_orm_model(grade, Grade,    exclude=["id"])
        grade_db.created_at =   datetime.now()
                                 # .strftime("%Y-%m-%d %H:%M:%S"))

        grade_db = await self.grade_dao.add_grade(grade_db)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def update_grade(self, grade):
        exists_grade = await self.grade_dao.get_grade_by_id(grade.id)
        if not exists_grade:
            raise Exception(f"年级{grade.id}不存在")

        need_update_list = []
        for key, value in grade.dict().items():
            if value:
                need_update_list.append(key)

        print(need_update_list,222,grade)
        grade_db = await self.grade_dao.update_grade_byargs(grade,*need_update_list)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def delete_grade(self, grade_id):
        exists_grade = await self.grade_dao.get_grade_by_id(grade_id)
        if not exists_grade:
            raise Exception(f"年级{grade_id}不存在")
        grade_db = await self.grade_dao.delete_grade(exists_grade)
        grade = orm_model_to_view_model(grade_db, GradeModel, exclude=[""])
        return grade

    async def softdelete_grade(self, grade_id):
        exists_grade = await self.grade_dao.get_grade_by_id(grade_id)
        if not exists_grade:
            raise Exception(f"年级信息{grade_id}不存在")
        grade_db = await self.grade_dao.softdelete_grade(exists_grade)
        return grade_db

    async def get_all_grades(self):
        return await self.grade_dao.get_all_grades()

    async def get_grade_count(self):
        return await self.grade_dao.get_grade_count()

    async def query_grade_with_page(self,  page_request: PageRequest,grade_name=None,school_id=None,city='', district=''):
        paging = await self.grade_dao.query_grade_with_page(grade_name,school_id, page_request,city, district)
        # 字段映射的示例写法
        paging_result = PaginatedResponse.from_paging(paging, GradeModel)
        return paging_result



    async def query_grade(self,grade_name,extendparams=None):

        session = await db_connection_manager.get_async_session("default", True)
        query =select(Grade).where(Grade.grade_name.like(f'%{grade_name}%') )
        if extendparams:
            if extendparams.school_id:
                query = query.where(Grade.school_id == extendparams.school_id)
            if extendparams.city:
                query = query.where(Grade.city == extendparams.city)
            if extendparams.county_id :
                query = query.where(Grade.district == extendparams.county_id)

        result = await session.execute(query)
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, GradeModel)

            lst.append(planning_school)
        return lst

