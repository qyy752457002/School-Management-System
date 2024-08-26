# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.course import CourseNotFoundError, CourseAlreadyExistError

from daos.education_year_dao import EducationYearDAO
from models.education_year import EducationYear
from views.models.education_year import EducationYearModel


@dataclass_inject
class EducationYearRule(object):
    education_year_dao: EducationYearDAO

    async def get_education_year_by_id(self, education_year_id):
        education_year_db = await self.education_year_dao.get_education_year_by_id(education_year_id)
        # 可选 , exclude=[""]
        education_year = orm_model_to_view_model(education_year_db, EducationYearModel)
        return education_year
    async def get_education_year_by_name(self, education_year_name):
        education_year_db = await self.education_year_dao.get_education_year_by_name(education_year_name)
        # 可选 , exclude=[""]
        education_year = orm_model_to_view_model(education_year_db, EducationYearModel)
        return education_year

    async def add_education_year(self, education_year: EducationYearModel):
        exists_education_year = await self.education_year_dao.get_education_year_by_name(
            education_year.education_year_name)
        if exists_education_year:
            raise CourseAlreadyExistError()
        education_year_db = view_model_to_orm_model(education_year, EducationYear,    exclude=["id"])

        education_year_db = await self.education_year_dao.add_education_year(education_year_db)
        education_year = orm_model_to_view_model(education_year_db, EducationYearModel, exclude=["created_at",'updated_at'])
        return education_year

    async def update_education_year(self, education_year,ctype=1):
        exists_education_year = await self.education_year_dao.get_education_year_by_id(education_year.id)
        if not exists_education_year:
            raise CourseNotFoundError()
        need_update_list = []
        for key, value in education_year.dict().items():
            if value:
                need_update_list.append(key)

        education_year_db = await self.education_year_dao.update_education_year(education_year, *need_update_list)


        # education_year_db = await self.education_year_dao.update_education_year(education_year_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # education_year = orm_model_to_view_model(education_year_db, EducationYearModel, exclude=[""])
        return education_year_db

    async def softdelete_education_year(self, education_year_id):
        exists_education_year = await self.education_year_dao.get_education_year_by_id(education_year_id)
        if not exists_education_year:
            raise Exception(f"课程信息{education_year_id}不存在")
        education_year_db = await self.education_year_dao.softdelete_education_year(exists_education_year)
        return education_year_db
    async def softdelete_education_year_by_school_id(self, education_year_id):
        # exists_education_year = await self.education_year_dao.get_education_year_by_school_id(education_year_id)
        # if not exists_education_year:
        #     raise Exception(f"课程信息{education_year_id}不存在")
        education_year_db = await self.education_year_dao.softdelete_education_year_by_school_id(education_year_id)
        return education_year_db


    async def get_education_year_count(self):
        return await self.education_year_dao.get_education_year_count()

    async def query_education_year_with_page(self, page_request: PageRequest,school_id=None, education_year_name=None,
                                              education_year_id=None,education_year_no=None ):
        kdict = {
            "education_year_name": education_year_name,
            "school_id": school_id,
            "education_year_id": education_year_id,
            "education_year_no": education_year_no,
            "is_deleted":False
        }
        if not kdict["education_year_name"]:
            del kdict["education_year_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]
        if not kdict["education_year_id"]:
            del kdict["education_year_id"]
        if not kdict["education_year_no"]:
            del kdict["education_year_no"]

        paging = await self.education_year_dao.query_education_year_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, EducationYearModel)
        return paging_result


    async def get_education_year_all(self, school_type, city, district, ):
        return await self.education_year_dao.query_education_year_with_args(school_type, city, district,)


    async def add_education_year_school(self,school_id,education_year_list):
        exists_education_year = await self.education_year_dao.get_education_year_by_school_id(      school_id)
        if exists_education_year:
            raise CourseAlreadyExistError()
        # education_year_db =  Course(school_id=school_id,education_year_list=education_year_list)
        for education_year in education_year_list:
            education_year_db= view_model_to_orm_model(education_year, EducationYear, exclude=["id"])
            res = await self.education_year_dao.add_education_year(education_year_db)

            # print(education_year_db.education_year_list)





        # education_year_db = await self.education_year_dao.add_education_year(education_year_db)
        education_year = orm_model_to_view_model(res, EducationYearModel, exclude=["created_at",'updated_at'])
        return education_year


