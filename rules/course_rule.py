# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.course import CourseNotFoundError, CourseAlreadyExistError
from daos.Course_dao import CourseDAO
from models.course import Course
from views.models.course import Course  as CourseModel



@dataclass_inject
class CourseRule(object):
    course_dao: CourseDAO

    async def get_course_by_id(self, course_id):
        course_db = await self.course_dao.get_course_by_id(course_id)
        # 可选 , exclude=[""]
        course = orm_model_to_view_model(course_db, CourseModel)
        return course
    async def get_course_by_name(self, course_name):
        course_db = await self.course_dao.get_course_by_name(course_name)
        # 可选 , exclude=[""]
        course = orm_model_to_view_model(course_db, CourseModel)
        return course

    async def add_course(self, course: CourseModel):
        exists_course = await self.course_dao.get_course_by_name(
            course.course_name)
        if exists_course:
            raise CourseAlreadyExistError()
        course_db = view_model_to_orm_model(course, Course,    exclude=["id"])

        course_db = await self.course_dao.add_course(course_db)
        course = orm_model_to_view_model(course_db, CourseModel, exclude=["created_at",'updated_at'])
        return course

    async def update_course(self, course,ctype=1):
        exists_course = await self.course_dao.get_course_by_id(course.id)
        if not exists_course:
            raise CourseNotFoundError()
        need_update_list = []
        for key, value in course.dict().items():
            if value:
                need_update_list.append(key)

        course_db = await self.course_dao.update_course(course, *need_update_list)


        # course_db = await self.course_dao.update_course(course_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # course = orm_model_to_view_model(course_db, CourseModel, exclude=[""])
        return course_db

    async def softdelete_course(self, course_id):
        exists_course = await self.course_dao.get_course_by_id(course_id)
        if not exists_course:
            raise Exception(f"课程信息{course_id}不存在")
        course_db = await self.course_dao.softdelete_course(exists_course)
        return course_db
    async def softdelete_course_by_school_id(self, course_id):
        # exists_course = await self.course_dao.get_course_by_school_id(course_id)
        # if not exists_course:
        #     raise Exception(f"课程信息{course_id}不存在")
        course_db = await self.course_dao.softdelete_course_by_school_id(course_id)
        return course_db


    async def get_course_count(self):
        return await self.course_dao.get_course_count()

    async def query_course_with_page(self, page_request: PageRequest,school_id=None, course_name=None,
                                              course_id=None,course_no=None ):
        kdict = {
            "course_name": course_name,
            "school_id": school_id,
            "course_id": course_id,
            "course_no": course_no,
            "is_deleted":False
        }
        if not kdict["course_name"]:
            del kdict["course_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]
        if not kdict["course_id"]:
            del kdict["course_id"]
        if not kdict["course_no"]:
            del kdict["course_no"]

        paging = await self.course_dao.query_course_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CourseModel)
        return paging_result


    async def get_course_all(self, filterdict):
        return await self.course_dao.get_all_course(filterdict)


    async def add_course_school(self,school_id,course_list):
        exists_course = await self.course_dao.get_course_by_school_id(      school_id)
        if exists_course:
            raise CourseAlreadyExistError()
        # course_db =  Course(school_id=school_id,course_list=course_list)
        for course in course_list:
            course_db= view_model_to_orm_model(course, Course, exclude=["id"])
            res = await self.course_dao.add_course(course_db)

            # print(course_db.course_list)





        # course_db = await self.course_dao.add_course(course_db)
        course = orm_model_to_view_model(res, CourseModel, exclude=["created_at",'updated_at'])
        return course


