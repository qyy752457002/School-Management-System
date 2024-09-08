# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import copy
from typing import List

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.course import CourseNotFoundError, CourseAlreadyExistError
from daos.course_dao import CourseDAO
from daos.school_dao import SchoolDAO
from models.course import Course
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model
from views.models.course import Course as CourseModel
from views.models.extend_params import ExtendParams


@dataclass_inject
class CourseRule(object):
    course_dao: CourseDAO
    school_dao: SchoolDAO

    async def get_course_by_id(self, course_id):
        course_id=int(course_id)
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
            course.course_name,course)
        if exists_course:
            raise CourseAlreadyExistError()
        course_db = view_model_to_orm_model(course, Course,    exclude=["id"])
        course_db.id = SnowflakeIdGenerator(1, 1).generate_id()

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
        course_db = await self.course_dao.softdelete_course_by_school_id(course_id)
        return course_db
    async def softdelete_course_by_district(self, course_id):
        course_db = await self.course_dao.softdelete_course_by_district(course_id)
        return course_db

    async def get_course_count(self):
        return await self.course_dao.get_course_count()

    async def query_course_with_page(self, page_request: PageRequest,school_id=None, course_name=None,
                                              course_id=None,course_no=None ,extobj:ExtendParams=None):
        kdict = {
            "course_name": course_name,
            "school_id": school_id,
            "course_id": course_id,
            "course_no": course_no,
            "school_nature": None,
            "city": extobj.city,
            "district": extobj.county_id,
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
        if not kdict["city"]:
            del kdict["city"]
        if not kdict["district"]:
            del kdict["district"]
        # 如果有学校ID  读取学校的 二级类型
        if school_id is not None:
            school_info = await self.school_dao.get_school_by_id(school_id)
            if school_info:
                kdict["school_nature"] = school_info.school_category
        print(kdict)

        paging = await self.course_dao.query_course_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CourseModel)
        convert_snowid_to_strings(paging_result, ["id", "school_id",'grade_id',])
        return paging_result


    async def get_course_all(self, filterdict):
        items =  await self.course_dao.get_all_course(filterdict)
        items = copy.deepcopy(items)
        for item in items:
            convert_snowid_in_model(item,["id", "school_id",'grade_id',])
        return items


    async def add_course_school(self,school_id,course_list:List[CourseModel],obj:ExtendParams=None):
        res=None
        print("add_course_school",school_id,obj)
        if school_id:
            exists_course = await self.course_dao.get_course_by_school_id(      school_id)
            if exists_course:
                raise CourseAlreadyExistError()
        #     自动对list里的课程遍历 针对courseno去重
        cousrnos= [ ]

        for course in course_list:
            if school_id:
                course.school_id = school_id
            if course.course_no in cousrnos:
                print("重复课程",course.course_no)
                continue
            cousrnos.append(course.course_no)
            # 扩展参数 放入到视图模型 再转换给orm
            if obj and  obj.county_id:
                course.district=obj.county_id
            if obj  and  obj.edu_type:
                course.school_type=obj.edu_type
            course_db= view_model_to_orm_model(course, Course, exclude=["id"])
            course_db.id = SnowflakeIdGenerator(1, 1).generate_id()

            res = await self.course_dao.add_course(course_db)
        course = orm_model_to_view_model(res, CourseModel, exclude=["created_at",'updated_at'])
        convert_snowid_in_model(course, ["id", "school_id",'grade_id',])
        return course


