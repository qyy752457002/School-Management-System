# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.graduation_student import GraduationStudentNotFoundError, GraduationStudentAlreadyExistError
from daos.GraduationStudent_dao import GraduationStudentDAO
from models.graduation_student import GraduationStudent
from views.models.students import GraduationStudents  as GraduationStudentModel



@dataclass_inject
class GraduationStudentRule(object):
    graduation_student_dao: GraduationStudentDAO

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
        graduation_student_db = view_model_to_orm_model(graduation_student, GraduationStudent,    exclude=["id"])

        graduation_student_db = await self.graduation_student_dao.add_graduationstudent(graduation_student_db)
        graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel, exclude=["created_at",'updated_at'])
        return graduation_student

    async def update_graduation_student(self, graduation_student,ctype=1):
        exists_graduation_student = await self.graduation_student_dao.get_graduationstudent_by_id(graduation_student.id)
        if not exists_graduation_student:
            raise GraduationStudentNotFoundError()
        need_update_list = []
        for key, value in graduation_student.dict().items():
            if value:
                need_update_list.append(key)

        graduation_student_db = await self.graduation_student_dao.update_graduationstudent(graduation_student, *need_update_list)


        # graduation_student_db = await self.graduation_student_dao.update_graduation_student(graduation_student_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel, exclude=[""])
        return graduation_student_db

    async def softdelete_graduation_student(self, graduation_student_id):
        exists_graduation_student = await self.graduation_student_dao.get_graduationstudent_by_id(graduation_student_id)
        if not exists_graduation_student:
            raise GraduationStudentNotFoundError()
        graduation_student_db = await self.graduation_student_dao.softdelete_graduationstudent(exists_graduation_student)
        return graduation_student_db


    async def get_graduation_student_count(self):
        return await self.graduation_student_dao.get_graduationstudent_count()

    async def query_graduation_student_with_page(self, page_request: PageRequest,  student_name,school_id,gender,edu_number,class_id ):
        # todo  转换条件 为args
        paging = await self.graduation_student_dao.query_graduationstudent_with_page(page_request,
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, GraduationStudentModel)
        return paging_result

