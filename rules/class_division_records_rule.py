# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from daos.class_dao import ClassesDAO
from daos.class_division_records_dao import ClassDivisionRecordsDAO
from daos.grade_dao import GradeDAO
from daos.students_dao import StudentsDao
from models.class_division_records import ClassDivisionRecords
from views.common.common_view import page_none_deal
from views.models.class_division_records import ClassDivisionRecords as ClassDivisionRecordsModel
from views.models.class_division_records import ClassDivisionRecordsSearchRes
from views.models.classes import Classes
from views.models.grades import Grades
from views.models.students import NewStudentsQuery


@dataclass_inject
class ClassDivisionRecordsRule(object):
    class_division_records_dao: ClassDivisionRecordsDAO
    student_dao: StudentsDao
    class_dao: ClassesDAO
    garde_dao: GradeDAO

    async def get_class_division_records_by_id(self, class_division_records_id):
        class_division_records_db = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records_id)
        # 可选 , exclude=[""]
        class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel)
        return class_division_records

    async def add_class_division_records(self, class_id, student_ids):
        class_division_records=[]
        if ',' in student_ids:
            student_ids = student_ids.split(',')
        else:
            student_ids = [student_ids]
        for student_id in student_ids:
            class_division_records = ClassDivisionRecordsModel(class_id=class_id, student_id=student_id)
            class_division_records_db = view_model_to_orm_model(class_division_records, ClassDivisionRecords, exclude=["id"])

            #     读取 班级细腻系  学生信息
            # class_info = await self.class_dao.get_classes_info_by_id(class_id)
            # print(class_info)
            #
            # class_info = orm_model_to_view_model(class_info, Classes)
            #
            # print(class_info)
            # class_division_records.grade_id = class_info.grade_id
            # class_division_records.school_id = class_info.school_id
            stu_info = await self.student_dao.get_students_by_id(student_id)
            stu_info = orm_model_to_view_model(stu_info, NewStudentsQuery)

            # stu_info =
            class_info = orm_model_to_view_model(await self.class_dao.get_classes_by_id(class_id), Classes)

            grade_info = orm_model_to_view_model(await self.garde_dao.get_grade_by_id(class_info.grade_id), Grades)


            # class_division_records.student_no = stu_info.student_no
            class_division_records_db.student_name = stu_info.student_name
            class_division_records_db.grade_id = class_info.grade_id

            class_division_records_db.school_id = grade_info.school_id
            # class_division_records_db.status =

            class_division_records_db = await self.class_division_records_dao.add_class_division_records(class_division_records_db)
            class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=["created_at", 'updated_at'])


        #
        # exists_class_division_records = await self.class_division_records_dao.add_class_division_records(
        #     class_division_records.class_name, class_division_records.school_id)

        # class_division_records_db = view_model_to_orm_model(class_division_records, ClassDivisionRecords, exclude=["id"])
        #
        # class_division_records_db = await self.class_division_records_dao.add_class_division_records(class_division_records_db)
        # class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=["created_at", 'updated_at'])
        return class_division_records

    async def update_class_division_records(self, class_division_records, ctype=1):
        exists_class_division_records = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records.id)
        if not exists_class_division_records:
            raise Exception(f"班级信息{class_division_records.id}不存在")
        need_update_list = []
        for key, value in class_division_records.dict().items():
            if value:
                need_update_list.append(key)

        class_division_records_db = await self.class_division_records_dao.update_class_division_records_byargs(class_division_records, *need_update_list)

        # class_division_records_db = await self.class_division_records_dao.update_class_division_records(class_division_records_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=[""])
        return class_division_records_db

    async def softdelete_class_division_records(self, class_division_records_id):
        exists_class_division_records = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records_id)
        if not exists_class_division_records:
            raise Exception(f"班级信息{class_division_records_id}不存在")
        class_division_records_db = await self.class_division_records_dao.delete_class_division_records(exists_class_division_records)
        # class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=[""],)
        return class_division_records_db

    async def get_class_division_records_count(self):
        return await self.class_division_records_dao.get_class_division_records_count()

    async def query_class_division_records_with_page(self, page_request: PageRequest, school_id,id_type,student_name,created_at,student_gender,class_id,status,enrollment_number):
        paging = await self.class_division_records_dao.query_class_division_records_with_page(school_id,id_type,student_name,created_at,student_gender,class_id,status,enrollment_number,
                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"} ClassDivisionRecordsSearchRes
        print(paging)
        paging=page_none_deal(paging)
        # paging_result = PaginatedResponse.from_paging(, NewStudentsQueryRe)
        paging_result = PaginatedResponse.from_paging(paging, ClassDivisionRecordsSearchRes,other_mapper={"school_name": "school_name",})
        return paging_result
