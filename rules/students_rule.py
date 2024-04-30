from datetime import datetime, date

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.common import IdCardError, EnrollNumberError
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.students import Student
from views.common.common_view import check_id_number
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel, StudentsKeyinfoDetail, StudentsKeyinfo, \
    NewStudentTransferIn
from views.models.students import NewStudents
from business_exceptions.student import StudentNotFoundError, StudentExistsError


@dataclass_inject
class StudentsRule(object):
    students_dao: StudentsDao
    students_baseinfo_dao: StudentsBaseInfoDao

    async def get_students_by_id(self, students_id):
        """
        获取单个学生信息
        """
        students_db = await self.students_dao.get_students_by_id(students_id)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoDetail, exclude=[""])
        # 查其他的信息
        baseinfo2 = await self.students_baseinfo_dao.get_students_base_info_ext_by_student_id(students_id)
        # print(baseinfo2)
        # baseinfo= baseinfo2[0]
        if  baseinfo2:
            # raise StudentNotFoundError("学生不存在")
            graduation_student = baseinfo2[0]
            for key, value in graduation_student.items():
                if value is None:
                    baseinfo2[0][key] = ''
                # delattr(graduation_student, key)

            baseinfo = orm_model_to_view_model(baseinfo2[0], StudentsKeyinfoDetail, exclude=[""],
                                               other_mapper={"major_name": "major_name", })

            if baseinfo:
                students.province = baseinfo.province
                students.city = baseinfo.city
                students.school_name = baseinfo.school_name
                students.session = baseinfo.session
                students.grade_name = baseinfo.grade_name
                students.class_name = baseinfo.class_name
                students.major_name = baseinfo.major_name
                students.block = baseinfo.block
                students.borough = baseinfo.borough
                students.loc_area_pro = baseinfo.loc_area_pro
                students.loc_area = baseinfo.loc_area

        return students

    async def add_students(self, students: NewStudents):
        """
        新增学生关键信息
        """
        students_db = view_model_to_orm_model(students, Student, exclude=["student_id"])
        # 校验身份证号
        if  students.id_type=='resident_id_card':
            idstatus= check_id_number(students.id_number)
            if not idstatus:
                raise IdCardError()
        # 报名号 去重  学籍号去重
        if students.enrollment_number:
            if await self.students_dao.get_students_by_param(enrollment_number=students.enrollment_number,is_delete=False):
                raise EnrollNumberError()

        students_db = await self.students_dao.add_students(students_db)
        print(students_db)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        print(students)
        return students

    async def add_student_new_student_transferin(self, students):
        """
        校验 一个身份证 布能重复 新增学生
        """

        if isinstance(students.birthday, tuple) or (isinstance(students.birthday, str) and len(students.birthday) == 0):

            # 使用 strptime 函数将字符串转换为 datetime 对象
            special_date = date(1970, 1, 1)
            # dt_obj = datetime.strptime( students.birthday, '%Y-%m-%d')

            # 从 datetime 对象中提取 date 部分
            # date_obj = dt_obj.date()
            students.birthday = special_date
        else:
            pass
            # students.birthday = datetime.strptime(students.birthday, '%Y-%m-%d').date()

        # print(students)
        # 校验学籍号
        if students.edu_number:
            kdict = {
                "edu_number": students.edu_number,
                "is_deleted": False
            }
            exist = await self.students_dao.get_students_by_param(**kdict)
            if exist:
                raise EduNumberError()

        students_db = view_model_to_orm_model(students, Student, exclude=["student_id"])
        students_db.student_gender = students.student_gender
        kdict = {

        }
        if students_db.id_number:
            kdict["id_number"] = students_db.id_number
            kdict["is_deleted"] =  False
            exist = await self.students_dao.get_students_by_param(**kdict)
            # print(exist)

            # studentsex = orm_model_to_view_model(exist, NewStudents, exclude=[""])
            # print(studentsex)


            if exist:
                # print(exist)
                raise StudentExistsError()

        # print(students_db)
        students_db = await self.students_dao.add_students(students_db)
        students = orm_model_to_view_model(students_db, NewStudentTransferIn, exclude=[""],other_mapper={"id": "student_id"})
        return students

    async def update_students(self, students):
        """
        编辑学生关键信息
        """
        exists_students = await self.students_dao.get_students_by_id(students.student_id)
        if not exists_students:
            raise StudentNotFoundError()
        need_update_list = []
        for key, value in students.dict().items():
            if value:
                need_update_list.append(key)
        students = await self.students_dao.update_students(students, *need_update_list)
        return students

    async def delete_students(self, students_id):
        """
        删除学生关键信息
        """
        exists_students = await self.students_dao.get_students_by_id(students_id)
        if not exists_students:
            raise StudentNotFoundError()
        students_db = await self.students_dao.delete_students(exists_students)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        return students

    async def get_all_students(self):
        """
        获取所有学生信息
        """
        students_db = await self.students_dao.get_all_students()
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        return students

    async def get_student_count(self):
        """
        获取学生总数
        """
        return await self.students_dao.get_student_count()
