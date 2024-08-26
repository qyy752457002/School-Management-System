import copy
import json
import os
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
from sqlalchemy import select

from business_exceptions.common import OrgCenterApiError
from business_exceptions.planning_school import PlanningSchoolNotFoundError, \
    PlanningSchoolNotFoundByProcessInstanceIdError, PlanningSchoolExistsError, PlanningSchoolStatusError
from daos.enum_value_dao import EnumValueDAO
from daos.planning_school_communication_dao import PlanningSchoolCommunicationDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.planning_school_eduinfo_dao import PlanningSchoolEduinfoDAO
from models.planning_school import PlanningSchool
from models.public_enum import IdentityType
from models.student_transaction import AuditAction
from rules import enum_value_rule
from rules.common.common_rule import send_request, send_orgcenter_request, get_identity_by_job, check_social_credit_code
from rules.enum_value_rule import EnumValueRule
from rules.school_communication_rule import SchoolCommunicationRule
from rules.school_eduinfo_rule import SchoolEduinfoRule
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config, convert_snowid_to_strings, convert_snowid_in_model, \
    frontend_enum_mapping, convert_dates_to_strings
from views.common.constant import Constant
from views.models.organization import Organization
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus, \
    PlanningSchoolKeyInfo, PlanningSchoolTransactionAudit, PlanningSchoolPageSearch, \
    PlanningSchoolOptional
from views.models.planning_school import PlanningSchoolBaseInfo
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.system import PLANNING_SCHOOL_OPEN_WORKFLOW_CODE, \
    PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE, PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, DISTRICT_ENUM_KEY, \
    PROVINCE_ENUM_KEY, CITY_ENUM_KEY, PLANNING_SCHOOL_STATUS_ENUM_KEY, FOUNDER_TYPE_ENUM_KEY, FOUNDER_TYPE_LV2_ENUM_KEY, \
    FOUNDER_TYPE_LV3_ENUM_KEY, SCHOOL_ORG_FORM_ENUM_KEY, OrgCenterApiStatus
from views.models.teachers import EducateUserModel


@dataclass_inject
class PlanningSchoolRule(object):
    planning_school_dao: PlanningSchoolDAO
    enum_value_dao: EnumValueDAO
    system_rule: SystemRule
    file_storage_dao: FileStorageDAO
    task_dao: TaskDAO
    planning_school_communication_dao: PlanningSchoolCommunicationDAO
    planning_school_eduinfo_dao: PlanningSchoolEduinfoDAO
    other_mapper = {"school_name": "planning_school_name",
                    "school_code": "planning_school_no",
                    "school_edu_level": "planning_school_edu_level",
                    "school_category": "planning_school_category",
                    "school_org_type": "planning_school_org_type",
                    }
    districts = None
    enum_mapper = None

    async def get_planning_school_by_id(self, planning_school_id, extra_model=None):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not planning_school_db:
            raise PlanningSchoolNotFoundError()
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel)
        # str
        convert_snowid_in_model(planning_school)

        if extra_model:
            planning_school_extra = orm_model_to_view_model(planning_school_db, extra_model,
                                                            exclude=[""])
            convert_snowid_in_model(planning_school_extra)

            return planning_school, planning_school_extra

        else:
            return planning_school

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school_name)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def add_planning_school(self, planning_school: PlanningSchoolModel | PlanningSchoolOptional):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school.planning_school_name)
        if exists_planning_school:
            raise PlanningSchoolExistsError()

        # 校验编码 不能重复
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_args(planning_school_no=planning_school.planning_school_no)
        if exists_planning_school:
            raise PlanningSchoolExistsError()
        # 检查社会信用编码唯一
        # exists_planning_school = await self.planning_school_dao.get_planning_school_by_args(social_credit_code=planning_school.social_credit_code)


        planning_school_db = view_model_to_orm_model(planning_school, PlanningSchool, exclude=["id"])
        planning_school_db.status = PlanningSchoolStatus.DRAFT.value
        planning_school_db.created_uid = 0
        planning_school_db.updated_uid = 0
        planning_school_db.id = SnowflakeIdGenerator(1, 1).generate_id()
        if planning_school.province and len(planning_school.province) > 0:
            pass
        else:
            planning_school.province = "210000"
        if planning_school.city and len(planning_school.city) > 0:
            pass
        else:
            planning_school.city = "210100"

        planning_school_db = await self.planning_school_dao.add_planning_school(planning_school_db)
        print('id 111', planning_school_db.id)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel,
                                                  exclude=["created_at", 'updated_at', ])
        # str
        convert_snowid_in_model(planning_school)
        return planning_school

    async def delete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.delete_planning_school(exists_planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""], )
        return planning_school

    async def softdelete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.softdelete_planning_school(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db

    async def get_all_planning_schools(self):
        return await self.planning_school_dao.get_all_planning_schools()

    async def get_planning_school_count(self):
        return await self.planning_school_dao.get_planning_school_count()

    async def query_planning_school_with_page(self, page_request: PageRequest, planning_school_name, planning_school_no,
                                              planning_school_code,
                                              block, planning_school_level, borough, status, founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3, extend_params=None):
        # todo 根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res = await enum_value_rule.get_next_level_enum_values('founder_type', founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)

            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if len(founder_type_lv2) > 0:
            founder_type_lv3_res = await enum_value_rule.get_next_level_enum_values('founder_type_lv2',
                                                                                    founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.planning_school_dao.query_planning_school_with_page(page_request, planning_school_name,
                                                                                planning_school_no,
                                                                                planning_school_code,
                                                                                block, planning_school_level, borough,
                                                                                status, founder_type,
                                                                                founder_type_lv2,
                                                                                founder_type_lv3, extend_params)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolModel)
        # str
        convert_snowid_to_strings(paging_result)
        return paging_result

    async def update_planning_school_status(self, planning_school_id, target_status, action=None):

        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        # 判断原来的状态+要更改的状态 进行后续的更新
        if target_status == PlanningSchoolStatus.NORMAL.value and exists_planning_school.status == PlanningSchoolStatus.OPENING.value:
            # 开办 自动创建一条学校信息
            exists_planning_school.status = PlanningSchoolStatus.NORMAL.value
        elif target_status == PlanningSchoolStatus.CLOSED.value and exists_planning_school.status == PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_planning_school.status = PlanningSchoolStatus.CLOSED.value
        else:
            # exists_planning_school.status= PlanningSchoolStatus.OPENING.value
            raise PlanningSchoolStatusError()

        need_update_list = []
        need_update_list.append('status')

        print(exists_planning_school.status, 2222222)
        if action == 'open':
            #这个和分校的不同 分校是对接和更新本地库并列  这里是对接放在更新本地的方法内部   自动同步到 组织中心的处理  包含 规划校 对接过去 先加单位 再加组织 后续的    学校单位作为组织的成员 加入到组织里
            res_unit, data_unit = await self.send_planning_school_to_org_center(exists_planning_school)
            #  自动添加一个组织
            res_oigna = await self.send_unit_orgnization_to_org_center(exists_planning_school, data_unit)
            # 添加组织结构 部门
            org = Organization(org_name=exists_planning_school.planning_school_name,
                               school_id=exists_planning_school.id,
                               org_type='校',
                               parent_id=0,
                               org_code=exists_planning_school.planning_school_no,
                               # 多一个参数 比分校
                               org_code_type='school',
                               )

            res_org, data_org = await self.send_org_to_org_center(org, res_unit)
            # 添加 管理员 用户
            res_admin = await self.send_admin_to_org_center(exists_planning_school, data_org)
            # 添加 用户和组织关系 就是部门
            await self.send_user_org_relation_to_org_center(exists_planning_school, res_unit, data_org, res_admin)
            # 添加 服务范围
            # await self.send_service_unit_to_org_center(exists_planning_school, res_unit, data_org, res_admin)

            # 自动新增 学校信息的处理 1.学校信息 2.学校联系方式 3.学校教育信息
            school_rule = get_injector(SchoolRule)
            school_communication_rule = get_injector(SchoolCommunicationRule)
            school_eduinfo_rule = get_injector(SchoolEduinfoRule)
            planning_school = orm_model_to_view_model(exists_planning_school, PlanningSchoolModel,
                                                      exclude=["created_at", 'updated_at', ])
            print('自动创建分校')

            school_res = await school_rule.add_school_from_planning_school(planning_school)
            # school_res = await self.school_rule.add_school_from_planning_school(res)
            exists_planning_school_com = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(
                planning_school_id)
            res_comm = orm_model_to_view_model(exists_planning_school_com, PlanningSchoolCommunications,
                                               exclude=["created_at", 'updated_at', ])
            print('自动创建分校的通信信息')

            await school_communication_rule.add_school_communication_from_planning_school(res_comm, school_res)
            # planning_school_edu = orm_model_to_view_model(res_edu, PlanningSchoolEduInfo, exclude=["created_at",'updated_at',])
            exists_planning_school_edu = await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_planning_school_id(
                planning_school_id)
            res_edu = orm_model_to_view_model(exists_planning_school_edu, PlanningSchoolEduInfo,
                                              exclude=["created_at", 'updated_at', ])
            print('自动创建分校的教育信息')

            await school_eduinfo_rule.add_school_eduinfo_from_planning_school(res_edu, school_res)

        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        print('更新规划校主体信息')
        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(exists_planning_school,
                                                                                          *need_update_list,
                                                                                          is_commit=True)

        return planning_school_db

    async def update_planning_school_byargs(self, planning_school, need_update_list=None):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        if hasattr(planning_school, 'social_credit_code'):
            await check_social_credit_code(planning_school.social_credit_code,exists_planning_school)

        if exists_planning_school.status == PlanningSchoolStatus.DRAFT.value:
            if hasattr(planning_school, 'status'):
                # planning_school.status= PlanningSchoolStatus.OPENING.value
                pass
        else:
            pass
        if not need_update_list:

            need_update_list = []
            for key, value in planning_school.__dict__.items():
                if key.startswith('_'):
                    continue
                if value:
                    need_update_list.append(key)
            need_update_list.remove('id')

        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(planning_school,
                                                                                          *need_update_list,
                                                                                          is_commit=True)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        convert_snowid_in_model(planning_school_db)
        return planning_school_db

    async def query_planning_schools(self, planning_school_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(PlanningSchool)
                                       .where(PlanningSchool.planning_school_name.like(f'%{planning_school_name}%'))
                                       .where(PlanningSchool.is_deleted == False)
                                       .where(PlanningSchool.status == PlanningSchoolStatus.NORMAL.value)
                                       )
        res = result.scalars().all()
        print(res)
        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, PlanningSchoolModel)
            convert_snowid_in_model(planning_school)
            lst.append(planning_school)
        return lst

    # 向工作流中心发送申请
    async def add_planning_school_work_flow(self, planning_school_flow: PlanningSchoolModel,
                                            planning_school_baseinfo: PlanningSchoolBaseInfo):
        # planning_school_flow.id=0
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        data = planning_school_flow
        datadict = data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] = planning_school_flow.founder_type_lv3
        datadict['block'] = planning_school_flow.block
        datadict['borough'] = planning_school_flow.borough
        datadict['planning_school_level'] = planning_school_flow.planning_school_level
        datadict['apply_user'] = 'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
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
        # 节点实例id todo  自动获取
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

    async def add_planning_school_close_work_flow(self, planning_school_flow: PlanningSchoolModel,
                                                  planning_school_baseinfo: PlanningSchoolBaseInfo, action_reason,
                                                  related_license_upload):
        # planning_school_flow.id=0
        data = planning_school_flow
        datadict = data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] = planning_school_flow.founder_type_lv3
        datadict['block'] = planning_school_flow.block
        datadict['borough'] = planning_school_flow.borough
        datadict['planning_school_level'] = planning_school_flow.planning_school_level
        datadict['apply_user'] = 'tester'
        dicta = planning_school_flow.__dict__
        dicta['action_reason'] = action_reason
        dicta['related_license_upload'] = related_license_upload

        dicta['planning_school_id'] = planning_school_flow.id

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

        try:
            if audit_info.transaction_audit_action == AuditAction.PASS.value:
                # 成功则写入数据
                res2 = await self.deal_planning_school(audit_info.process_instance_id, action)
                pass
            # 发起审批流的 处理

            datadict = audit_info.__dict__
            audit_info.process_instance_id = int(audit_info.process_instance_id)
            if audit_info.process_instance_id > 0:
                node_id = await self.system_rule.get_work_flow_current_node_by_process_instance_id(
                    audit_info.process_instance_id)
                audit_info.node_id = node_id['node_instance_id']

            # 节点实例id
            datadict['node_instance_id'] = audit_info.node_id

            apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
            # 字典参数
            datadict = {"user_id": "11", "action": "approved", **datadict}
            if audit_info.transaction_audit_action == AuditAction.PASS.value:
                datadict['action'] = 'approved'
            if audit_info.transaction_audit_action == AuditAction.REFUSE.value:
                datadict['action'] = 'rejected'
            print('审批流发起请求')

            response = await send_request(apiname, datadict, 'post', True)
            print(response, '接口响应')

            # 终态的处理 这个要改为另一个方式

            await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)

            return response
        except Exception as e:
            print(e)
            raise e
            return response
        pass

    async def deal_planning_school(self, process_instance_id, action, ):
        #  读取流程实例ID
        planning_school = await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if not planning_school:
            print('未查到规划校信息', process_instance_id)
            # raise Exception('未查到规划校信息')
            raise PlanningSchoolNotFoundByProcessInstanceIdError()
            return
        if action == 'open':
            res = await self.update_planning_school_status(planning_school.id, PlanningSchoolStatus.NORMAL.value,
                                                           'open')
        if action == 'close':
            res = await self.update_planning_school_status(planning_school.id, PlanningSchoolStatus.CLOSED.value,
                                                           'close')
        if action == 'keyinfo_change':
            # todo 把基本信息变更 改进去
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data = JsonUtils.json_str_to_dict(result.get('json_data'))
            print(json_data)
            planning_school_orm = PlanningSchoolKeyInfo(**json_data)
            planning_school_orm.id = planning_school.id

            res = await self.update_planning_school_byargs(planning_school_orm)
            pass

        # res = await self.update_planning_school_status(planning_school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass

    async def set_transaction_end(self, process_instance_id, status):
        tinfo = await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status = status.value
            tinfo.id = int(tinfo.id)

            planning_school_db = await self.planning_school_dao.update_planning_school_byargs(tinfo, 'workflow_status',
                                                                                              is_commit=True)
            # await self.update_planning_school_byargs(tinfo,['workflow_status'])

        pass

    async def add_planning_school_keyinfo_change_work_flow(self, planning_school_flow: PlanningSchoolKeyInfo, ):
        # planning_school_flow.id=0
        httpreq = HTTPRequest()
        url = workflow_service_config.workflow_config.get("url")
        data = planning_school_flow
        datadict = data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        datadict['teacher_id'] = 0
        datadict['applicant_name'] = 'tester'
        datadict['planning_school_no'] = planning_school_flow.planning_school_no

        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['planning_school_edu_level'] = planning_school_flow.planning_school_edu_level
        datadict['block'] = planning_school_flow.block
        datadict['borough'] = planning_school_flow.borough
        datadict['planning_school_level'] = planning_school_flow.planning_school_level
        datadict['planning_school_category'] = planning_school_flow.planning_school_category
        datadict['planning_school_operation_type'] = planning_school_flow.planning_school_operation_type
        datadict['planning_school_org_type'] = planning_school_flow.planning_school_org_type

        datadict['apply_user'] = 'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
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

    async def is_can_not_add_workflow(self, student_id, is_all_status_allow=False):
        tinfo = await self.get_planning_school_by_id(student_id)
        print('当前信息', tinfo)
        if not is_all_status_allow:
            # 如果 是草稿态 则锁定
            if tinfo and tinfo.status == PlanningSchoolStatus.DRAFT.value:
                return True
        # 检查是否有占用 如果有待处理的流程ID 则锁定
        if tinfo and tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
            return True
        return False

    async def planning_school_export(self, task: Task):
        bucket = 'school'
        print(bucket, '桶')

        export_params: PlanningSchoolPageSearch = (
            task.payload if task.payload is PlanningSchoolPageSearch() else PlanningSchoolPageSearch()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"planning_school_export_{shortuuid.uuid()}.xlsx"
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
            paging = await self.planning_school_dao.query_planning_school_with_page(
                page_request, export_params.planning_school_name, export_params.planning_school_no,
                export_params.planning_school_code,
                export_params.block, export_params.planning_school_level, export_params.borough, export_params.status,
                export_params.founder_type,
                export_params.founder_type_lv2, export_params.founder_type_lv3
            )

            paging_result = PaginatedResponse.from_paging(
                paging, PlanningSchoolOptional, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            await self.convert_planning_school_to_export_format(paging_result)

            logger.info('分页的结果条数', len(paging_result.items))
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
            print(f"任务结果 {task_result}")

            resadd = await self.task_dao.add_task_result(task_result, True)
            print('task_result写入结果', resadd, f"task_result写入结果 {resadd}")
            # print(dir(task_result),dir(resadd))
            # objprint(task_result,resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result

    async def is_can_change_keyinfo(self, student_id, is_all_status_allow=False):
        tinfo = await self.get_planning_school_by_id(student_id)
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

    #     定义方法吧一行记录转化为适合导出展示的格式
    async def convert_planning_school_to_export_format(self, paging_result):
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
            for item in paging_result.items:
                # item.approval_status =  item.approval_status.value
                delattr(item, 'id')
                delattr(item, 'created_uid')
                item.province = provinces[item.province].description if item.province in provinces else item.province
                item.city = citys[item.city].description if item.city in citys else item.city
                item.block = districts[item.block].description if item.block in districts else item.block
                item.borough = districts[item.borough].description if item.borough in districts else item.borough
                item.planning_school_edu_level = enum_mapper[
                    item.planning_school_edu_level] if item.planning_school_edu_level in enum_mapper.keys() else item.planning_school_edu_level
                item.planning_school_category = enum_mapper[
                    item.planning_school_category] if item.planning_school_category in enum_mapper.keys() else item.planning_school_category
                item.planning_school_operation_type = enum_mapper[
                    item.planning_school_operation_type] if item.planning_school_operation_type in enum_mapper.keys() else item.planning_school_operation_type
                item.planning_school_org_type = enum_mapper[
                    item.planning_school_org_type] if item.planning_school_org_type in enum_mapper.keys() else item.planning_school_org_type
                item.planning_school_level = enum_mapper[
                    item.planning_school_level] if item.planning_school_level in enum_mapper.keys() else item.planning_school_level
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
                if item.planning_school_org_form:
                    item.planning_school_org_form = school_org_form[
                        item.planning_school_org_form].description if item.planning_school_org_form in school_org_form else item.planning_school_org_form

                pass
            pass
        else:
            item = paging_result
            delattr(item, 'id')
            delattr(item, 'created_uid')
            item.province = provinces[item.province].description if item.province in provinces else item.province
            item.city = citys[item.city].description if item.city in citys else item.city
            item.block = districts[item.block].description if item.block in districts else item.block
            item.borough = districts[item.borough].description if item.borough in districts else item.borough
            item.planning_school_edu_level = enum_mapper[
                item.planning_school_edu_level] if item.planning_school_edu_level in enum_mapper.keys() else item.planning_school_edu_level
            item.planning_school_category = enum_mapper[
                item.planning_school_category] if item.planning_school_category in enum_mapper.keys() else item.planning_school_category
            item.planning_school_operation_type = enum_mapper[
                item.planning_school_operation_type] if item.planning_school_operation_type in enum_mapper.keys() else item.planning_school_operation_type
            item.planning_school_org_type = enum_mapper[
                item.planning_school_org_type] if item.planning_school_org_type in enum_mapper.keys() else item.planning_school_org_type
            item.planning_school_level = enum_mapper[
                item.planning_school_level] if item.planning_school_level in enum_mapper.keys() else item.planning_school_level
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
            if item.planning_school_org_form:
                item.planning_school_org_form = school_org_form[
                    item.planning_school_org_form].description if item.planning_school_org_form in school_org_form else item.planning_school_org_form
            return item

        # return item

    #     枚举初始化的方法
    async def init_enum_value_rule(self):
        enum_value_rule = get_injector(EnumValueRule)
        self.districts = await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY, Constant.CURRENT_CITY,
                                                                 return_keys='description')
        print('区域', self.districts)
        self.enum_mapper = {value: key for key, value in frontend_enum_mapping.items()}
        print('枚举映射', self.enum_mapper)
        return self

    async def convert_planning_school_to_import_format(self, item):
        item.block = self.districts[item.block].enum_value if item.block in self.districts else item.block
        item.borough = self.districts[item.borough].enum_value if item.borough in self.districts else item.borough
        item.planning_school_edu_level = self.enum_mapper[
            item.planning_school_edu_level] if item.planning_school_edu_level in self.enum_mapper.keys() else item.planning_school_edu_level
        value = item.planning_school_category
        if value and isinstance(value, str) and value.find('-') != -1:
            temp = value.split('-')
            item.planning_school_category = temp[1] if len(temp) > 1 else value

        item.planning_school_category = self.enum_mapper[
            item.planning_school_category] if item.planning_school_category in self.enum_mapper.keys() else item.planning_school_category
        item.planning_school_org_type = self.enum_mapper[
            item.planning_school_org_type] if item.planning_school_org_type in self.enum_mapper.keys() else item.planning_school_org_type
        pass

    # 发送规划校到组织中心的方法
    async def send_planning_school_to_org_center(self, exists_planning_school_origin):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer
        planning_school_communication = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(
            exists_planning_school.id)
        cn_exists_planning_school = await self.convert_planning_school_to_export_format(exists_planning_school)
        dict_data = {'administrativeDivisionCity':  '',
                     'administrativeDivisionCounty': cn_exists_planning_school.block,
                     'administrativeDivisionProvince': planning_school_communication.loc_area_pro,
                     'createdTime': exists_planning_school.create_planning_school_date,
                     'locationAddress': planning_school_communication.detailed_address,
                     'locationCity': '',
                     'locationCounty': planning_school_communication.loc_area,
                     'locationProvince': planning_school_communication.loc_area_pro,
                     # 所属组织这个可以不要
                     'owner': exists_planning_school.planning_school_no,
                     # 'unitCode': exists_planning_school.planning_school_no+shortuuid.uuid(),
                     'unitCode': exists_planning_school.planning_school_no,
                     'unitId': '',
                     'unitName': exists_planning_school.planning_school_name,
                     'unitType': 'school',
                     'updatedTime': exists_planning_school.updated_at,
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
        print('发起请求单位到组织中心')

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print(response)
            print('发起请求单位到组织中心suc')
            if isinstance(response, dict):
                unitid = response['data2'] if 'data2' in response.keys() else ''
                exists_planning_school_origin.org_center_info = unitid
                need_update_list = []
                need_update_list.append( 'org_center_info')
                datadict['unitId'] = unitid
                #检查这个方法 加字段
                await self.planning_school_dao.update_planning_school_byargs(exists_planning_school_origin,  *need_update_list)


            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    async def send_admin_to_org_center(self, exists_planning_school_origin, data_org):
        # teacher_db = await self.teachers_dao.get_teachers_arg_by_id(teacher_id)
        # data_dict = to_dict(teacher_db)
        # print(data_dict)
        # todo  身份类型的 读取
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        school = exists_planning_school
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school)
            return
        school_operation_type = []
        if school:
            school = orm_model_to_view_model(school, PlanningSchoolModel)
            if school.planning_school_edu_level:
                school_operation_type.append(school.planning_school_edu_level)
            if school.planning_school_category:
                school_operation_type.append(school.planning_school_category)
            if school.planning_school_operation_type:
                school_operation_type.append(school.planning_school_operation_type)
        identity_type, identity = await get_identity_by_job(school_operation_type, '')

        school  = await self.planning_school_dao.get_planning_school_by_id(
            exists_planning_school_origin.id)
        dict_data = EducateUserModel(**exists_planning_school_origin.__dict__,
                                     # 单位 部门
                                     currentUnit=school.org_center_info,
                                     createdTime=exists_planning_school_origin.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     updatedTime=exists_planning_school_origin.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     # 账号和组织 syyxorg
                                     name=exists_planning_school_origin.admin_phone,
                                     owner=exists_planning_school_origin.planning_school_no,
                                     # owner= exists_planning_school_origin.planning_school_name,
                                     userCode=exists_planning_school_origin.admin,
                                     # userId=exists_planning_school_origin.admin_phone+shortuuid.uuid(),
                                     phoneNumber=exists_planning_school_origin.admin_phone,
                                     # 部门group 的显示名字
                                     departmentNames=data_org['displayName'],
                                     # 部门group的name
                                     departmentId=data_org['name'],
                                     identity = identity,
                                     identityType = IdentityType.STAFF.value,
                                     realName=exists_planning_school_origin.admin
                                     )
        dict_data = dict_data.__dict__
        # params_data = JsonUtils.dict_to_json_str(dict_data)
        api_name = '/api/add-educate-user'
        # 字典参数 把键按照字典序排序

        datadict = dict_data
        # datadict = dict(sorted(datadict.items()))
        # 字典升序

        print('参数', datadict)
        print('发起请求 人员管理员到组织中心')
        response = await send_orgcenter_request(api_name, datadict, 'post', False)
        print(response, '接口响应')
        try:
            print('发起请求 人员管理员到组织中心res', response)
            return response
        except Exception as e:
            print(e)
            raise e
            return response
        return None

    async def send_unit_orgnization_to_org_center(self, exists_planning_school_origin, data_unit):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer  orgType组织类型 -必填 administrative_unit|public_institutions|school|developer
        planning_school_communication = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(
            exists_planning_school.id)
        cn_exists_planning_school = await self.convert_planning_school_to_export_format(exists_planning_school)
        dict_data = {'administrativeDivisionCity':  '',
                     'administrativeDivisionCounty': exists_planning_school.block,
                     'administrativeDivisionProvince': '',
                     'createdTime': exists_planning_school.create_planning_school_date,
                     'locationAddress': planning_school_communication.detailed_address,
                     'locationCity':  '',
                     'locationCounty': planning_school_communication.loc_area,
                     'locationProvince': planning_school_communication.loc_area_pro, 'owner': '',
                     'unitCode': exists_planning_school.planning_school_no,
                     # 'unitId': '',
                     'unitName': exists_planning_school.planning_school_name,
                     'unitType': 'school',
                     'updatedTime': exists_planning_school.updated_at,
                     # "appHomeUrl": "http://tgiibjya.nr/xxhsh",
                     # "appName": exists_planning_school.planning_school_name,

                     "educateUnits": [
                         data_unit
                     ],

                     "certPublicKey": "",
                     "clientId": "",
                     "clientSecret": "",
                     "code": exists_planning_school.planning_school_no,
                     # "defaultApplication":   exists_planning_school.planning_school_name,
                     "defaultAvatar": "",
                     "defaultPassword": "",
                     "displayName": exists_planning_school.planning_school_name,

                     "logo": "",

                     "orgType": "school",
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

            print('组织添加 res')

            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    async def send_org_to_org_center(self, exists_planning_school_origin: Organization, res_unit):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        if hasattr(exists_planning_school, 'updated_at') and isinstance(exists_planning_school.updated_at,
                                                                        (date, datetime)):
            exists_planning_school.updated_at = exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer

        school = await self.planning_school_dao.get_planning_school_by_id(exists_planning_school.school_id)
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
            "educateUnit": unitid if unitid is not None else school.planning_school_name,
            "isDeleted": False,
            "isEnabled": True,
            "isTopGroup": exists_planning_school.parent_id == 0,
            "key": "sit",
            "manager": "",
            "name": exists_planning_school.org_name + "默认部门",
            # "name": "基础信息管理系统",
            "newCode": exists_planning_school.org_code,
            "newType": "organization",  # 组织类型 特殊参数必须穿这个
            "owner": school.planning_school_no,
            "parentId": str(exists_planning_school.parent_id),
            "parentName": "",
            "tags": [
                ""
            ],
            "title": exists_planning_school.org_name,
            "type": "",
        }

        apiname = '/api/add-group-organization'
        # 字典参数
        datadict = dict_data
        datadict = convert_dates_to_strings(datadict)
        print('调用添加部门  字典参数', datadict, )

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print('调用添加部门 接口响应', response, )
        try:
            print(response)

            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None

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
            school = orm_model_to_view_model(school, PlanningSchoolModel)
            if school.planning_school_edu_level:
                school_operation_type.append(school.planning_school_edu_level)
            if school.planning_school_category:
                school_operation_type.append(school.planning_school_category)
            if school.planning_school_operation_type:
                school_operation_type.append(school.planning_school_operation_type)
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
            "unitId": unitid if unitid is not None else school.planning_school_name,
        }

        apiname = '/api/add-educate-user-department-identitys'
        # 字典参数 todo  调整  参数完善   另 服务范围的接口
        datadict = [dict_data]
        # datadict = convert_dates_to_strings(datadict)
        print('调用添加部门用户关系  字典参数', datadict, )

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print('调用添加部门用户关系 接口响应', response, )
        try:
            print(response)

            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None

    async def send_service_unit_to_org_center(self, exists_planning_school_origin, res_unit,
                                              data_org, res_admin):
        exists_planning_school = copy.deepcopy(exists_planning_school_origin)
        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer

        # school = await self.planning_school_dao.get_planning_school_by_id(exists_planning_school.school_id)
        school = exists_planning_school
        if school is None:
            print('学校未找到 跳过发送组织', exists_planning_school)
            return

        unitid = None
        userid = None

        dict_data = {
            "administrativeDivisionCity": exists_planning_school.city,
            "administrativeDivisionCounty": exists_planning_school.block,
            "administrativeDivisionProvince": exists_planning_school.province,
            "locationAddress": exists_planning_school.block,
            "locationCity": exists_planning_school.city,
            "locationCounty": exists_planning_school.block,
            "locationProvince": exists_planning_school.province,
            # 所属组织
            "owner": exists_planning_school.planning_school_name,
            # 教育单位的code
            "unitCode": exists_planning_school.planning_school_no,
            "unitType": "school",
        }
        apiname = '/api/add-service-units'
        # 字典参数 todo  调整  参数完善   另 服务范围的接口
        datadict = [dict_data]
        print('调用添加服务范围  字典参数', datadict, )

        response = await send_orgcenter_request(apiname, datadict, 'post', False)
        print('调用添加服务范围 接口响应', response, )
        try:
            print(response)

            return response, datadict
        except Exception as e:
            print(e)
            raise e
            return response

        return None
