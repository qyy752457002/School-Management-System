# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import os
from datetime import datetime
from typing import List

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from daos.class_dao import ClassesDAO
from daos.class_division_records_dao import ClassDivisionRecordsDAO
from daos.grade_dao import GradeDAO
from daos.school_dao import SchoolDAO
from daos.students_dao import StudentsDao
from models.class_division_records import ClassDivisionRecords
from rules.students_base_info_rule import StudentsBaseInfoRule
from views.common.common_view import page_none_deal, convert_snowid_to_strings
from views.models.class_division_records import ClassDivisionRecords as ClassDivisionRecordsModel, \
    ClassDivisionRecordsImport
from views.models.class_division_records import ClassDivisionRecordsSearchRes
from views.models.classes import Classes
from views.models.grades import Grades
from views.models.students import NewStudentsQuery, StudentsBaseInfo


@dataclass_inject
class ClassDivisionRecordsRule(object):
    class_division_records_dao: ClassDivisionRecordsDAO
    student_dao: StudentsDao
    class_dao: ClassesDAO
    school_dao: SchoolDAO
    garde_dao: GradeDAO
    file_storage_dao: FileStorageDAO
    # students_base_info_dao: StudentsBaseInfoDao
    task_dao: TaskDAO

    async def get_class_division_records_by_id(self, class_division_records_id):
        class_division_records_db = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records_id)
        # 可选 , exclude=[""]
        class_division_records = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel)
        return class_division_records

    async def add_class_division_records(self, class_id, student_ids):
        class_id = int(class_id)
        class_division_records=[]
        if ',' in student_ids:
            student_ids = student_ids.split(',')
        else:
            student_ids = [student_ids]
        for student_id in student_ids:
            student_id = int(student_id)

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
            class_division_records_db.id = SnowflakeIdGenerator(1, 1).generate_id()
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
        paging_result = PaginatedResponse.from_paging(paging, ClassDivisionRecordsSearchRes,other_mapper={"approval_status": "status",})
        convert_snowid_to_strings(paging_result,["id", "school_id",'grade_id','student_id','class_id'])


        return paging_result

    async def class_division_records_export(self, task: Task):
        bucket = 'student'
        print(bucket,'桶')

        export_params: ClassDivisionRecordsSearchRes = (
            task.payload if task.payload is ClassDivisionRecordsSearchRes() else ClassDivisionRecordsSearchRes()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"class_division_records_export{shortuuid.uuid()}.xlsx"
        temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)
        temp_file_path = os.path.join(temp_file_path, random_file_name)
        while True:
            paging = await self.class_division_records_dao.query_class_division_records_with_page(
                export_params.school_id, export_params.id_type, export_params.student_name,
                export_params.created_at, export_params.student_gender, export_params.class_id,
                export_params.status, export_params.enrollment_number, page_request
            )
            paging_result = PaginatedResponse.from_paging(
                paging, ClassDivisionRecordsSearchRes, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            for item in paging_result.items:
                item.approval_status =  item.approval_status.value


            # logger.info('分页的结果',len(paging_result.items))
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", paging_result.items)
            excel_writer.set_data(temp_file_path)
            excel_writer.execute()
            # break
            if len(paging.items) < page_request.per_page:
                break
            page_request.page += 1
        #     保存文件时可能报错
        print('临时文件路径',temp_file_path)
        file_storage =  storage_manager.put_file_to_object(
            bucket, f"{random_file_name}.xlsx", temp_file_path
        )
        # 这里会写入 task result 提示 缺乏 result file id  导致报错
        try:

            file_storage_resp = await storage_manager.add_file(
                self.file_storage_dao, file_storage
            )
            print('file_storage_resp ',file_storage_resp)

            task_result = TaskResult()
            task_result.task_id = task.task_id
            task_result.result_file = file_storage_resp.file_name
            task_result.result_bucket = file_storage_resp.virtual_bucket_name
            task_result.result_file_id = file_storage_resp.file_id
            task_result.last_updated = datetime.now()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id =  0
            print('拼接数据task_result ',task_result)

            resadd = await self.task_dao.add_task_result(task_result)
            print('task_result写入结果',resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result


    async def add_class_division_records_and_update_student_baseinfo(self,    class_division_records:List[ClassDivisionRecordsImport] ):

        # 根据编码转换ID 等操作
        schools = await self.school_dao.get_all_schools()
        grades = await self.garde_dao.get_all_grades()
        classes  = await self.class_dao.get_all_class()
        dic = {}
        for row in schools:
            dic[getattr(row, 'id')] = row
        schools= dic
        dic = {}
        for row in grades:
            dic[getattr(row, 'id')] = row
        grades= dic
        dic = {}
        for row in classes:
            dic[getattr(row, 'id')] = row
        classes= dic
        students_base_info_rule= get_injector(StudentsBaseInfoRule )
        class_division_records_rule= get_injector(StudentsBaseInfoRule )
        for class_division_records_item in class_division_records:
            class_division_records_item.school_id =  schools[class_division_records_item.school_no].getattr('id') if class_division_records_item.school_no in schools.keys() else None
            class_division_records_item.grade_id =  grades[class_division_records_item.grade_no].getattr('id') if class_division_records_item.grade_no in grades.keys() else None
            class_division_records_item.class_id =  classes[class_division_records_item.class_no].getattr('id') if class_division_records_item.class_no in classes.keys() else None
            student= await self.student_dao.get_students_by_param( student_number = class_division_records_item.student_no)
            class_division_records_item.student_id = student.student_id

            # 学生班级和学生状态
            res = await students_base_info_rule.update_students_class_division( class_division_records_item.class_id,  class_division_records_item.student_id)
            # 分班记录
            res_div = await self.add_class_division_records(class_division_records_item.class_id,  class_division_records_item.student_id)
            # 更新学生的 班级和 学校信息
            student_ids =  class_division_records_item.student_id
            class_id= class_division_records_item.class_id
            if ',' in student_ids:
                student_ids = student_ids.split(',')
            else:
                student_ids = [student_ids]
            for student_id in student_ids:
                baseinfo = StudentsBaseInfo(student_id=student_id, class_id=class_id, school_id=res_div.school_id,
                                            grade_id=res_div.grade_id)

                res3 = await students_base_info_rule.update_students_base_info(baseinfo)




        return class_division_records