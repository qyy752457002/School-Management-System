import copy
import os
from datetime import datetime, date

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.common import IdCardError, EnrollNumberError, EduNumberError
from business_exceptions.school import SchoolNotFoundError
from daos.class_dao import ClassesDAO
from daos.school_dao import SchoolDAO
from daos.students_base_info_dao import StudentsBaseInfoDao
from daos.students_dao import StudentsDao
from models.public_enum import Gender
from models.students import Student, StudentApprovalAtatus
from rules.import_common_abstract_rule import ImportCommonAbstractRule
from rules.system_rule import SystemRule
from views.common.common_view import check_id_number, convert_snowid_in_model
from views.models.students import NewStudents
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel, StudentsKeyinfoDetail, NewStudentTransferIn, \
    NewStudentsQuery, NewStudentsQueryRe, NewStudentImport
from business_exceptions.student import StudentFamilyInfoNotFoundError, StudentNotFoundError,StudentExistsError


@dataclass_inject
class StudentsRule(ImportCommonAbstractRule, object):
    students_dao: StudentsDao
    school_dao: SchoolDAO
    class_dao: ClassesDAO
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
            fileurl = await sysrule.get_download_url_by_id(students.photo)
            students.photo_url = fileurl
            logger.info(f"photo url:{students.photo}")

            pass

        # 查其他的信息
        baseinfo2 = await self.students_baseinfo_dao.get_students_base_info_ext_by_student_id(students_id)
        # print(baseinfo2)
        # baseinfo= baseinfo2[0]
        if baseinfo2:
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
        convert_snowid_in_model(students, ["id", 'student_id', 'school_id', 'class_id', 'session_id'])

        return students

    async def add_students(self, students: NewStudents | NewStudentImport):
        """
        新增学生关键信息
        """
        # db里的生日只能日期型 兜底的给str转日期
        if isinstance(students.birthday, tuple) or (
                isinstance(students.birthday, str) and len(students.birthday) == 0) or students.birthday is None:
            students.birthday = date(1970, 1, 1)
        print(students)
        students_db = view_model_to_orm_model(students, Student, exclude=["student_id"])
        # 校验身份证号
        if students.id_type == 'resident_id_card':
            idstatus = check_id_number(students.id_number)
            if not idstatus:
                raise IdCardError()
        # 报名号 去重  学籍号去重
        if hasattr(students, 'enrollment_number') and students.enrollment_number:
            if await self.students_dao.get_students_by_param(enrollment_number=students.enrollment_number,
                                                             is_deleted=False):
                raise EnrollNumberError()
        # 证件类型和证件号 唯一
        exists_students = await self.students_dao.get_students_by_param(id_type=students.id_type,id_number=students.id_number,is_deleted=False,)
        if  exists_students:
            raise StudentExistsError()
        # 校验学校
        if students.school_id:
            school = await self.school_dao.get_school_by_id(students.school_id)
            if not school:
                raise SchoolNotFoundError()

        students_db.student_id = SnowflakeIdGenerator(1, 1).generate_id()

        students_db = await self.students_dao.add_students(students_db)
        print(students_db)
        students = orm_model_to_view_model(students_db, StudentsKeyinfoModel, exclude=[""])
        print(students)
        convert_snowid_in_model(students, ["id",'student_id','school_id','class_id','session_id'])
        # await self.send_student_to_org_center(students)

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
            kdict["is_deleted"] = False
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
        students = orm_model_to_view_model(students_db, NewStudentTransferIn, exclude=[""],
                                           other_mapper={"id": "student_id"})
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
        print(students.birthday)

        if hasattr(students, 'birthday') and isinstance(students.birthday, tuple):
            students.birthday = None

            # 使用 strptime 函数将字符串转换为 datetime 对象

            # date_object = datetime.strptime(date_string, "%Y-%m-%d")
            # students.birthday = students.birthday.date()
        if hasattr(students, 'birthday') and isinstance(students.birthday, str) and len(students.birthday) > 0:
            students.birthday = datetime.strptime(students.birthday, "%Y-%m-%d %H:%M:%S")
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
        print(bucket, '桶')

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
                item.approval_status = item.approval_status.value

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
        print('临时文件路径', temp_file_path)
        file_storage = storage_manager.put_file_to_object(
            bucket, f"{random_file_name}.xlsx", temp_file_path
        )
        # 这里会写入 task result 提示 缺乏 result file id  导致报错
        try:

            file_storage_resp = await storage_manager.add_file(
                self.file_storage_dao, file_storage
            )
            print('file_storage_resp ', file_storage_resp)

            task_result = TaskResult()
            task_result.task_id = task.task_id
            task_result.result_file = file_storage_resp.file_name
            task_result.result_bucket = file_storage_resp.virtual_bucket_name
            task_result.result_file_id = file_storage_resp.file_id
            task_result.last_updated = datetime.now()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id = 0
            print('拼接数据task_result ', task_result)
            resadd = await self.task_dao.add_task_result(task_result)
            print('task_result写入结果', resadd)
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
            if school_info:
                student_edu_info.school_name = school_info.school_name
        if student_edu_info.student_id:
            school_info = await self.students_baseinfo_dao.get_students_base_info_by_student_id(
                student_edu_info.student_id)
            if school_info:
                student_edu_info.edu_number = school_info.edu_number

        return student_edu_info

    async def update_student_formaladmission(self, student_id):
        """
        编辑学生关键信息  StudentApprovalAtatus.FORMAL_ADMISSION.value
        """
        # 判断student_id存在逗号,  则分割为列表
        if ',' in student_id:
            student_id = student_id.split(',')

        students = await self.students_dao.update_student_formaladmission(student_id,
                                                                          StudentApprovalAtatus.FORMAL.value)
        # if not exists_students:
        #     raise StudentNotFoundError()
        # need_update_list = []
        # for key, value in students.dict().items():
        #     if value:
        #         need_update_list.append(key)
        # students = await self.students_dao.update_students(students, *need_update_list)
        return students

    async def convert_import_format_to_view_model(self, item: NewStudentImport):
        # 学校转id
        # item.block = self.districts[item.block].enum_value if item.block in self.districts else  item.block
        # item.borough = self.districts[item.borough].enum_value if item.borough in self.districts else  item.borough
        if hasattr(item, 'school_name'):
            school = await self.school_dao.get_school_by_school_name(item.school_name)
            item.school_id = school.id if school else None

        if hasattr(item, 'class_name') and item.class_name:
            class_info = await self.class_dao.get_classes_by_classes_name(item.class_name)
            item.class_id = class_info.id if class_info else None
        #     证件类型转英文 中小学班级类型
        if hasattr(item, 'teacher_card_type'):
            item.teacher_card_type = self.id_types.get(item.teacher_card_type, item.teacher_card_type)

        if hasattr(item, 'class_type'):
            item.class_type = self.class_systems.get(item.class_type, item.class_type)
        #     enrollment_method
        if hasattr(item, 'enrollment_method'):
            item.enrollment_method = self.enrollment_methods.get(item.enrollment_method, item.enrollment_method)
        #  todo   residence_nature student_gender ethnicity political_status blood_type 都需要转枚举值
        # 字段转格式的  id_number, photo, approval_status, is_deleted  傻萝卜, None, 'enrollment', False
        if hasattr(item, 'id_number') and item.id_number:
            item.id_number = str(item.id_number)
        if hasattr(item, 'photo') and item.photo:
            item.photo = str(item.photo)
        if hasattr(item, 'photo') and item.photo is None:
            item.photo = ''
        if hasattr(item, 'enrollment_number') and item.enrollment_number is None:
            item.enrollment_number = ''
        if hasattr(item, 'student_gender') and item.student_gender is not None:
            item.student_gender = Gender.from_chinese(item.student_gender)
        # print('转换后',item)
        # 下面是根据学生信息获取ID
        if hasattr(item, 'id_number') and item.id_number:
            student_info = await self.students_dao.get_students_by_param(id_number=item.id_number)
            if student_info:
                item.student_id = student_info.student_id
        pass

    async def is_can_update_student(self, student_id, is_all_status_allow=False):
        tinfo = await self.get_students_by_id(student_id)
        print('当前信息', tinfo)

        # 检查是否有占用 如果有待处理的流程ID 则锁定
        if tinfo and tinfo.approval_status == StudentApprovalAtatus.OUT.value:
            return False
        return True
