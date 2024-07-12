import copy
import os
import pprint
from datetime import datetime, date

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.storage.view_model import FileStorageModel
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.async_task.data_access.task_dao import TaskDAO

from business_exceptions.common import IdCardError, EnrollNumberError, EduNumberError
from daos.school_dao import SchoolDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.students import Student, StudentApprovalAtatus
from rules.storage_rule import StorageRule
from rules.system_rule import SystemRule
from views.common.common_view import check_id_number, convert_snowid_in_model
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel, StudentsKeyinfoDetail, StudentsKeyinfo, \
    NewStudentTransferIn, NewStudentsQuery, NewStudentsQueryRe
from views.models.students import NewStudents
from business_exceptions.student import StudentNotFoundError, StudentExistsError

from mini_framework.utils.logging import logger



@dataclass_inject
class StudentsRule(object):
    students_dao: StudentsDao
    school_dao: SchoolDAO
    students_baseinfo_dao: StudentsBaseInfoDao
    file_storage_dao: FileStorageDAO
    # students_base_info_dao: StudentsBaseInfoDao
    task_dao: TaskDAO


    async def get_students_by_id(self, students_id):
        """
        获取单个学生信息
        """
        students_db = await self.students_dao.get_students_by_id(students_id)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoDetail, exclude=[""])
        # 照片等  处理URL 72
        if students.photo and students.photo.isnumeric():
            sysrule = get_injector(SystemRule)
            students.photo = await sysrule.get_download_url_by_id(students.photo)
            logger.info(f"photo url:{students.photo}")

            pass


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
        convert_snowid_in_model(students, ["id",'student_id','school_id','class_id','session_id'])

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
            if await self.students_dao.get_students_by_param(enrollment_number=students.enrollment_number,is_deleted=False):
                raise EnrollNumberError()
        students_db.student_id = SnowflakeIdGenerator(1, 1).generate_id()
        students_db = await self.students_dao.add_students(students_db)
        print(students_db)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        print(students)
        convert_snowid_in_model(students, ["id",'student_id','school_id','class_id','session_id'])
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
            exist = await self.students_baseinfo_dao.get_students_base_info_by_param(**kdict)
            if exist:
                # raise EduNumberError()
                pass

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
                # raise StudentExistsError()
                pass


        # print(students_db)
        students_db.student_id = SnowflakeIdGenerator(1, 1).generate_id()

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
        # 针对日期 字符串型  转换为datetime或者date
        if isinstance(students.birthday, tuple) or (isinstance(students.birthday, str)  ):
            # 使用 strptime 函数将字符串转换为 datetime 对象
            students.birthday = datetime.strptime( students.birthday,  "%Y-%m-%d %H:%M:%S")
            # date_object = datetime.strptime(date_string, "%Y-%m-%d")
            # students.birthday = students.birthday.date()
            print(students.birthday)
        for key, value in students.dict().items():
            if value:
                need_update_list.append(key)
        students = await self.students_dao.update_students(students, *need_update_list)
        students = copy.deepcopy(students)
        convert_snowid_in_model(students)
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


    async def student_export(self, task: Task):
        bucket = 'student'
        print(bucket,'桶')

        export_params: NewStudentsQuery = (
            task.payload if task.payload is NewStudentsQuery() else NewStudentsQuery()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"student_export_{shortuuid.uuid()}.xlsx"
        temp_file_path = os.path.join(os.path.dirname(__file__), 'tmp')
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)
        temp_file_path = os.path.join(temp_file_path, random_file_name)
        while True:
            paging = await self.students_baseinfo_dao.query_students_with_page(
                export_params, page_request
            )
            paging_result = PaginatedResponse.from_paging(
                paging, NewStudentsQueryRe, {"hash_password": "password"}
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
            task_result.result_bucket = file_storage_resp.bucket_name
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



    async def complete_info_students_by_id(self, student_edu_info):
        """
        学校ID 填充获取学校名称等

        """
        if student_edu_info.school_id:
            school_info = await self.school_dao.get_school_by_id(student_edu_info.school_id)
            if  school_info:
                student_edu_info.school_name = school_info.school_name
        if student_edu_info.student_id:
            school_info = await self.students_baseinfo_dao.get_students_base_info_by_student_id(student_edu_info.student_id)
            if  school_info:
                student_edu_info.edu_number = school_info.edu_number

        return student_edu_info

    async def update_student_formaladmission(self, student_id):
        """
        编辑学生关键信息  StudentApprovalAtatus.FORMAL_ADMISSION.value
        """
        # 判断student_id存在逗号,  则分割为列表
        if ',' in student_id:
            student_id = student_id.split(',')

        students = await self.students_dao.update_student_formaladmission( student_id, StudentApprovalAtatus.FORMAL.value )
        # if not exists_students:
        #     raise StudentNotFoundError()
        # need_update_list = []
        # for key, value in students.dict().items():
        #     if value:
        #         need_update_list.append(key)
        # students = await self.students_dao.update_students(students, *need_update_list)
        return students