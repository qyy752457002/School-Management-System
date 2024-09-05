# from mini_framework.databases.entities.toolkit import orm_model_to_view_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.subject import SubjectAlreadyExistError, SubjectNotFoundError
from daos.school_dao import SchoolDAO
# from business_exceptions.subject import CourseNotFoundError, CourseAlreadyExistError
from daos.subject_dao import SubjectDAO
from daos.tenant_dao import TenantDAO
from models.subject import Subject
from rules.course_rule import CourseRule
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model
from views.models.extend_params import ExtendParams
from views.models.subject import Subject as SubjectModel


@dataclass_inject
class SubjectRule(object):
    subject_dao: SubjectDAO
    tenant_dao:TenantDAO
    school_dao:SchoolDAO

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
        subject_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        subject_db = await self.subject_dao.add_subject(subject_db)
        subject = orm_model_to_view_model(subject_db, SubjectModel, exclude=["created_at",'updated_at'])
        convert_snowid_in_model(subject, ["id",'student_id','school_id','class_id','session_id','relation_id','process_instance_id','in_school_id','grade_id','transferin_audit_id'])
        return subject

    async def update_subject(self, subject,):
        exists_subject = await self.subject_dao.get_subject_by_id(subject.id)
        if not exists_subject:
            raise SubjectNotFoundError()
        need_update_list = []
        for key, value in subject.dict().items():
            if value:
                need_update_list.append(key)

        subject_db = await self.subject_dao.update_subject(subject, *need_update_list)
        convert_snowid_in_model(subject_db, ["id",'student_id','school_id','class_id','session_id','relation_id','process_instance_id','in_school_id','grade_id','transferin_audit_id'])


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
            "city": extobj.city,
            "district": extobj.county_id,
        }
        if not kdict["subject_name"]:
            del kdict["subject_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]

        if not kdict["city"]:
            del kdict["city"]
        if not kdict["district"]:
            del kdict["district"]
        print(2222, extobj.tenant )
        if extobj.tenant:
            # 读取类型  读取ID  加到条件里
            tenant =  await self.tenant_dao.get_tenant_by_code(extobj.tenant.code)

            if tenant.tenant_type== 'school':
                school =  await self.school_dao.get_school_by_school_no(tenant.code)
                print('获取租户的学校对象',school)
                kdict["school_id"] = school.id
            pass


        paging = await self.subject_dao.query_subject_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, SubjectModel)
        # 处理name
        course_rule = get_injector(CourseRule)
        courses =await course_rule.get_course_all( {'school_id':0} )
        coursemap = {course.course_no: course.course_name for course in courses}
        # print(grade_enums,999)

        for item in paging_result.items:
            if item.course_no in coursemap:

                item.course_name = coursemap[item.course_no]
            else:
                item.course_name =  ''

        convert_snowid_to_strings(paging_result, ["id",'student_id','school_id','class_id','session_id','relation_id','process_instance_id','in_school_id','grade_id','transferin_audit_id'])
        return paging_result


    async def get_subject_all(self, filterdict):
        return await self.subject_dao.get_all_subject(filterdict)

    async def delete_subject(self, subject_id):
        exists_organization = await self.subject_dao.get_subject_by_id(subject_id,True)
        if not exists_organization:
            raise SubjectNotFoundError()
        subject_db = await self.subject_dao.delete_subject(exists_organization)
        return exists_organization


