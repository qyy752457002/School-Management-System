# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from fastapi import Query
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.graduation_student import GraduationStudentNotFoundError, GraduationStudentAlreadyExistError
from daos.GraduationStudent_dao import GraduationStudentDAO
from daos.students_dao import StudentsDao
from models.graduation_student import GraduationStudent
from models.students import Student, StudentApprovalAtatus
from views.common.common_view import page_none_deal
from views.models.students import GraduationStudents as GraduationStudentModel, StudentGraduation


@dataclass_inject
class GraduationStudentRule(object):
    graduation_student_dao: GraduationStudentDAO
    student_dao: StudentsDao

    async def get_graduationstudent_by_id(self, graduation_student_id):
        graduation_student_db = await self.graduation_student_dao.get_graduationstudent_by_id(graduation_student_id)
        # 可选 , exclude=[""]
        graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel)
        return graduation_student

    async def get_graduation_student_by_name(self, student_name):
        graduation_student_db = await self.graduation_student_dao.get_graduationstudent_by_name(student_name)
        # 可选 , exclude=[""]
        graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel)
        return graduation_student

    async def add_graduation_student(self, graduation_student: GraduationStudentModel):
        exists_graduation_student = await self.graduation_student_dao.get_graduationstudent_by_name(
            graduation_student.student_name)
        if exists_graduation_student:
            raise GraduationStudentAlreadyExistError()
        graduation_student_db = view_model_to_orm_model(graduation_student, GraduationStudent, exclude=["id"])

        graduation_student_db = await self.graduation_student_dao.add_graduationstudent(graduation_student_db)
        graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel,
                                                     exclude=["created_at", 'updated_at'])
        return graduation_student

    async def update_graduation_student(self, student_id, graduate_status, graduate_picture, graduation_photo='',
                                        credential_notes=''):

        need_update_list = []
        graduation_student = StudentGraduation(student_id=student_id)
        print(type(graduation_student.graduation_type))
        if graduate_status and graduate_status is not None:
            graduation_student.graduation_type = graduate_status.value
        if graduate_picture and graduate_picture is not None:
            graduation_student.graduation_remarks = graduate_picture
        if graduation_photo:
            graduation_student.graduation_photo = graduation_photo
        if credential_notes:
            graduation_student.credential_notes = credential_notes
        #
        # if isinstance(graduation_student.graduation_type, tuple):

        # if isinstance(graduation_student.graduation_remarks, tuple):
        #     del graduation_student.graduation_remarks

        for key, value in graduation_student.dict().items():
            if value and value is not Query and not isinstance(value, tuple):
                need_update_list.append(key)
            if isinstance(value, tuple):
                delattr(graduation_student, key)

        print(graduation_student, need_update_list)
        print(vars(graduation_student))


        graduation_student_db = await self.graduation_student_dao.update_graduationstudent(graduation_student,
                                                                                           *need_update_list)
        need_update_list2 = ['approval_status']
        students = Student(student_id=student_id, approval_status=StudentApprovalAtatus.GRADUATED.value)

        graduation_student_db2 = await self.student_dao.update_students(students, *need_update_list2)

        # graduation_student_db = await self.graduation_student_dao.update_graduation_student(graduation_student_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel, exclude=[""])
        return graduation_student_db

    async def softdelete_graduation_student(self, graduation_student_id):
        exists_graduation_student = await self.graduation_student_dao.get_graduationstudent_by_id(graduation_student_id)
        if not exists_graduation_student:
            raise GraduationStudentNotFoundError()
        graduation_student_db = await self.graduation_student_dao.softdelete_graduationstudent(
            exists_graduation_student)
        return graduation_student_db

    async def get_graduation_student_count(self):
        return await self.graduation_student_dao.get_graduationstudent_count()

    async def query_graduation_student_with_page(self, page_request: PageRequest, student_name, school_id, gender,
                                                 edu_number, class_id):
        #    转换条件 为args
        kdict = {
            "student_name": student_name,
            "school_id": school_id,
            "student_gender": gender,
            "edu_number": edu_number,
            "class_id": class_id,
        }
        if not kdict["student_name"]:
            del kdict["student_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]
        if not kdict["student_gender"]:
            del kdict["student_gender"]
        if not kdict["edu_number"]:
            del kdict["edu_number"]
        if not kdict["class_id"]:
            del kdict["class_id"]

        paging = await self.graduation_student_dao.query_graduationstudent_with_page(page_request, **kdict)
        # 字段映射的示例写法   , {"hash_password": "password"}
        # paging_result = PaginatedResponse.from_paging(page_none_deal(paging), NewStudentsQueryRe)

        paging_result = PaginatedResponse.from_paging(page_none_deal(paging), GraduationStudentModel,other_mapper={"student_id":"id" })
        return paging_result
