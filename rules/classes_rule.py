import copy
import traceback
from datetime import datetime

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.classes import ClassesLockedError
from daos.class_dao import ClassesDAO
from daos.grade_dao import GradeDAO
from daos.school_dao import SchoolDAO
from daos.student_session_dao import StudentSessionDao
from models.classes import Classes
from rules.common.common_rule import send_orgcenter_request, get_school_map, get_grade_map
from rules.enum_value_rule import EnumValueRule
from rules.import_common_abstract_rule import ImportCommonAbstractRule
from rules.teachers_rule import TeachersRule
from views.common.common_view import convert_snowid_in_model, convert_snowid_to_strings, convert_dates_to_strings, \
    system_config
from views.models.classes import Classes as ClassesModel, ClassStatus
from views.models.classes import ClassesSearchRes
from views.models.system import GRADE_ENUM_KEY, MAJOR_LV3_ENUM_KEY


@dataclass_inject
class ClassesRule(ImportCommonAbstractRule, object):
    classes_dao: ClassesDAO
    school_dao: SchoolDAO
    session_dao: StudentSessionDao
    grade_dao: GradeDAO
    class_leader_teacher_rule = 1  # `1填写 2关联老师

    async def get_classes_by_id(self, classes_id):
        classes_db = await self.classes_dao.get_classes_by_id(classes_id)
        # 可选 , exclude=[""]
        classes = orm_model_to_view_model(classes_db, ClassesModel)
        return classes

    async def get_classes_by_name(self, classes_id):
        classes_db = await self.classes_dao.get_classes_by_classes_name(classes_id)
        # 可选 , exclude=[""]
        classes = orm_model_to_view_model(classes_db, ClassesModel)
        return classes

    async def add_classes(self, classes: ClassesModel):
        classes_input = copy.deepcopy(classes)
        exists_classes = await self.classes_dao.get_classes_by_classes_name(
            classes.class_name, classes.school_id, classes)
        if exists_classes:
            raise Exception(f"班级信息{classes.class_name}已存在")
        await self.check_lock()

        # 校验 teacher_id,care_teacher_id  根据系统配置来决定是允许手填还是关联老师 默认关联老师
        if self.class_leader_teacher_rule == 1:
            if hasattr(classes, "teacher_id") and classes.teacher_id is not None and isinstance(classes.teacher_id,
                                                                                                str) and not classes.teacher_id.isdigit():
                # 名字 则提换到 teacher_name
                if classes.teacher_name is None or len(classes.teacher_name) == 0:
                    classes.teacher_name = classes.teacher_id
                classes.teacher_id = None

            pass
        elif self.class_leader_teacher_rule == 2:

            teacher_rule = get_injector(TeachersRule)
            if classes.teacher_id:
                tea = await teacher_rule.get_teachers_by_id(classes.teacher_id)
                if not tea:
                    raise Exception(f"班主任信息{classes.teacher_id}不存在")
                pass
            if classes.care_teacher_id:
                tea = await teacher_rule.get_teachers_by_id(classes.care_teacher_id)
                if not tea:
                    raise Exception(f"保育员信息{classes.care_teacher_id}不存在")
                pass
        # 如果存在专业 校验专业是否符合枚举
        if classes.major_for_vocational:
            enum_value_rule = get_injector(EnumValueRule)
            check_major = await  enum_value_rule.check_enum_values(MAJOR_LV3_ENUM_KEY, classes.major_for_vocational)
            if not check_major:
                raise Exception(f"专业信息{classes.major_for_vocational}不存在,请选择正确的专业")

        # 学校类别  届别 年级 班号
        class_std_name_mix = []
        if classes.school_id:
            school_db = await self.school_dao.get_school_by_id(classes.school_id)
            class_std_name_mix.append(school_db.school_category if school_db and school_db.school_category else '')
            pass
        if classes.session_id:
            session_db = await self.session_dao.get_student_session_by_id(classes.session_id)
            class_std_name_mix.append(session_db.session_name if session_db and session_db.session_name else '')
            pass
        if classes.grade_id:
            grade_db = await self.grade_dao.get_grade_by_id(classes.grade_id)
            class_std_name_mix.append(grade_db.grade_name if grade_db and grade_db.grade_name else '')
            pass
        class_std_name_mix.append(classes.class_number)
        classes.class_standard_name = "".join(class_std_name_mix)
        print(classes)

        classes_db = view_model_to_orm_model(classes, Classes, exclude=["id"], other_mapper={

        })
        # 更新时间赋值当前的时间
        classes_db.updated_at = datetime.now()

        classes_db.id = SnowflakeIdGenerator(1, 1).generate_id()
        classes_db_out = await self.classes_dao.add_classes(classes_db)
        classes_out = orm_model_to_view_model(classes_db, ClassesModel, exclude=["created_at", 'updated_at'])
        await self.grade_dao.increment_class_number(classes.school_id, classes.grade_id)

        # 组织中心对接过去 todo  接口故障  超时  不让他影响接口
        try:
            school = await self.school_dao.get_school_by_id(classes_input.school_id)
            print(school)

            await self.send_org_to_org_center(classes, school)
            pass
        except TypeError as e:
            print('班级作为部门对接失败', e)
            traceback.print_exc()
        except Exception as e:
            print('班级作为部门对接失败', e)
            traceback.print_exc()

        return classes_out

    async def update_classes(self, classes, ctype=1):
        exists_classes = await self.classes_dao.get_classes_by_id(classes.id)
        if not exists_classes:
            raise Exception(f"班级信息{classes.id}不存在")
        await self.check_lock(exists_classes)

        need_update_list = []
        for key, value in classes.dict().items():
            if value:
                need_update_list.append(key)

        classes_db = await self.classes_dao.update_classes_byargs(classes, *need_update_list)

        # classes_db = await self.classes_dao.update_classes(classes_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # classes = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""])
        classes_db = copy.deepcopy(classes_db)
        convert_snowid_in_model(classes_db, ['id'])
        return classes_db

    async def softdelete_classes(self, classes_id):
        exists_classes = await self.classes_dao.get_classes_by_id(classes_id)
        if not exists_classes:
            raise Exception(f"班级信息{classes_id}不存在")
        await self.check_lock(exists_classes)

        classes_db = await self.classes_dao.softdelete_classes(exists_classes)
        # classes = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""],)
        return classes_db

    async def check_lock(self, exists_classes=None):
        is_lock = system_config.system_config.get("add_class")
        if int(is_lock) == 1:
            raise ClassesLockedError()

        # 如果已有的状态为锁定
        if exists_classes is not None and exists_classes.status == ClassStatus.LOCKED:
            raise ClassesLockedError()

    async def get_classes_count(self):
        return await self.classes_dao.get_classes_count()

    async def query_classes_with_page(self, page_request: PageRequest, borough, block, school_id, grade_id, class_name,
                                      school_no=None, teacher_name=None, is_lock=None):
        paging = await self.classes_dao.query_classes_with_page(borough, block, school_id, grade_id, class_name,
                                                                page_request, school_no, teacher_name)
        # 字段映射的示例写法   , {"hash_password": "password"} ClassesSearchRes

        print(paging)
        paging_result = PaginatedResponse.from_paging(paging, ClassesSearchRes,
                                                      other_mapper={"school_name": "school_name", })
        # 字段处理
        schools = await get_school_map('id')
        # print(schools)
        grades = await get_grade_map('id')

        class_ids = []
        if paging_result.items:
            # 查询枚举值列表
            enum_value_rule = get_injector(EnumValueRule)
            grade_enums = await enum_value_rule.query_enum_values(GRADE_ENUM_KEY, '', return_keys='enum_value')
            # print(grade_enums,999)
            print(schools.keys())

            for item in paging_result.items:
                if hasattr(item, 'monitor_id') and item.monitor_id == 0:
                    item.monitor_id = None
                    pass
                class_ids.append(item.id)
                item.school_id = int(item.school_id)
                if item.grade_type in grade_enums:
                    item.grade_type_name = grade_enums[item.grade_type].description
                else:
                    item.grade_type_name = item.grade_type
                item.school_no = schools[item.school_id].school_no if item.school_id in schools.keys() else '--'
                item.grade_no = grades[item.grade_id].grade_no if item.grade_id in grades.keys() else '--'
        if len(class_ids) > 0 and is_lock is not None and is_lock > 0:
            # 批量锁定
            res = await self.classes_dao.lock_classes_by_ids(class_ids)

        convert_snowid_to_strings(paging_result,
                                  ["id", "school_id", 'grade_id', 'session_id', 'teacher_id', 'care_teacher_id'])

        return paging_result

    async def convert_import_format_to_view_model(self, item: Classes):
        # 学校转id
        # item.block = self.districts[item.block].enum_value if item.block in self.districts else  item.block
        # item.borough = self.districts[item.borough].enum_value if item.borough in self.districts else  item.borough
        if hasattr(item, 'school_name'):
            school = await self.school_dao.get_school_by_school_name(item.school_name)
            item.school_id = school.id if school else None
        if hasattr(item, 'session_name'):
            session = await self.session_dao.get_student_session_by_param(session_name=item.session_name)
            item.session_id = session.id if session else None

        if hasattr(item, 'grade_no'):
            grade = await self.grade_dao.get_grade_by_grade_name(item.grade_no)
            item.grade_id = grade.id if grade else None
        #     证件类型转英文 中小学班级类型
        if hasattr(item, 'teacher_card_type'):
            item.teacher_card_type = self.id_types.get(item.teacher_card_type, item.teacher_card_type)

        if hasattr(item, 'class_type'):
            item.class_type = self.class_systems.get(item.class_type, item.class_type)
        pass

    async def send_org_to_org_center_group(self, exists_planning_school_origin: Classes, school):
        # exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        exists_planning_school = exists_planning_school_origin
        # pprint.pprint(exists_planning_school)
        # if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
        #                                                                 (date, datetime)):
        #     exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # school = await self.school_dao.get_school_by_id(exists_planning_school_origin.school_id)
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school.school_id)
            return
        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "createdTime": '',
            "displayName": exists_planning_school.class_standard_name,
            "educateUnit": school.school_name,
            "educateUnitObj": {
                "administrativeDivisionCity": "",
                "administrativeDivisionCounty": "",
                "administrativeDivisionProvince": "",
                # "createdTime": school.created_at,
                "departmentObjs": [],
                "locationAddress": "",
                "locationCity": "",
                "locationCounty": "",
                "locationProvince": "",
                "owner": "",
                "unitCode": school.school_no,
                "unitId": "",
                "unitName": school.school_name,
                "unitType": "",
                # "updatedTime": school.updated_at
            },
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": True,
            "key": "sit",
            "manager": "",
            "name": exists_planning_school.class_standard_name,
            "newCode": exists_planning_school.class_number,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,
            "parentId": '',
            "parentName": "",
            "tags": [
                ""
            ],
            "title": exists_planning_school.class_standard_name,
            "type": "",
            "updatedTime": ''
        }

        apiname = '/api/add-group'
        # 字典参数
        datadict = dict_data
        # if isinstance(datadict['createdTime'], (date, datetime)):
        #     datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")

        datadict = convert_dates_to_strings(datadict)
        print(datadict, '字典参数')

        response = await send_orgcenter_request(apiname, datadict, 'post', True)
        print(response, '接口响应')
        try:
            print(response)

            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    async def send_org_to_org_center(self, exists_planning_school_origin: ClassesModel, res_unit=None):
        exists_planning_school = exists_planning_school_origin

        school = await self.school_dao.get_school_by_id(exists_planning_school_origin.school_id)
        grade = await self.grade_dao.get_grade_by_id(exists_planning_school_origin.grade_id)
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school.school_id)
            return
        unitid = None
        if isinstance(res_unit, dict):
            unitid = res_unit['data2']
        if unitid is None:
            unitid = school.org_center_info
        parent_id = ""

        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "displayName": exists_planning_school.class_name,
            "educateUnit": unitid if unitid is not None else school.school_name,
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": False,
            "key": "",
            "manager": "",
            "name": exists_planning_school.class_name,
            "newCode": exists_planning_school.class_number,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,
            "parentId": grade.grade_name,  # 年级编号
            # "parentName": grade.grade_name, #年级名称
            "tags": [
                ""
            ],
            "title": "",
            "type": "",
        }
        apiname = '/api/add-group-organization'
        # 字典参数
        datadict = dict_data
        datadict = convert_dates_to_strings(datadict)
        print('调用添加部门  字典参数', datadict, )
        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        try:
            print('调用添加部门 接口响应', response, )
            return response, datadict
        except Exception as e:
            print(e)
            raise e

    async def delete_class_by_school_id_and_session_id(self, school_id, session_id):
        result = await self.classes_dao.get_all_class_by_school_id(school_id, session_id)
        try:
            for item in result:
                await self.softdelete_classes(item.id)
            return True
        except Exception as e:
            print(e)
            return e
