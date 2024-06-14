# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from typing import List

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.subject import SubjectAlreadyExistError
# from business_exceptions.subject import CourseNotFoundError, CourseAlreadyExistError
from daos.subject_dao import SubjectDAO
from models.subject import Subject
from views.models.subject import Subject  as SubjectModel
from views.models.extend_params import ExtendParams


@dataclass_inject
class SubjectRule(object):
    subject_dao: SubjectDAO

    async def get_subject_by_id(self, subject_id):
        subject_db = await self.subject_dao.get_subject_by_id(subject_id)
        # 可选 , exclude=[""]
        subject = orm_model_to_view_model(subject_db, SubjectModel)
        return subject
    async def get_subject_by_name(self, subject_name):
        subject_db = await self.subject_dao.get_subject_by_name(subject_name)
        # 可选 , exclude=[""]
        subject = orm_model_to_view_model(subject_db, SubjectModel)
        return subject

    async def add_subject(self, subject: SubjectModel):
        exists_subject = await self.subject_dao.get_subject_by_param(
            subject)
        if exists_subject:
            raise SubjectAlreadyExistError()
        subject_db = view_model_to_orm_model(subject, Subject,    exclude=["id"])

        subject_db = await self.subject_dao.add_subject(subject_db)
        subject = orm_model_to_view_model(subject_db, SubjectModel, exclude=["created_at",'updated_at'])
        return subject

    async def update_subject(self, subject,ctype=1):
        exists_subject = await self.subject_dao.get_subject_by_id(subject.id)
        if not exists_subject:
            raise CourseNotFoundError()
        need_update_list = []
        for key, value in subject.dict().items():
            if value:
                need_update_list.append(key)

        subject_db = await self.subject_dao.update_subject(subject, *need_update_list)


        # subject_db = await self.subject_dao.update_subject(subject_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # subject = orm_model_to_view_model(subject_db, SubjectModel, exclude=[""])
        return subject_db

    async def softdelete_subject(self, subject_id):
        exists_subject = await self.subject_dao.get_subject_by_id(subject_id)
        if not exists_subject:
            raise Exception(f"课程信息{subject_id}不存在")
        subject_db = await self.subject_dao.softdelete_subject(exists_subject)
        return subject_db
    async def softdelete_subject_by_school_id(self, subject_id):
        subject_db = await self.subject_dao.softdelete_subject_by_school_id(subject_id)
        return subject_db
    async def softdelete_subject_by_district(self, subject_id):
        subject_db = await self.subject_dao.softdelete_subject_by_district(subject_id)
        return subject_db

    async def get_subject_count(self):
        return await self.subject_dao.get_subject_count()

    async def query_subject_with_page(self, page_request: PageRequest,school_id=None,subject_name=None,
                                               extobj:ExtendParams=None):
        kdict = {
            "subject_name": subject_name,
            "school_id": school_id,
            # "subject_id": subject_id,
            # "subject_no": subject_no,
            "city": extobj.city,
            "district": extobj.county_id,
            # "is_deleted":False
        }
        if not kdict["subject_name"]:
            del kdict["subject_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]

        if not kdict["city"]:
            del kdict["city"]
        if not kdict["district"]:
            del kdict["district"]

        paging = await self.subject_dao.query_subject_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SubjectModel)
        return paging_result


    async def get_subject_all(self, filterdict):
        return await self.subject_dao.get_all_subject(filterdict)


    async def add_subject_school(self,school_id,subject_list:List[SubjectModel],obj:ExtendParams=None):
        res=None
        if school_id:
            exists_subject = await self.subject_dao.get_subject_by_school_id(      school_id)
            if exists_subject:
                raise CourseAlreadyExistError()
        for subject in subject_list:
            # 扩展参数 放入到视图模型 再转换给orm
            if obj.county_id:
                subject.district=obj.county_id
            if obj.edu_type:
                subject.school_type=obj.edu_type
            subject_db= view_model_to_orm_model(subject, Course, exclude=["id"])

            res = await self.subject_dao.add_subject(subject_db)
        subject = orm_model_to_view_model(res, SubjectModel, exclude=["created_at",'updated_at'])
        return subject


