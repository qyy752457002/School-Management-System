# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from datetime import datetime

from fastapi import Query
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import (
    orm_model_to_view_model,
    view_model_to_orm_model,
)

from business_exceptions.graduation_student import (
    GraduationStudentNotFoundError,
    GraduationStudentAlreadyExistError,
)
from business_exceptions.school import SchoolNotFoundError
from daos.graduation_student_dao import GraduationStudentDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from daos.students_dao import StudentsDao
from models.graduation_student import GraduationStudent
from models.students import Student, StudentApprovalAtatus
from rules.classes_rule import ClassesRule
from views.common.common_view import page_none_deal
from views.models.student_graduate import (
    GraduateStudentQueryModel,
    GraduateStudentQueryReModel,
    CountySchoolArchiveQueryReModel,
)
from views.models.students import (
    GraduationStudents as GraduationStudentModel,
    StudentGraduation,
)
from views.models.system import SchoolNatureLv2


@dataclass_inject
class GraduationStudentRule(object):
    graduation_student_dao: GraduationStudentDAO
    student_dao: StudentsDao
    school_dao: SchoolDAO
    student_session_dao: StudentSessionDao

    async def get_graduationstudent_by_id(self, graduation_student_id):
        graduation_student_db = (
            await self.graduation_student_dao.get_graduationstudent_by_id(
                graduation_student_id
            )
        )
        # 可选 , exclude=[""]
        graduation_student = orm_model_to_view_model(
            graduation_student_db, GraduationStudentModel
        )
        return graduation_student

    async def get_graduation_student_by_name(self, student_name):
        graduation_student_db = (
            await self.graduation_student_dao.get_graduationstudent_by_name(
                student_name
            )
        )
        # 可选 , exclude=[""]
        graduation_student = orm_model_to_view_model(
            graduation_student_db, GraduationStudentModel
        )
        return graduation_student

    async def add_graduation_student(self, graduation_student: GraduationStudentModel):
        exists_graduation_student = (
            await self.graduation_student_dao.get_graduationstudent_by_name(
                graduation_student.student_name
            )
        )
        if exists_graduation_student:
            raise GraduationStudentAlreadyExistError()
        graduation_student_db = view_model_to_orm_model(
            graduation_student, GraduationStudent, exclude=["id"]
        )

        graduation_student_db = await self.graduation_student_dao.add_graduationstudent(
            graduation_student_db
        )
        graduation_student = orm_model_to_view_model(
            graduation_student_db,
            GraduationStudentModel,
            exclude=["created_at", "updated_at"],
        )
        return graduation_student

    async def update_graduation_student_status(self, student_id, graduate_status):
        exit_graduates_student = (
            await self.graduation_student_dao.get_graduationstudent_by_student_id(
                student_id
            )
        )
        if not exit_graduates_student:
            raise GraduationStudentNotFoundError()
        if exit_graduates_student.archive_status == True:
            raise Exception("该学生已归档，不能修改毕业状态")
        exit_graduates_student.status = graduate_status
        result = await self.graduation_student_dao.update_graduationstudent(
            exit_graduates_student, "status"
        )
        return result

    async def update_archive_status_and_year_by_student_id(self, school_id):
        """
        更新归学校所有学生的归档状态，并在区县学校表中增加已完全归档的学校
        """
        res = await self.graduation_student_dao.update_graduation_student_archive_status_by_school_id(
            school_id
        )
        return res

    async def update_archive_status_and_year_by_student_id_county(self, borough):
        un_graduate_school_list = []
        # 获取未发起毕业的学校
        un_graduate_school_list_db = (
            await self.graduation_student_dao.get_school_is_graduate()
        )
        for school in un_graduate_school_list_db:
            item = {}
            item["school_id"] = school.school_id
            item["school_name"] = school.school_name
            un_graduate_school_list.append(item)
        # 判断是否有未发起毕业的学校
        if not un_graduate_school_list:
            res = await self.graduation_student_dao.update_graduation_student_archive_status(
                borough
            )
            return res
        else:
            return un_graduate_school_list

    async def update_graduation_student(
        self,
        student_id,
        graduate_status,
        graduate_picture,
        graduation_photo="",
        credential_notes="",
    ):
        need_update_list = []
        graduation_student = StudentGraduation(student_id=student_id)
        print(type(graduation_student.graduation_type))
        if graduate_status and graduate_status is not None:
            graduation_student.graduation_type = graduate_status
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

        # print(graduation_student, need_update_list)
        # print(vars(graduation_student))

        graduation_student_db = (
            await self.graduation_student_dao.update_graduationstudent(
                graduation_student, *need_update_list
            )
        )
        need_update_list2 = ["approval_status"]
        students = Student(
            student_id=student_id, approval_status=StudentApprovalAtatus.GRADUATED.value
        )

        graduation_student_db2 = await self.student_dao.update_students(
            students, *need_update_list2
        )

        # graduation_student_db = await self.graduation_student_dao.update_graduation_student(graduation_student_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # graduation_student = orm_model_to_view_model(graduation_student_db, GraduationStudentModel, exclude=[""])
        return graduation_student_db

    async def softdelete_graduation_student(self, graduation_student_id):
        exists_graduation_student = (
            await self.graduation_student_dao.get_graduationstudent_by_id(
                graduation_student_id
            )
        )
        if not exists_graduation_student:
            raise GraduationStudentNotFoundError()
        graduation_student_db = (
            await self.graduation_student_dao.softdelete_graduationstudent(
                exists_graduation_student
            )
        )
        return graduation_student_db

    async def get_graduation_student_count(self):
        return await self.graduation_student_dao.get_graduationstudent_count()

    async def query_graduation_student_with_page(
        self,
        page_request: PageRequest,
        student_name,
        school_id,
        gender,
        edu_number,
        class_id,
        borough,
    ):
        #    转换条件 为args
        kdict = {
            "student_name": student_name,
            "school_id": school_id,
            "student_gender": gender,
            "edu_number": edu_number,
            "class_id": class_id,
            "borough": borough,
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
        if not kdict["borough"]:
            del kdict["borough"]

        paging = await self.graduation_student_dao.query_graduationstudent_with_page(
            page_request, **kdict
        )
        # 字段映射的示例写法   , {"hash_password": "password"}
        # paging_result = PaginatedResponse.from_paging(page_none_deal(paging), NewStudentsQueryRe)

        paging_result = PaginatedResponse.from_paging(
            page_none_deal(paging),
            GraduationStudentModel,
            other_mapper={"student_id": "id"},
        )
        return paging_result

    async def update_graduation_student_by_school_id(self, school_id):
        """
        根据学校id更新学生毕业状态
        """
        school_db = await self.school_dao.get_school_by_id(school_id)
        if not school_db:
            raise SchoolNotFoundError()
        school_category = school_db.school_category
        grade_level = SchoolNatureLv2.get_grade_level(school_category)
        result = (
            await self.graduation_student_dao.update_graduation_student_by_school_id(
                school_id, grade_level
            )
        )
        if result == True:
            year = str(datetime.now().year)
            session = await self.student_session_dao.get_student_session_by_year(year)
            if not session:
                raise Exception("当前年度届别不存在")
            else:
                session_id = session.session_id
                class_rule = get_injector(ClassesRule)
                # 这里是为了删除已毕业学生的班级信息
                result = await class_rule.delete_class_by_school_id_and_session_id(
                    school_id, session_id
                )
                if result == True:
                    page_request = PageRequest(page=1, per_page=10)
                    query_model = GraduateStudentQueryModel(school_id=school_id)
                    paging = await self.query_graduation_student_by_model_with_page(
                        page_request, query_model
                    )
                    return paging
                else:
                    return result
        else:
            return result

    async def update_graduation_student_by_school_id_new(self, school_id):
        """
        按照年级是否是毕业年级来更新学生的毕业状态
        """
        school_db = await self.school_dao.get_school_by_id(school_id)
        if not school_db:
            raise SchoolNotFoundError()
        result = await self.graduation_student_dao.update_graduation_student_by_school_id_new(school_id)


    async def query_graduation_student_by_model_with_page(
        self, page_request: PageRequest, query_model
    ):
        """
        根据条件查询毕业生
        """
        paging = await self.graduation_student_dao.query_graduation_student_by_model_with_page(
            page_request, query_model
        )
        paging_result = PaginatedResponse.from_paging(
            paging, GraduateStudentQueryReModel
        )
        return paging_result

    async def query_school_archive_status_with_page(
        self, page_request: PageRequest, query_model
    ):
        paging = (
            await self.graduation_student_dao.query_school_archive_status_with_page(
                page_request, query_model
            )
        )
        paging_result = PaginatedResponse.from_paging(
            paging, CountySchoolArchiveQueryReModel
        )
        return paging_result

    async def upgrade_all_student(self, school_id):
        """
        升级所有学生
        """
        result = await self.graduation_student_dao.upgrade_all_student(school_id)
        return result
