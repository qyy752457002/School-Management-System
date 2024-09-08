# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import copy
import json
import os
import random
import traceback
from copy import deepcopy
from datetime import datetime, date

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from sqlalchemy import select, or_

from business_exceptions.institution import InstitutionExistError
from business_exceptions.planning_school import PlanningSchoolNotFoundError
from business_exceptions.school import SchoolExistsError
from daos.enum_value_dao import EnumValueDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.school_communication_dao import SchoolCommunicationDAO
from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from models.planning_school import PlanningSchool
from models.public_enum import IdentityType
from models.school import School
from models.student_transaction import AuditAction
from rules.common.common_rule import send_request, send_orgcenter_request, get_identity_by_job, \
    check_social_credit_code, check_school_no
from rules.enum_value_rule import EnumValueRule
from rules.system_rule import SystemRule
from rules.tenant_rule import TenantRule
from views.common.common_view import workflow_service_config, convert_snowid_in_model, convert_snowid_to_strings, \
    frontend_enum_mapping, convert_dates_to_strings
from views.common.constant import Constant
from views.models.extend_params import ExtendParams
from views.models.institutions import Institutions, InstitutionsImport
from views.models.organization import Organization
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus
# from rules.planning_school_rule import PlanningSchoolRule
from views.models.planning_school import PlanningSchoolTransactionAudit
from views.models.school import School as SchoolModel, SchoolKeyAddInfo, SchoolKeyInfo, SchoolPageSearch, \
    SchoolBaseInfoOptional
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, \
    SCHOOL_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, DISTRICT_ENUM_KEY, PROVINCE_ENUM_KEY, \
    CITY_ENUM_KEY, \
    PLANNING_SCHOOL_STATUS_ENUM_KEY, FOUNDER_TYPE_LV2_ENUM_KEY, SCHOOL_ORG_FORM_ENUM_KEY, FOUNDER_TYPE_LV3_ENUM_KEY, \
    FOUNDER_TYPE_ENUM_KEY, OrgCenterInstitutionType, InstitutionType
from views.models.teachers import EducateUserModel


@dataclass_inject
class SchoolRule(object):
    school_dao: SchoolDAO
    school_communication_dao: SchoolCommunicationDAO
    p_school_dao: PlanningSchoolDAO
    enum_value_dao: EnumValueDAO
    system_rule: SystemRule
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    districts = None
    enum_mapper = None
    # 定义映射关系 orm到视图的映射关系
    other_mapper = {"school_name": "institution_name",
                    "school_no": "institution_code",
                    "school_en_name": "institution_en_name",
                    "school_org_type": "institution_type",
                    "create_school_date": "create_date",
                    }

    async def get_school_by_id(self, school_id, extra_model=None):
        # other_mapper={ }
        school_db = await self.school_dao.get_school_by_id(school_id)
        if not school_db:
            return None
        if extra_model:
            school = orm_model_to_view_model(school_db, extra_model, other_mapper=self.other_mapper)
        else:
            school = orm_model_to_view_model(school_db, SchoolModel)
        convert_snowid_in_model(school, ['planning_school_id'])

        return school

    async def get_school_by_school_name(self, school_name):
        school_db = await self.school_dao.get_school_by_school_name(
            school_name)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school

    async def add_school(self,
                         school: SchoolKeyAddInfo | SchoolModel | Institutions | SchoolBaseInfoOptional | InstitutionsImport):
        exists_school = await self.school_dao.get_school_by_school_name(
            school.school_name)
        if exists_school:
            if hasattr(school, "institution_category") and school.institution_category  in [ InstitutionType.ADMINISTRATION,InstitutionType.INSTITUTION]  :
                raise InstitutionExistError()

                pass
            else:
                raise SchoolExistsError()

                pass
        if hasattr(school, "planning_school_id") and   school.planning_school_id != "" and  school.planning_school_id  is not None  :
            pschool  =await self.p_school_dao.get_planning_school_by_id(school.planning_school_id)
            if pschool:
                school.school_no = pschool.planning_school_no + str(random.randint(10, 99))
            pass
        if hasattr(school, "institution_category"):
            school_no = school.block

            if school.institution_category == InstitutionType.INSTITUTION.value:
                school_no = school_no + "X10"
            elif school.institution_category == InstitutionType.ADMINISTRATION.value:
                school_no = school_no + "X20"

            else:
                pass
            school_no = school_no + str(random.randint(100, 999))
            print('生成机构编码', school_no)
            school.school_no = school_no
        if hasattr(school, "school_no"):
            await check_school_no(school.school_no)
        school_db = view_model_to_orm_model(school, School, exclude=["id"])

        school_db.status = PlanningSchoolStatus.DRAFT.value
        school_db.created_uid = 0
        school_db.updated_uid = 0
        school_db.id = SnowflakeIdGenerator(1, 1).generate_id()
        if school.planning_school_id and school.planning_school_id > 0:
            # rule互相应用有问题  用dao
            p_exists_school_model = await self.p_school_dao.get_planning_school_by_id(school.planning_school_id)
            if not p_exists_school_model:
                raise PlanningSchoolNotFoundError()
            print(p_exists_school_model, 999)

            p_exists_school = orm_model_to_view_model(p_exists_school_model, PlanningSchoolModel)
            print(p_exists_school)

            # await school_rule.add_school_from_planning_school(exists_planning_school)
            #     p_exists_school = await p_school_rule.get_planning_school_by_id(
            #         school.planning_school_id)
            if p_exists_school:
                # 办学者
                # school_db.school_type = p_exists_school.planning_school_type
                school_db.school_edu_level = p_exists_school.planning_school_edu_level
                school_db.school_category = p_exists_school.planning_school_category
                school_db.school_operation_type = p_exists_school.planning_school_operation_type

                # school_db.school_nature = p_exists_school.planning_school_nature
                school_db.school_org_type = p_exists_school.planning_school_org_type
                school_db.school_org_form = p_exists_school.planning_school_org_form
                school_db.founder_type = p_exists_school.founder_type
                school_db.founder_type_lv2 = p_exists_school.founder_type_lv2
                school_db.founder_type_lv3 = p_exists_school.founder_type_lv3
                school_db.founder_name = p_exists_school.founder_name
                school_db.founder_code = p_exists_school.founder_code
                # school_db.urban_rural_nature = p_exists_school.planning_school_urban_rural_nature

        school_db = await self.school_dao.add_school(school_db)
        school = orm_model_to_view_model(school_db, SchoolKeyAddInfo, exclude=["created_at", 'updated_at'])
        convert_snowid_in_model(school, ['planning_school_id'])
        return school

    async def add_school_from_planning_school(self, planning_school: PlanningSchool):
        # todo 这里的值转换 用 数据库db类型直接赋值  模型转容易报错   另 其他2个表的写入  检查是否原有的  防止重复新增
        # return None

        # schooldatabaseinfo = SchoolBaseInfoOptional(**planning_school.__dict__)
        dicta = planning_school.__dict__
        dicta['school_name'] = planning_school.planning_school_name
        dicta['planning_school_id'] = planning_school.id
        dicta['school_no'] = planning_school.planning_school_no + '00'
        dicta['school_edu_level'] = planning_school.planning_school_edu_level
        dicta['school_category'] = planning_school.planning_school_category
        dicta['school_operation_type'] = planning_school.planning_school_operation_type
        dicta['school_org_type'] = planning_school.planning_school_org_type
        dicta['school_level'] = planning_school.planning_school_level
        dicta['school_code'] = planning_school.planning_school_code
        dicta['is_master'] = True

        school = SchoolKeyAddInfo(**dicta)

        res = await self.add_school(school)

        return res

    # 废弃 未使用
    async def update_school(self, school, ctype=1):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校{school.id}不存在")
        if ctype == 1:
            school_db = School()
            school_db.id = school.id
            school_db.school_no = school.school_no
            school_db.school_name = school.school_name
            school_db.block = school.block
            school_db.borough = school.borough
            # school_db.school_type = school.school_type
            school_db.school_edu_level = school.school_edu_level
            school_db.school_category = school.school_category
            school_db.school_operation_type = school.school_operation_type
            school_db.school_org_type = school.school_org_type
            school_db.school_level = school.school_level
        else:
            school_db = School()
            school_db.id = school.id
            school_db.school_name = school.school_name
            school_db.school_short_name = school.school_short_name
            school_db.school_code = school.school_code
            school_db.create_school_date = school.create_school_date
            school_db.founder_type = school.founder_type
            school_db.founder_name = school.founder_name
            school_db.urban_rural_nature = school.urban_rural_nature
            school_db.school_edu_level = school.school_edu_level
            school_db.school_org_form = school.school_org_form
            school_db.school_category = school.school_category
            school_db.school_operation_type = school.school_operation_type
            school_db.department_unit_number = school.department_unit_number
            school_db.sy_zones = school.sy_zones
            school_db.historical_evolution = school.historical_evolution

        school_db = await self.school_dao.update_school(school_db, ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school_db

    async def update_school_byargs(self, school, changed_fields: list = None,modify_status=None ):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"单位{school.id}不存在")
        # 通过指定更新的字段 来 决定是否校验 信用编码
        if changed_fields is not None:
            # 取消 和 驳回等 不校验
            if 'social_credit_code' in changed_fields:
                if hasattr(school, 'social_credit_code'):
                    await check_social_credit_code(school.social_credit_code, exists_school)
            pass
        else:
            # 默认校验
            if hasattr(school, 'social_credit_code'):
                await check_social_credit_code(school.social_credit_code, exists_school)
        if exists_school.status == PlanningSchoolStatus.DRAFT.value and modify_status:
            if hasattr(school, 'status'):
                # school.status= PlanningSchoolStatus.OPENING.value
                pass

            exists_school.status = PlanningSchoolStatus.OPENING.value
        else:
            pass

        need_update_list = []
        for key, value in school.__dict__.items():
            if key.startswith('_'):
                continue
            if value:
                need_update_list.append(key)

        school_db = await self.school_dao.update_school_byargs(school, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        school_db = deepcopy(school_db)
        convert_snowid_in_model(school_db, ['id'])

        return school_db

    async def delete_school(self, school_id):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"单位{school_id}不存在")
        school_db = await self.school_dao.delete_school(exists_school)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""], )
        return school

    async def softdelete_school(self, school_id):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"单位{school_id}不存在")
        school_db = await self.school_dao.softdelete_school(exists_school)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db

    async def get_all_schools(self):
        return await self.school_dao.get_all_schools()

    async def get_school_count(self):
        return await self.school_dao.get_school_count()

    async def query_school_with_page(self, page_request: PageRequest, school_name=None, school_no=None,
                                     school_code=None,
                                     block=None, school_level=None, borough=None, status=None, founder_type=None,
                                     founder_type_lv2=None,
                                     founder_type_lv3=None, planning_school_id=None, province=None, city=None,
                                     institution_category=None, social_credit_code=None, school_org_type=None,
                                     extra_model=None, extend_params: ExtendParams = None):
        #  根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:
                founder_type_lv2_res = await enum_value_rule.get_next_level_enum_values('founder_type', founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)

            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if founder_type_lv2 and len(founder_type_lv2) > 0:
            founder_type_lv3_res = await enum_value_rule.get_next_level_enum_values('founder_type_lv2',
                                                                                    founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao = get_injector(TenantDAO)
            # school_dao=get_injector(SchoolDAO)
            tenant = await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)

            if  tenant is   not None and  tenant.tenant_type== 'school' and tenant.code!='210100' and len(tenant.code)>=10:
                school =  await self.school_dao.get_school_by_id(tenant.origin_id)
                print('获取租户的学校对象',school)
                if school is not None:
                    school_no = school.school_no
            pass

        paging = await self.school_dao.query_school_with_page(page_request, school_name, school_no, school_code,
                                                              block, school_level, borough, status, founder_type,
                                                              founder_type_lv2,
                                                              founder_type_lv3, planning_school_id, province, city,
                                                              institution_category, social_credit_code, school_org_type,
                                                              extend_params=extend_params
                                                              )
        # 字段映射的示例写法   , {"hash_password": "password"}
        if extra_model:
            # paging.data = [extra_model(**item) for item in paging.data]
            paging_result = PaginatedResponse.from_paging(paging, extra_model, other_mapper=self.other_mapper)

        else:
            paging_result = PaginatedResponse.from_paging(paging, SchoolModel)
        convert_snowid_to_strings(paging_result, ['planning_school_id'])

        return paging_result

    async def update_school_status(self, school_id, status, action=None):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"单位{school_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status == PlanningSchoolStatus.NORMAL.value and exists_school.status == PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_school.status = PlanningSchoolStatus.NORMAL.value
        elif status == PlanningSchoolStatus.CLOSED.value and exists_school.status == PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_school.status = PlanningSchoolStatus.CLOSED.value
        else:
            # exists_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"单位当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_school.status,2222222)
        school_db = await self.school_dao.update_school_byargs(exists_school, *need_update_list)

        # school_db = await self.school_dao.update_school_status(exists_school,status)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db

    # 搜索使用
    async def query_schools(self, school_name, extend_params: ExtendParams | None, school_id=None, block=None,
                            borough=None, institution_category=None, extra_model=None):
        # block,borough
        session = await db_connection_manager.get_async_session("default", True)
        query = select(School)
        if institution_category:
            if isinstance(institution_category, list):
                query = query.where(School.institution_category.in_(institution_category))
            else:
                query = query.where(School.institution_category == institution_category)
        if school_name:
            if ',' in school_name:
                school_name = school_name.split(',')
                if isinstance(school_name, list):
                    query = query.where(School.school_name.in_(school_name))
            else:
                query = query.where(School.school_name.like(f'%{school_name}%'))
        if school_id:
            if ',' in school_id:
                school_id = school_id.split(',')
                if isinstance(school_id, list):
                    query = query.where(School.id.in_(school_id))
            else:
                query = query.where(School.id == school_id)
        if block:
            if ',' in block:
                block = block.split(',')
                if isinstance(block, list):
                    query = query.where(School.block.in_(block))
            else:
                query = query.where(School.block.like(f'%{block}%'))
        if borough:
            if ',' in borough:
                borough = borough.split(',')
                if isinstance(borough, list):
                    query = query.where(School.borough.in_(borough))
            else:
                query = query.where(School.borough.like(f'%{borough}%'))
        # print(extend_params,3333333333)
        if extend_params:
            if extend_params.school_id:
                # query = query.where(School.id == int(extend_params.school_id))
                pass
            if extend_params.planning_school_id:
                query = query.where(School.planning_school_id == int(extend_params.planning_school_id))

            if extend_params.county_name:
                # 区的转换   or todo
                # enuminfo = await self.enum_value_dao.get_enum_value_by_value(extend_params.county_id, 'country' )
                query = query.filter(
                    or_(School.block == extend_params.county_name, School.borough == extend_params.county_name))

                # if enuminfo:
                pass
            if extend_params.system_type:
                pass

        result = await session.execute(query)
        res = result.scalars().all()

        lst = []
        for row in res:
            if extra_model:

                planning_school = orm_model_to_view_model(row, extra_model, other_mapper=self.other_mapper)
            else:
                planning_school = orm_model_to_view_model(row, SchoolModel)

            # account = PlanningSchool(school_id=row.school_id,
            #                  grade_no=row.grade_no,
            #                  grade_name=row.grade_name,
            #                  grade_alias=row.grade_alias,
            #                  description=row.description)
            lst.append(planning_school)
        return lst

    # 向工作流中心发送申请
    async def add_school_work_flow(self, school_flow: SchoolModel, ):
        # school_flow.id=0
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        data = school_flow
        datadict = data.__dict__
        datadict['process_code'] = SCHOOL_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        datadict['founder_type_lv3'] = school_flow.founder_type_lv3
        datadict['block'] = school_flow.block
        datadict['borough'] = school_flow.borough
        datadict['school_level'] = school_flow.school_level
        datadict['school_no'] = school_flow.school_no
        datadict['apply_user'] = 'tester'
        dicta = school_flow.__dict__
        dicta['school_id'] = school_flow.id

        datadict['json_data'] = json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url = url + apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict, headerdict)
        response = None
        try:
            response = await httpreq.post_json(url, datadict, headerdict)
            print('请求工作流结果', response)
        except Exception as e:
            print(e)
        return response

    async def add_school_close_work_flow(self, school_flow: PlanningSchoolModel, action_reason, related_license_upload):
        # school_flow.id=0
        data = school_flow
        datadict = data.__dict__
        datadict['process_code'] = SCHOOL_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        datadict['founder_type_lv3'] = school_flow.founder_type_lv3
        datadict['block'] = school_flow.block
        datadict['borough'] = school_flow.borough
        datadict['school_level'] = school_flow.school_level
        datadict['school_no'] = school_flow.school_no

        datadict['apply_user'] = 'tester'
        dicta = school_flow.__dict__
        dicta['action_reason'] = action_reason
        dicta['related_license_upload'] = related_license_upload
        dicta['school_id'] = school_flow.id

        datadict['json_data'] = json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'

        response = None
        try:
            response = await send_request(apiname, datadict, 'post')
            print('请求工作流结果', response)
        except Exception as e:
            print(e)
        return response

    async def req_workflow_audit(self, audit_info: PlanningSchoolTransactionAudit, action):
        if audit_info.transaction_audit_action == AuditAction.PASS.value:
            # 成功则写入数据
            res2 = await self.deal_school(audit_info.process_instance_id, action)
        # 发起审批流的 处理

        datadict = dict()
        if audit_info.process_instance_id > 0:
            node_id = await self.system_rule.get_work_flow_current_node_by_process_instance_id(
                audit_info.process_instance_id)
            audit_info.node_id = node_id['node_instance_id']

        # 节点实例id
        datadict['node_instance_id'] = audit_info.node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # from urllib.parse import urlencode
        # apiname += ('?' + urlencode(datadict))

        # 如果是query 需要拼接参数

        # 字典参数
        datadict = {"user_id": "11", "action": "approved", **datadict}
        if audit_info.transaction_audit_action == AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if audit_info.transaction_audit_action == AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await send_request(apiname, datadict, 'post', True)
        print(response, '接口响应')

        # 终态的处理

        await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)

        return response
        pass

    async def send_school_to_org_center_by_school_no(self, school_no):
        """
        一期同步过来的数据送到组织中心
        """
        school = await self.school_dao.get_school_by_school_no_to_org(school_no)
        if not school:
            raise Exception(f"单位{school_no}不存在")
        # 单位发送过去
        res_unit, data_unit = await self.send_school_to_org_center(school)
        # 单位的组织 对接
        await self.send_unit_orgnization_to_org_center(school, data_unit)
        # 添加组织结构 部门
        org = Organization(org_name=school.school_name,
                           school_id=school.id,
                           org_type='校',
                           parent_id=0,
                           org_code=school.school_no,
                           )
        # 部门对接
        res_org, data_org = await self.send_org_to_org_center(org, res_unit)
        # 管理员 对接
        res_admin = await self.send_admin_to_org_center(school, data_org)
        # 添加 用户和组织关系 就是部门
        await self.send_user_org_relation_to_org_center(school, res_unit, data_org, res_admin)
        return True

    async def deal_school(self, process_instance_id, action, ):
        #  读取流程实例ID
        school = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到学校信息', process_instance_id)
            return
        if action == 'open':
            res = await self.update_school_status(school.id, PlanningSchoolStatus.NORMAL.value, 'open')
            try:
                # 单位发送过去
                res_unit, data_unit = await self.send_school_to_org_center(school)
                # 单位的组织 对接
                res_oigna = await self.send_unit_orgnization_to_org_center(school, data_unit)
                # 服务单位
                # res_oigna_service_unit = await self.send_service_unit_to_org_center(school, data_unit)

                # 添加组织结构 部门
                org = Organization(org_name=school.school_name,
                                   school_id=school.id,
                                   org_type='校',
                                   parent_id=0,
                                   org_code=school.school_no,
                                   )
                # 部门对接
                res_org, data_org = await self.send_org_to_org_center(org, res_unit)
                # 管理员 对接
                res_admin = await self.send_admin_to_org_center(school, data_org)
                # 添加 用户和组织关系 就是部门
                await self.send_user_org_relation_to_org_center(school, res_unit, data_org, res_admin)
                #     todo 自懂获取秘钥
                tenant_rule = get_injector(TenantRule)
                print('开始 获取租户信息-单位')
                await tenant_rule.sync_tenant_all(school.id)

            except Exception as e:
                print('异常', e)
                traceback.print_exc()
                # raise e

        if action == 'close':
            res = await self.update_school_status(school.id, PlanningSchoolStatus.CLOSED.value, 'close')
        if action == 'keyinfo_change':
            # todo 把基本信息变更 改进去
            # res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data = JsonUtils.json_str_to_dict(result.get('json_data'))
            print(json_data)
            planning_school_orm = SchoolKeyInfo(**json_data)
            planning_school_orm.id = school.id

            res = await self.update_school_byargs(planning_school_orm)
            pass

        # res = await self.update_school_status(school_id,  PlanningSchoolStatus.NORMAL.value, 'open')
        pass

    async def add_school_keyinfo_change_work_flow(self, school_flow: SchoolKeyInfo, process_code=None):
        # school_flow.id=0
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        data = school_flow
        datadict = data.__dict__
        datadict['process_code'] = SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        if process_code:
            datadict['process_code'] = process_code
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['school_no'] = school_flow.school_no

        datadict['school_name'] = school_flow.school_name
        datadict['school_edu_level'] = school_flow.school_edu_level
        datadict['block'] = school_flow.block
        datadict['borough'] = school_flow.borough
        datadict['school_level'] = school_flow.school_level
        datadict['school_category'] = school_flow.school_category
        datadict['school_operation_type'] = school_flow.school_operation_type
        datadict['school_org_type'] = school_flow.school_org_type

        datadict['apply_user'] = 'tester'
        mapa = school_flow.__dict__
        mapa['school_id'] = school_flow.id
        datadict['json_data'] = json.dumps(mapa, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url = url + apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict, headerdict)
        response = None
        try:
            response = await httpreq.post_json(url, datadict, headerdict)
            print('请求工作流结果', response)
        except Exception as e:
            print(e)
        return response

    async def req_workflow_cancel(self, node_id, process_instance_id=None):

        # 发起审批流的 处理
        datadict = dict()
        # 节点实例id    自动获取
        if process_instance_id > 0:
            node_id = await self.system_rule.get_work_flow_current_node_by_process_instance_id(process_instance_id)
            node_id = node_id['node_instance_id']

        datadict['node_instance_id'] = node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # 字典参数
        # datadict ={"user_id":"11","action":"revoke"}
        datadict = {"user_id": "11", "action": "revoke", **datadict}

        response = await send_request(apiname, datadict, 'post', True)

        print(response, '接口响应')
        # 终态的处理

        await self.set_transaction_end(process_instance_id, AuditAction.CANCEL)

        return response
        pass

    async def set_transaction_end(self, process_instance_id, status):
        tinfo = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status = status.value
            if status == AuditAction.PASS.value:
                await self.update_school_byargs(tinfo, )

                pass
            else:
                # 不校验
                await self.update_school_byargs(tinfo, ['workflow_status'])

        pass

    async def is_can_not_add_workflow(self, student_id, is_all_status_allow=False):
        tinfo = await self.get_school_by_id(student_id)
        if not is_all_status_allow:
            if tinfo and tinfo.status == PlanningSchoolStatus.DRAFT.value:
                return True
        # 检查是否有占用
        if tinfo and tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
            return True
        return False

    async def school_export(self, task: Task):
        bucket = 'school'

        print(bucket, '桶')

        export_params: SchoolPageSearch = (
            task.payload if task.payload is SchoolPageSearch() else SchoolPageSearch()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"school_export_{shortuuid.uuid()}.xlsx"
        # 获取当前脚本所在目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取当前脚本所在目录的父目录
        parent_dir = os.path.dirname(script_dir)

        # 构建与 script_dir 并列的 temp 目录的路径
        temp_dir_path = os.path.join(parent_dir, 'temp')

        # 确保 temp 目录存在，如果不存在则创建它
        os.makedirs(temp_dir_path, exist_ok=True)
        temp_file_path = os.path.join(temp_dir_path, random_file_name)
        while True:
            # todo  这里的参数需要 解包
            paging = await self.school_dao.query_school_with_page(
                page_request, export_params.school_name, export_params.school_no, export_params.school_code,
                export_params.block, export_params.school_level, export_params.borough, export_params.status,
                export_params.founder_type,
                export_params.founder_type_lv2,
                export_params.founder_type_lv3, export_params.planning_school_id, export_params.province,
                export_params.city, export_params.institution_category,
            )
            paging_result = PaginatedResponse.from_paging(
                paging, SchoolBaseInfoOptional, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            await self.convert_school_to_export_format(paging_result)
            logger.info('分页的结果条数', len(paging_result.items))

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
            task_result.result_id = shortuuid.uuid()

            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id = 0
            print('拼接数据task_result ', task_result)

            resadd = await self.task_dao.add_task_result(task_result, True)

            print('task_result写入结果', resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result

    async def is_can_change_keyinfo(self, student_id, ):
        tinfo = await self.get_school_by_id(student_id)
        print('当前信息', tinfo)
        if tinfo and tinfo.status == PlanningSchoolStatus.DRAFT.value:
            return True
        if tinfo and tinfo.status != PlanningSchoolStatus.NORMAL.value:
            # return  True

            # 检查是否有占用 如果有待处理的流程ID 则锁定
            if tinfo and tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
                return False
            return True
        if tinfo and tinfo.status == PlanningSchoolStatus.CLOSED.value:
            return False
        return True

    #     枚举初始化的方法
    async def init_enum_value_rule(self):
        enum_value_rule = get_injector(EnumValueRule)
        self.districts = await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY, Constant.CURRENT_CITY,
                                                                 return_keys='description')
        print('区域', self.districts)
        self.enum_mapper = {value: key for key, value in frontend_enum_mapping.items()}
        print('枚举映射', self.enum_mapper)
        return self

    async def convert_school_to_import_format(self, item):
        item.block = self.districts[item.block].enum_value if item.block in self.districts else item.block
        item.borough = self.districts[item.borough].enum_value if item.borough in self.districts else item.borough
        if hasattr(item, 'planning_school_edu_level'):
            item.planning_school_edu_level = self.enum_mapper[
                item.planning_school_edu_level] if item.planning_school_edu_level in self.enum_mapper.keys() else item.planning_school_edu_level
        if hasattr(item, 'planning_school_category'):
            value = item.planning_school_category
            if value and isinstance(value, str) and value.find('-') != -1:
                temp = value.split('-')
                item.planning_school_category = temp[1] if len(temp) > 1 else value

            item.planning_school_category = self.enum_mapper[
                item.planning_school_category] if item.planning_school_category in self.enum_mapper.keys() else item.planning_school_category
        if hasattr(item, 'planning_school_org_type'):
            item.planning_school_org_type = self.enum_mapper[
                item.planning_school_org_type] if item.planning_school_org_type in self.enum_mapper.keys() else item.planning_school_org_type
        pass

    #     定义方法吧一行记录转化为适合导出展示的格式
    async def convert_school_to_export_format(self, paging_result):
        # 获取区县的枚举
        enum_value_rule = get_injector(EnumValueRule)
        provinces = await enum_value_rule.query_enum_values(PROVINCE_ENUM_KEY, None, return_keys='enum_value')
        citys = await enum_value_rule.query_enum_values(CITY_ENUM_KEY, None, return_keys='enum_value')
        districts = await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY, Constant.CURRENT_CITY,
                                                            return_keys='enum_value')
        planningschool_status = await enum_value_rule.query_enum_values(PLANNING_SCHOOL_STATUS_ENUM_KEY, None,
                                                                        return_keys='enum_value')
        founder_type = await enum_value_rule.query_enum_values(FOUNDER_TYPE_ENUM_KEY, None, return_keys='enum_value')
        founder_type_lv2 = await enum_value_rule.query_enum_values(FOUNDER_TYPE_LV2_ENUM_KEY, None,
                                                                   return_keys='enum_value')
        founder_type_lv3 = await enum_value_rule.query_enum_values(FOUNDER_TYPE_LV3_ENUM_KEY, None,
                                                                   return_keys='enum_value')
        school_org_form = await enum_value_rule.query_enum_values(SCHOOL_ORG_FORM_ENUM_KEY, None,
                                                                  return_keys='enum_value')
        print('区域', districts, '')
        enum_mapper = frontend_enum_mapping
        # todo 这4个 目前 城乡类型 逗号3级   教学点类型 经济属性 民族属性
        if hasattr(paging_result, 'items'):
            # print('paging_result.items',paging_result.items)
            for item in paging_result.items:
                # item.approval_status =  item.approval_status.value
                delattr(item, 'id')
                delattr(item, 'created_uid')
                if hasattr(item, 'province'):
                    item.province = provinces[
                        item.province].description if item.province in provinces else item.province
                if hasattr(item, 'city'):
                    item.city = citys[item.city].description if item.city in citys else item.city
                item.block = districts[item.block].description if item.block in districts else item.block
                item.borough = districts[item.borough].description if item.borough in districts else item.borough
                item.school_edu_level = enum_mapper[
                    item.school_edu_level] if item.school_edu_level in enum_mapper.keys() else item.school_edu_level
                item.school_category = enum_mapper[
                    item.school_category] if item.school_category in enum_mapper.keys() else item.school_category
                item.school_operation_type = enum_mapper[
                    item.school_operation_type] if item.school_operation_type in enum_mapper.keys() else item.school_operation_type
                item.school_org_type = enum_mapper[
                    item.school_org_type] if item.school_org_type in enum_mapper.keys() else item.school_org_type
                item.school_level = enum_mapper[
                    item.school_level] if item.school_level in enum_mapper.keys() else item.school_level
                # item.status = PlanningSchoolStatus[item.status] if item.status in enum_mapper.keys() else  item.status
                item.status = planningschool_status[
                    item.status].description if item.status in planningschool_status else item.status
                item.founder_type = founder_type[
                    item.founder_type].description if item.founder_type in founder_type else item.founder_type
                item.founder_type_lv2 = founder_type_lv2[
                    item.founder_type_lv2].description if item.founder_type_lv2 in founder_type_lv2 else item.founder_type_lv2
                item.founder_type_lv3 = founder_type_lv3[
                    item.founder_type_lv3].description if item.founder_type_lv3 in founder_type_lv3 else item.founder_type_lv3
                # print('枚举映射',item)
                if item.school_org_form:
                    item.school_org_form = school_org_form[
                        item.school_org_form].description if item.school_org_form in school_org_form else item.school_org_form

                pass
        else:
            item = paging_result
            delattr(item, 'id')
            delattr(item, 'created_uid')
            if hasattr(item, 'province'):
                item.province = provinces[item.province].description if item.province in provinces else item.province
            if hasattr(item, 'city'):
                item.city = citys[item.city].description if item.city in citys else item.city
            item.block = districts[item.block].description if item.block in districts else item.block
            item.borough = districts[item.borough].description if item.borough in districts else item.borough
            item.school_edu_level = enum_mapper[
                item.school_edu_level] if item.school_edu_level in enum_mapper.keys() else item.school_edu_level
            item.school_category = enum_mapper[
                item.school_category] if item.school_category in enum_mapper.keys() else item.school_category
            item.school_operation_type = enum_mapper[
                item.school_operation_type] if item.school_operation_type in enum_mapper.keys() else item.school_operation_type
            item.school_org_type = enum_mapper[
                item.school_org_type] if item.school_org_type in enum_mapper.keys() else item.school_org_type
            item.school_level = enum_mapper[
                item.school_level] if item.school_level in enum_mapper.keys() else item.school_level
            # item.status = PlanningSchoolStatus[item.status] if item.status in enum_mapper.keys() else  item.status
            item.status = planningschool_status[
                item.status].description if item.status in planningschool_status else item.status
            item.founder_type = founder_type[
                item.founder_type].description if item.founder_type in founder_type else item.founder_type
            item.founder_type_lv2 = founder_type_lv2[
                item.founder_type_lv2].description if item.founder_type_lv2 in founder_type_lv2 else item.founder_type_lv2
            item.founder_type_lv3 = founder_type_lv3[
                item.founder_type_lv3].description if item.founder_type_lv3 in founder_type_lv3 else item.founder_type_lv3
            # print('枚举映射',item)
            if item.school_org_form:
                item.school_org_form = school_org_form[
                    item.school_org_form].description if item.school_org_form in school_org_form else item.school_org_form
            # return paging_result

        # 发送规划校到组织中心的方法

    # 单位对接
    async def send_school_to_org_center(self, exists_planning_school_origin: School):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer
        planning_school_communication = await self.school_communication_dao.get_school_communication_by_school_id(
            exists_planning_school.id)
        cn_exists_planning_school = await self.convert_school_to_export_format(exists_planning_school)
        # todo 多组织 是否支持逗号分隔
        dict_data = {
            'administrativeDivisionCity': '',
            'administrativeDivisionCounty': exists_planning_school.block,
            'administrativeDivisionProvince': planning_school_communication.loc_area_pro,
            'createdTime': exists_planning_school.create_school_date,
            'locationAddress': planning_school_communication.detailed_address,
            'locationCity': '',
            'locationCounty': planning_school_communication.loc_area,
            'locationProvince': planning_school_communication.loc_area_pro,
            'owner': exists_planning_school.school_no,
            # 单位的唯一标识 是code
            'unitCode': exists_planning_school.school_no, 'unitId': '',
            'unitName': exists_planning_school.school_name,
            'unitType': OrgCenterInstitutionType.get_mapper(
                exists_planning_school.institution_category) if exists_planning_school.institution_category else 'school',
            'updatedTime': exists_planning_school.updated_at

        }

        apiname = '/api/add-educate-unit'
        # 字典参数
        datadict = dict_data
        if isinstance(datadict['createdTime'], (date, datetime)):
            datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")

        # if isinstance(datadict['createdTime'], (date, datetime)):
        #     datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")
        datadict = convert_dates_to_strings(datadict)
        print(datadict, '字典参数')

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        try:
            print('发送单位', response)
            # 单位id更新到表里
            if isinstance(response, dict):
                unitid = response['data2'] if 'data2' in response.keys() else ''
                exists_planning_school_origin.org_center_info = unitid
                need_update_list = []
                need_update_list.append('org_center_info')
                datadict['unitId'] = unitid
                await self.school_dao.update_school_byargs(exists_planning_school_origin, *need_update_list)
            return response, datadict

            # return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    # 用户对接
    async def send_admin_to_org_center(self, exists_planning_school_origin, data_org):

        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        school = exists_planning_school
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school)
            return
        school_operation_type = []
        if school:
            school = orm_model_to_view_model(school, SchoolModel)
            if school.school_edu_level:
                school_operation_type.append(school.school_edu_level)
            if school.school_category:
                school_operation_type.append(school.school_category)
            if school.school_operation_type:
                school_operation_type.append(school.school_operation_type)
        identity_type, identity = await get_identity_by_job(school_operation_type, '')

        school = await self.school_dao.get_school_by_id(
            exists_planning_school_origin.id)
        # 学校综合管理系统  教育单位管理系统
        # 'unitType': ,

        dict_data = EducateUserModel(**exists_planning_school_origin.__dict__,
                                     # 所在单位
                                     currentUnit=school.org_center_info,
                                     createdTime=exists_planning_school_origin.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     updatedTime=exists_planning_school_origin.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     name=exists_planning_school_origin.admin_phone,
                                     # 组织
                                     owner=exists_planning_school_origin.school_no,
                                     userCode=exists_planning_school_origin.admin,
                                     # userId=exists_planning_school_origin.admin_phone,
                                     phoneNumber=exists_planning_school_origin.admin_phone,
                                     # 部门group 的显示名字
                                     departmentNames=data_org['displayName'],
                                     # 部门group的name
                                     departmentId=data_org['name'],
                                     realName=exists_planning_school_origin.admin,
                                     identity=identity,
                                     identityType=IdentityType.STAFF.value,
                                     user_account_status='active',

                                     sourceApp='教育单位管理系统' if exists_planning_school.institution_category in [
                                         InstitutionType.ADMINISTRATION.value,
                                         InstitutionType.INSTITUTION.value] else '学校综合管理系统'
                                     )
        dict_data = dict_data.__dict__
        # params_data = JsonUtils.dict_to_json_str(dict_data)
        api_name = '/api/add-educate-user'
        # 字典参数
        datadict = dict_data
        print(datadict, '参数')
        response = await send_orgcenter_request(api_name, datadict, 'post', False)
        print('  管理员 对接 ', response, )
        try:
            # print(response)
            return response
        except Exception as e:
            print(e)
            raise e
            return response
        return None

    # # 单位的组织 对接
    async def send_unit_orgnization_to_org_center(self, exists_planning_school_origin: School, data_unit):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer  orgType组织类型 -必填 administrative_unit|public_institutions|school|developer
        planning_school_communication = await self.school_communication_dao.get_school_communication_by_school_id(
            exists_planning_school.id)

        school = await self.school_dao.get_school_by_id(
            exists_planning_school.id)
        # cn_exists_planning_school = await self.convert_school_to_import_format(exists_planning_school)
        dict_data = {'administrativeDivisionCity': '',
                     'administrativeDivisionCounty': exists_planning_school.block,
                     'administrativeDivisionProvince': '',
                     'createdTime': exists_planning_school.create_school_date,
                     'locationAddress': planning_school_communication.detailed_address,
                     'locationCity': '',
                     'locationCounty': planning_school_communication.loc_area,
                     'locationProvince': planning_school_communication.loc_area_pro, 'owner': '',
                     # 组织的唯一标识 可能是 单位code
                     'unitCode': exists_planning_school.school_no,
                     # 'unitId': '',
                     'unitName': exists_planning_school.school_name,
                     # 'unitType': 'school', todo 需要调试
                     'unitType': OrgCenterInstitutionType.get_mapper(
                         exists_planning_school.institution_category) if exists_planning_school.institution_category else 'school',
                     'updatedTime': exists_planning_school.updated_at,
                     # "appHomeUrl": "http://tgiibjya.nr/xxhsh",
                     # "appName": exists_planning_school.planning_school_name,

                     "educateUnits": [
                         data_unit
                     ],
                     "certPublicKey": "",
                     "clientId": "",
                     "clientSecret": "",
                     # 组织的code
                     "code": exists_planning_school.school_no,
                     # "defaultApplication":   exists_planning_school.planning_school_name,
                     "defaultAvatar": "",
                     "defaultPassword": "",
                     "displayName": exists_planning_school.school_name,
                     "logo": "",
                     # 这里会决定放入哪个应用
                     "orgType": OrgCenterInstitutionType.get_mapper(
                         exists_planning_school.institution_category) if exists_planning_school.institution_category else 'school',
                     "overview": "",
                     "status": "",
                     "unitCount": "",
                     # "unitId": exists_planning_school.planning_school_no,

                     }
        #  URL修改
        apiname = '/api/add-org'
        # 字典参数
        datadict = dict_data
        if isinstance(datadict['createdTime'], (date, datetime)):
            datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")

        # if isinstance(datadict['createdTime'], (date, datetime)):
        #     datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")
        datadict = convert_dates_to_strings(datadict)
        print(datadict, '字典参数')
        print('发起请求组织到组织中心')

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print(response)
            # if response['status'] == OrgCenterApiStatus.ERROR.value and is_check_force:
            #     print('同步组织中心失败')
            #     raise OrgCenterApiError()
            print('组织添加suc')

            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    # 部门对接
    async def send_org_to_org_center(self, exists_planning_school_origin: Organization, res_unit):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer

        school = await self.school_dao.get_school_by_id(exists_planning_school.school_id)
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school.school_id)
            return
        unitid = None
        if isinstance(res_unit, dict):
            unitid = res_unit['data2']
        dict_data = {
            "contactEmail": "j.vyevxiloyy@qq.com",
            "displayName": exists_planning_school.org_name,
            # todo  参数调试  单位ID
            "educateUnit": unitid if unitid is not None else school.school_name,
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": exists_planning_school.parent_id == 0,
            "key": "sit",
            "manager": "",
            "name": exists_planning_school.org_name + "默认部门",
            # "name":  exists_planning_school_origin.org_name,
            # 名称唯一
            "newCode": exists_planning_school.org_code,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.school_no,  # 隶属的组织  是 自动的 组织
            "parentId": str(exists_planning_school.parent_id),  # 0表示顶级部门
            "parentName": "",
            "tags": [
                ""
            ],
            "title": exists_planning_school.org_name,
            # todo 可能这个字段  待定
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
            return response

        return None

    #   # 添加 用户和组织关系 就是部门
    async def send_user_org_relation_to_org_center(self, exists_planning_school_origin: Organization, res_unit,
                                                   data_org, res_admin):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer
        # school = await self.planning_school_dao.get_planning_school_by_id(exists_planning_school.school_id)
        school = exists_planning_school
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school)
            return
        school_operation_type = []
        if school:
            school = orm_model_to_view_model(school, SchoolModel)
            if school.school_edu_level:
                school_operation_type.append(school.school_edu_level)
            if school.school_category:
                school_operation_type.append(school.school_category)
            if school.school_operation_type:
                school_operation_type.append(school.school_operation_type)
        identity_type, identity = await get_identity_by_job(school_operation_type, '')

        unitid = None
        userid = None
        if isinstance(res_unit, dict):
            unitid = res_unit['data2']
        if isinstance(res_admin, dict):
            userid = res_admin['data2']
        #
        dict_data = {
            "createdTime": "1989-05-20 17:50:56",
            "departmentId": data_org['name'],
            "identity": identity,
            "identityType": IdentityType.STAFF.value,
            # 单位和用户ID
            # "unitId": "74",
            "userId": userid,
            "unitId": unitid if unitid is not None else school.school_name,
        }

        apiname = '/api/add-educate-user-department-identitys'
        # 字典参数 todo  调整  参数完善   另 服务范围的接口
        datadict = [dict_data]
        # datadict = convert_dates_to_strings(datadict)
        print('调用添加部门用户关系  字典参数', datadict, )

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print('调用添加部门用户关系 接口响应', response, )
        try:

            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    # 发送 服务单位 给 组织中心
    async def send_service_unit_to_org_center(self, exists_planning_school_origin: School, data_unit):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)

        school = await self.school_dao.get_school_by_id(
            exists_planning_school.id)
        dict_data = {
            # 组织的code

            'orgCode': exists_planning_school.school_no,

            'unitId': school.org_center_info,

        }
        #  URL修改
        apiname = '/api/add-service-unit'
        # 字典参数
        datadict = dict_data

        datadict = convert_dates_to_strings(datadict)
        print(datadict, '字典参数')
        print('发起请求服务单位到组织中心')

        response = await send_orgcenter_request(apiname, datadict, 'post', True)
        print(response, '接口响应')
        try:
            print(response)
            # if response['status'] == OrgCenterApiStatus.ERROR.value and is_check_force:
            #     print('同步组织中心失败')
            #     raise OrgCenterApiError()
            print('服务单位添加suc')

            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    # 获取区教育局
    async def get_country_edu_institution_by_code(self, tenant_code):
        school = await self.school_dao.get_school_by_args(block=tenant_code, planning_school_id=0)

        return school
