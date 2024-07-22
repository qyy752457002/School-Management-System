import json
import os
from datetime import datetime

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.data_access.task_dao import TaskDAO
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.storage.manager import storage_manager
from mini_framework.storage.persistent.file_storage_dao import FileStorageDAO
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from sqlalchemy import select
from business_exceptions.planning_school import PlanningSchoolNotFoundError, \
    PlanningSchoolNotFoundByProcessInstanceIdError
from daos.enum_value_dao import EnumValueDAO
from daos.planning_school_communication_dao import PlanningSchoolCommunicationDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.planning_school_eduinfo_dao import PlanningSchoolEduinfoDAO
from models.planning_school import PlanningSchool
from models.student_transaction import AuditAction
from rules import enum_value_rule
from rules.common.common_rule import send_request, send_orgcenter_request
from rules.enum_value_rule import EnumValueRule
from rules.school_communication_rule import SchoolCommunicationRule
from rules.school_eduinfo_rule import SchoolEduinfoRule
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config, convert_snowid_to_strings, convert_snowid_in_model, \
    frontend_enum_mapping
from views.common.constant import Constant
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus, \
    PlanningSchoolKeyInfo, PlanningSchoolTransactionAudit, PlanningSchoolBaseInfoOptional, PlanningSchoolPageSearch, \
    PlanningSchoolOptional
from views.models.planning_school import PlanningSchoolBaseInfo
from mini_framework.databases.conn_managers.db_manager import db_connection_manager

from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.system import STUDENT_TRANSFER_WORKFLOW_CODE, PLANNING_SCHOOL_OPEN_WORKFLOW_CODE, \
    PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE, PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, DISTRICT_ENUM_KEY, \
    PROVINCE_ENUM_KEY, CITY_ENUM_KEY, PLANNING_SCHOOL_STATUS_ENUM_KEY, FOUNDER_TYPE_ENUM_KEY, FOUNDER_TYPE_LV2_ENUM_KEY, \
    FOUNDER_TYPE_LV3_ENUM_KEY, SCHOOL_ORG_FORM_ENUM_KEY


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
    districts= None
    enum_mapper=None




    async def get_planning_school_by_id(self, planning_school_id,extra_model=None):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not planning_school_db:
            raise PlanningSchoolNotFoundError()
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel)
        #str
        convert_snowid_in_model(planning_school)

        if extra_model:
            planning_school_extra = orm_model_to_view_model(planning_school_db, extra_model,
                                                       exclude=[""])
            convert_snowid_in_model(planning_school_extra)

            return planning_school,planning_school_extra

        else:
            return planning_school

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school_name)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def add_planning_school(self, planning_school: PlanningSchoolModel|PlanningSchoolOptional):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school.planning_school_name)
        if exists_planning_school:
            raise Exception(f"规划校{planning_school.planning_school_name}已存在")
        planning_school_db = view_model_to_orm_model(planning_school, PlanningSchool,    exclude=["id"])
        planning_school_db.status =  PlanningSchoolStatus.DRAFT.value
        planning_school_db.created_uid = 0
        planning_school_db.updated_uid = 0
        planning_school_db.id =SnowflakeIdGenerator(1, 1).generate_id()
        if planning_school.province and len( planning_school.province)>0:
            pass
        else:
            planning_school.province = "210000"
        if planning_school.city and len( planning_school.city)>0:
            pass
        else:
            planning_school.city = "210100"

        planning_school_db = await self.planning_school_dao.add_planning_school(planning_school_db)
        print('id 111',planning_school_db.id)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=["created_at",'updated_at',])
        #str
        convert_snowid_in_model(planning_school)
        return planning_school

    async def delete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.delete_planning_school(exists_planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
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

    async def query_planning_school_with_page(self, page_request: PageRequest,  planning_school_name,planning_school_no,planning_school_code,
                                              block,planning_school_level,borough,status ,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ):
        # todo 根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res= await enum_value_rule.get_next_level_enum_values('founder_type'  ,founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)


            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if len(founder_type_lv2)>0:
            founder_type_lv3_res= await enum_value_rule.get_next_level_enum_values('founder_type_lv2'  ,founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.planning_school_dao.query_planning_school_with_page(  page_request, planning_school_name,planning_school_no,planning_school_code,
                                                                                  block,planning_school_level,borough,status,founder_type,
                                                                                  founder_type_lv2,
                                                                                  founder_type_lv3 )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolModel)
        #str
        convert_snowid_to_strings(paging_result)
        return paging_result


    async def update_planning_school_status(self, planning_school_id, target_status,action=None):

        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        # 判断原来的状态+要更改的状态 进行后续的更新
        if target_status== PlanningSchoolStatus.NORMAL.value and exists_planning_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办 自动创建一条学校信息
            exists_planning_school.status= PlanningSchoolStatus.NORMAL.value
        elif target_status== PlanningSchoolStatus.CLOSED.value and exists_planning_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_planning_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_planning_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"规划校当前状态不支持您的操作{exists_planning_school.status}")

        need_update_list = []
        need_update_list.append('status')

        print(exists_planning_school.status,2222222)
        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(exists_planning_school,*need_update_list,is_commit=True)
        if action=='open':
            # 自动新增 学校信息的处理 1.学校信息 2.学校联系方式 3.学校教育信息
            school_rule = get_injector(SchoolRule)
            school_communication_rule = get_injector(SchoolCommunicationRule)
            school_eduinfo_rule = get_injector(SchoolEduinfoRule)
            planning_school = orm_model_to_view_model(exists_planning_school, PlanningSchoolModel, exclude=["created_at",'updated_at',])

            school_res =await school_rule.add_school_from_planning_school(planning_school)
            # school_res = await self.school_rule.add_school_from_planning_school(res)
            exists_planning_school_com = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(planning_school_id)
            res_comm = orm_model_to_view_model(exists_planning_school_com, PlanningSchoolCommunications, exclude=["created_at",'updated_at',])


            await school_communication_rule.add_school_communication_from_planning_school(res_comm,school_res)
            # planning_school_edu = orm_model_to_view_model(res_edu, PlanningSchoolEduInfo, exclude=["created_at",'updated_at',])
            exists_planning_school_edu= await self.planning_school_eduinfo_dao.get_planning_school_eduinfo_by_planning_school_id(planning_school_id)
            res_edu = orm_model_to_view_model(exists_planning_school_edu, PlanningSchoolEduInfo, exclude=["created_at",'updated_at',])


            await school_eduinfo_rule.add_school_eduinfo_from_planning_school(res_edu,school_res)
            #todo 自动同步到 组织中心的处理  包含 规划校 对接过去     学校后面也加对接过去
            await self.send_planning_school_to_org_center(exists_planning_school)


        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db

    async def update_planning_school_byargs(self, planning_school,need_update_list=None):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()

        if exists_planning_school.status== PlanningSchoolStatus.DRAFT.value:
            if hasattr(planning_school,'status'):

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

        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(planning_school, *need_update_list,is_commit=True)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        convert_snowid_in_model(planning_school_db)
        return planning_school_db


    async def query_planning_schools(self,planning_school_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(PlanningSchool)
                                       .where(PlanningSchool.planning_school_name.like(f'%{planning_school_name}%') )
                                       .where(PlanningSchool.is_deleted==  False)
                                       )
        res= result.scalars().all()
        print(res)
        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, PlanningSchoolModel)
            convert_snowid_in_model(planning_school)
            lst.append(planning_school)
        return lst


    # 向工作流中心发送申请
    async def add_planning_school_work_flow(self, planning_school_flow: PlanningSchoolModel,planning_school_baseinfo: PlanningSchoolBaseInfo):
        # planning_school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] =   planning_school_flow.founder_type_lv3
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['apply_user'] =  'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
        datadict['json_data'] =  json.dumps(mapa, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def req_workflow_cancel(self,node_id,process_instance_id=None):

        # 发起审批流的 处理
        datadict = dict()
        # 节点实例id todo  自动获取
        if process_instance_id>0:
            node_id=await self.system_rule.get_work_flow_current_node_by_process_instance_id(  process_instance_id)
            node_id=node_id['node_instance_id']

        datadict['node_instance_id'] =  node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # 字典参数
        # datadict ={"user_id":"11","action":"revoke"}
        datadict ={"user_id":"11","action":"revoke",**datadict}

        response= await send_request(apiname,datadict,'post',True)

        print(response,'接口响应')
        # 终态的处理

        await self.set_transaction_end(process_instance_id, AuditAction.CANCEL)


        return response
        pass


    async def add_planning_school_close_work_flow(self, planning_school_flow: PlanningSchoolModel,planning_school_baseinfo: PlanningSchoolBaseInfo,action_reason,related_license_upload):
        # planning_school_flow.id=0
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_code'] = planning_school_flow.planning_school_code
        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['founder_type_lv3'] =   planning_school_flow.founder_type_lv3
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['apply_user'] =  'tester'
        dicta = planning_school_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload

        dicta['planning_school_id'] = planning_school_flow.id

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'

        response= None
        try:
            response = await send_request(apiname,datadict,'post')
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def req_workflow_audit(self,audit_info:PlanningSchoolTransactionAudit,action):

        # 发起审批流的 处理

        datadict = audit_info.__dict__
        audit_info.process_instance_id= int(audit_info.process_instance_id)
        if audit_info.process_instance_id>0:
            node_id=await self.system_rule.get_work_flow_current_node_by_process_instance_id(  audit_info.process_instance_id)
            audit_info.node_id=node_id['node_instance_id']


        # 节点实例id
        datadict['node_instance_id'] =  audit_info.node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # 字典参数
        datadict ={"user_id":"11","action":"approved",**datadict}
        if audit_info.transaction_audit_action== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if audit_info.transaction_audit_action== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await send_request(apiname,datadict,'post',True)
        print(response,'接口响应')
        try:
            if audit_info.transaction_audit_action== AuditAction.PASS.value:
                # 成功则写入数据
                # transrule = get_injector(StudentTransactionRule)
                # await transrule.deal_student_transaction(student_edu_info)
                res2 = await self.deal_planning_school(audit_info.process_instance_id, action)
                pass
            # 终态的处理 这个要改为另一个方式

            await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)


            return response
        except Exception as e:
            print(e)
            raise e
            return response
        pass

    async def deal_planning_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        planning_school = await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if not planning_school:
            print('未查到规划校信息',process_instance_id)
            # raise Exception('未查到规划校信息')
            raise PlanningSchoolNotFoundByProcessInstanceIdError()
            return
        if action=='open':
            res = await self.update_planning_school_status(planning_school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
        if action=='close':
            res = await self.update_planning_school_status(planning_school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            planning_school_orm = PlanningSchoolKeyInfo(**json_data)
            planning_school_orm.id= planning_school.id

            res = await self.update_planning_school_byargs(  planning_school_orm)
            pass

        # res = await self.update_planning_school_status(planning_school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass

    async def set_transaction_end(self,process_instance_id,status):
        tinfo=await self.planning_school_dao.get_planning_school_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status=status.value
            tinfo.id = int(tinfo.id)

            planning_school_db = await self.planning_school_dao.update_planning_school_byargs(tinfo,'workflow_status' ,is_commit=True)
            # await self.update_planning_school_byargs(tinfo,['workflow_status'])


        pass

    async def add_planning_school_keyinfo_change_work_flow(self, planning_school_flow: PlanningSchoolKeyInfo,):
        # planning_school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= planning_school_flow
        datadict =  data.__dict__
        datadict['process_code'] = PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['planning_school_no'] = planning_school_flow.planning_school_no

        datadict['planning_school_name'] = planning_school_flow.planning_school_name
        datadict['planning_school_edu_level'] =   planning_school_flow.planning_school_edu_level
        datadict['block'] =   planning_school_flow.block
        datadict['borough'] =   planning_school_flow.borough
        datadict['planning_school_level'] =   planning_school_flow.planning_school_level
        datadict['planning_school_category'] =   planning_school_flow.planning_school_category
        datadict['planning_school_operation_type'] =   planning_school_flow.planning_school_operation_type
        datadict['planning_school_org_type'] =   planning_school_flow.planning_school_org_type

        datadict['apply_user'] =  'tester'
        mapa = planning_school_flow.__dict__
        mapa['planning_school_id'] = planning_school_flow.id
        datadict['json_data'] =  json.dumps(mapa, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def is_can_not_add_workflow(self, student_id,is_all_status_allow=False):
        tinfo=await self.get_planning_school_by_id(student_id)
        print('当前信息',tinfo)
        if not is_all_status_allow:
            # 如果 是草稿态 则锁定
            if tinfo and  tinfo.status == PlanningSchoolStatus.DRAFT.value:
                return  True
        # 检查是否有占用 如果有待处理的流程ID 则锁定
        if tinfo and  tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
            return True
        return False

    async def planning_school_export(self, task: Task):
        bucket = 'school'
        print(bucket,'桶')

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
                 page_request,export_params.planning_school_name,export_params.planning_school_no,export_params.planning_school_code,
                export_params.block,export_params.planning_school_level,export_params.borough,export_params.status,export_params.founder_type,
                export_params.founder_type_lv2,export_params.founder_type_lv3
            )

            paging_result = PaginatedResponse.from_paging(
                paging, PlanningSchoolOptional, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            await self.convert_planning_school_to_export_format(paging_result)


            logger.info('分页的结果条数',len(paging_result.items))
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
            task_result.result_id = shortuuid.uuid()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id =  0
            print('拼接数据task_result ',task_result)
            print(f"任务结果 {task_result}")

            resadd = await self.task_dao.add_task_result(task_result,True)
            print('task_result写入结果',resadd,f"task_result写入结果 {resadd}")
            # print(dir(task_result),dir(resadd))
            # objprint(task_result,resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result
    async def is_can_change_keyinfo(self, student_id,is_all_status_allow=False):
        tinfo=await self.get_planning_school_by_id(student_id)
        print('当前信息',tinfo)
        if tinfo and  tinfo.status == PlanningSchoolStatus.DRAFT.value:
            return  True
        if tinfo and  tinfo.status != PlanningSchoolStatus.NORMAL.value:
            # return  True

            # 检查是否有占用 如果有待处理的流程ID 则锁定
            if tinfo and  tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
                return False
            return True
        if tinfo and  tinfo.status == PlanningSchoolStatus.CLOSED.value:
            return  False
        return True

    #     定义方法吧一行记录转化为适合导出展示的格式
    async def convert_planning_school_to_export_format(self,paging_result):
        # 获取区县的枚举
        enum_value_rule = get_injector(EnumValueRule)
        provinces =await enum_value_rule.query_enum_values(PROVINCE_ENUM_KEY,None,return_keys='enum_value')
        citys =await enum_value_rule.query_enum_values(CITY_ENUM_KEY, None,return_keys='enum_value')
        districts =await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY,Constant.CURRENT_CITY,return_keys='enum_value')
        planningschool_status =await enum_value_rule.query_enum_values(PLANNING_SCHOOL_STATUS_ENUM_KEY,None,return_keys='enum_value')
        founder_type =await enum_value_rule.query_enum_values(FOUNDER_TYPE_ENUM_KEY,None,return_keys='enum_value')
        founder_type_lv2 =await enum_value_rule.query_enum_values(FOUNDER_TYPE_LV2_ENUM_KEY,None,return_keys='enum_value')
        founder_type_lv3 =await enum_value_rule.query_enum_values(FOUNDER_TYPE_LV3_ENUM_KEY,None,return_keys='enum_value')
        school_org_form =await enum_value_rule.query_enum_values(SCHOOL_ORG_FORM_ENUM_KEY,None,return_keys='enum_value')
        print('区域',districts, '')
        enum_mapper = frontend_enum_mapping
        #todo 这4个 目前 城乡类型 逗号3级   教学点类型 经济属性 民族属性
        if hasattr(paging_result,'items'):
            for item in paging_result.items:
                # item.approval_status =  item.approval_status.value
                delattr(item, 'id')
                delattr(item, 'created_uid')
                item.province = provinces[item.province].description if item.province in provinces else  item.province
                item.city = citys[item.city].description if item.city in citys else  item.city
                item.block = districts[item.block].description if item.block in districts else  item.block
                item.borough = districts[item.borough].description if item.borough in districts else  item.borough
                item.planning_school_edu_level = enum_mapper[item.planning_school_edu_level] if item.planning_school_edu_level in enum_mapper.keys() else  item.planning_school_edu_level
                item.planning_school_category = enum_mapper[item.planning_school_category] if item.planning_school_category in enum_mapper.keys() else  item.planning_school_category
                item.planning_school_operation_type = enum_mapper[item.planning_school_operation_type] if item.planning_school_operation_type in enum_mapper.keys() else  item.planning_school_operation_type
                item.planning_school_org_type = enum_mapper[item.planning_school_org_type] if item.planning_school_org_type in enum_mapper.keys() else  item.planning_school_org_type
                item.planning_school_level = enum_mapper[item.planning_school_level] if item.planning_school_level in enum_mapper.keys() else  item.planning_school_level
                # item.status = PlanningSchoolStatus[item.status] if item.status in enum_mapper.keys() else  item.status
                item.status = planningschool_status[item.status].description if item.status in planningschool_status else  item.status
                item.founder_type = founder_type[item.founder_type].description if item.founder_type in founder_type else  item.founder_type
                item.founder_type_lv2 = founder_type_lv2[item.founder_type_lv2].description if item.founder_type_lv2 in founder_type_lv2 else  item.founder_type_lv2
                item.founder_type_lv3 = founder_type_lv3[item.founder_type_lv3].description if item.founder_type_lv3 in founder_type_lv3 else  item.founder_type_lv3
                # print('枚举映射',item)
                if item.planning_school_org_form:
                    item.planning_school_org_form = school_org_form[item.planning_school_org_form].description if item.planning_school_org_form in school_org_form else  item.planning_school_org_form

                pass
            pass
        else:
            item= paging_result
            delattr(item, 'id')
            delattr(item, 'created_uid')
            item.province = provinces[item.province].description if item.province in provinces else  item.province
            item.city = citys[item.city].description if item.city in citys else  item.city
            item.block = districts[item.block].description if item.block in districts else  item.block
            item.borough = districts[item.borough].description if item.borough in districts else  item.borough
            item.planning_school_edu_level = enum_mapper[item.planning_school_edu_level] if item.planning_school_edu_level in enum_mapper.keys() else  item.planning_school_edu_level
            item.planning_school_category = enum_mapper[item.planning_school_category] if item.planning_school_category in enum_mapper.keys() else  item.planning_school_category
            item.planning_school_operation_type = enum_mapper[item.planning_school_operation_type] if item.planning_school_operation_type in enum_mapper.keys() else  item.planning_school_operation_type
            item.planning_school_org_type = enum_mapper[item.planning_school_org_type] if item.planning_school_org_type in enum_mapper.keys() else  item.planning_school_org_type
            item.planning_school_level = enum_mapper[item.planning_school_level] if item.planning_school_level in enum_mapper.keys() else  item.planning_school_level
            # item.status = PlanningSchoolStatus[item.status] if item.status in enum_mapper.keys() else  item.status
            item.status = planningschool_status[item.status].description if item.status in planningschool_status else  item.status
            item.founder_type = founder_type[item.founder_type].description if item.founder_type in founder_type else  item.founder_type
            item.founder_type_lv2 = founder_type_lv2[item.founder_type_lv2].description if item.founder_type_lv2 in founder_type_lv2 else  item.founder_type_lv2
            item.founder_type_lv3 = founder_type_lv3[item.founder_type_lv3].description if item.founder_type_lv3 in founder_type_lv3 else  item.founder_type_lv3
            # print('枚举映射',item)
            if item.planning_school_org_form:
                item.planning_school_org_form = school_org_form[item.planning_school_org_form].description if item.planning_school_org_form in school_org_form else  item.planning_school_org_form




        # return item
    #     枚举初始化的方法
    async def init_enum_value_rule(self):
        enum_value_rule = get_injector(EnumValueRule)
        self.districts =await enum_value_rule.query_enum_values(DISTRICT_ENUM_KEY,Constant.CURRENT_CITY,return_keys='description')
        print('区域',self.districts)
        self.enum_mapper =   {value: key for key, value in frontend_enum_mapping.items()}
        print('枚举映射',self.enum_mapper)
        return self

    async def convert_planning_school_to_import_format(self,item):
        item.block = self.districts[item.block].enum_value if item.block in self.districts else  item.block
        item.borough = self.districts[item.borough].enum_value if item.borough in self.districts else  item.borough
        item.planning_school_edu_level = self.enum_mapper[item.planning_school_edu_level] if item.planning_school_edu_level in self.enum_mapper.keys() else  item.planning_school_edu_level
        value= item.planning_school_category
        if value and isinstance(value, str) and value.find('-')!=-1:
            temp = value.split('-')
            item.planning_school_category =  temp[1]  if len(temp)>1  else value

        item.planning_school_category = self.enum_mapper[item.planning_school_category] if item.planning_school_category in self.enum_mapper.keys() else  item.planning_school_category
        item.planning_school_org_type = self.enum_mapper[item.planning_school_org_type] if item.planning_school_org_type in self.enum_mapper.keys() else  item.planning_school_org_type
        pass
    #发送规划校到组织中心的方法
    async def send_planning_school_to_org_center(self,exists_planning_school):
        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer
        planning_school_communication = await self.planning_school_communication_dao.get_planning_school_communication_by_planning_shool_id(exists_planning_school.id)
        cn_exists_planning_school = await self.convert_planning_school_to_export_format(exists_planning_school )
        dict_data = {'administrativeDivisionCity': exists_planning_school.city, 'administrativeDivisionCounty': exists_planning_school.block, 'administrativeDivisionProvince':  exists_planning_school.province, 'createdTime':  exists_planning_school.create_planning_school_date, 'departmentObjs': [{'children': [{'children': [], 'contactEmail': 'x.vjxkswbr@qq.com', 'createdTime': '1987-03-23 02:53:35', 'displayName': '七比什己', 'educateUnit': 'consectetur ipsum sit', 'educateUnitObj': {}, 'isDeleted': False, 'isEnabled': True, 'isTopGroup': False, 'key': 'ipsum non adipisicing', 'manager': 'sed officia', 'name': '两状住法国', 'newCode': '71', 'newType': 'aliquip', 'owner': 'pariatur mollit', 'parentId': '96', 'parentName': '许什件究', 'tags': ['in'], 'title': '始然省非验改', 'type': 'mollit aliquip dolor nostrud', 'updatedTime': '2004-03-21 04:34:58', 'users': [{'accessKey': 'commodo ipsum consectetur irure', 'accessSecret': 'eu est', 'accountStatus': 'pariatur elit irure Ut dolor', 'address': ['甘肃省绵阳市镇雄县'], 'adfs': 'occaecat do eiusmod Duis cillum', 'affiliation': 'voluptate cillum ea', 'alipay': 'non laboris sint in', 'amazon': 'in dolore', 'apple': 'cupidatat qui', 'auth0': 'ullamco sint enim eu pariatur', 'avatar': 'http://dummyimage.com/100x100', 'avatarType': 'http://dummyimage.com/100x100', 'azuread': 'velit deserunt sunt', 'baidu': '9', 'battlenet': 'mollit enim nisi fugiat eiusmod', 'bilibili': 'velit', 'bio': 'ut in dolore dolor veniam', 'birthday': '1979-06-03', 'bitbucket': 'cillum aliquip labore', 'box': 'aliqua', 'casdoor': 'minim aliqua ad culpa', 'cloudfoundry': 'irure cillum minim incididunt est', 'countryCode': '25', 'createdIp': '232.66.103.13', 'createdTime': '1993-03-24 04:52:50', 'custom': 'Excepteur aliqua quis', 'dailymotion': 'eu dolore', 'deezer': 'in in laborum', 'digitalocean': 'Ut ullamco reprehenderit quis sit', 'dingtalk': 'sint aliqua laborum Lorem proident', 'discord': 'occaecat Ut culpa', 'displayName': '至空再指公千', 'douyin': 'Excepteur tempor amet', 'dropbox': 'incididunt aliquip sunt minim anim', 'educateUser': {'avatar': 'http://dummyimage.com/100x100', 'birthDate': '1983-07-30', 'createdTime': '1984-03-28 16:50:03', 'currentUnit': 'ex adipisicing', 'departmentId': '14', 'departmentNames': '员来何现层少学', 'email': 'v.jkr@qq.com', 'gender': '男', 'idCardNumber': '39', 'idCardType': '43', 'identity': '54', 'identityNames': '史也术法', 'identityType': '26', 'identityTypeNames': '放是据其', 'mainUnitName': '低是据角关次具', 'name': '细度战公往它联', 'owner': 'mollit non ad', 'phoneNumber': '69', 'realName': '东委员三高', 'sourceApp': 'aliqua anim ullamco', 'updatedTime': '2015-06-23 06:15:52', 'userCode': '55', 'userId': '49', 'userStatus': 'nisi Ut id dolor'}, 'education': 'Lorem dolor eiusmod velit', 'email': 'p.lwnuavib@qq.com', 'emailVerified': False, 'eveonline': 'non cupidatat Excepteur fugiat in', 'externalId': '51', 'facebook': 'ex', 'firstName': '问选相增养', 'fitbit': 'proident Lorem nulla', 'gender': '女', 'gitea': 'laboris anim fugiat', 'gitee': 'ullamco ex incididunt fugiat consectetur', 'github': 'sed', 'gitlab': 'in sit amet velit', 'google': 'nulla', 'groups': ['incididunt est ex quis'], 'hash': 'non tempor nulla', 'heroku': 'reprehenderit cillum culpa consequat elit', 'homepage': 'anim deserunt sint occaecat et', 'id': '14', 'idCard': '36', 'idCardType': '21', 'influxcloud': 'ex non amet id in', 'infoflow': 'in deserunt', 'instagram': 'labore deserunt dolore', 'intercom': 'aute dolore ipsum', 'isAdmin': False, 'isDefaultAvatar': True, 'isDeleted': True, 'isForbidden': False, 'isOnline': False, 'kakao': 'nulla incididunt ea in magna', 'karma': 57, 'language': 'veniam qui ea et in', 'lark': 'in reprehenderit incididunt in', 'lastName': '此温就置', 'lastSigninIp': '26.197.84.194', 'lastSigninTime': '1991-08-01 11:33:04', 'lastSigninWrongTime': '1984-01-13 17:13:58', 'lastfm': 'tempor ea cupidatat id eu', 'ldap': 'sunt in laboris in Ut', 'line': 'cupidatat ullamco voluptate et', 'linkedin': 'non minim deserunt officia', 'location': 'irure', 'mailru': 'u.ysh@qq.com', 'managedAccounts': [{'application': 'labore est occaecat', 'password': 'est pariatur qui ullamco', 'signinUrl': 'http://eykhvcw.中国/pevksv', 'username': '何磊'}], 'meetup': 'proident', 'metamask': 'aliquip', 'mfaEmailEnabled': True, 'mfaPhoneEnabled': True, 'microsoftonline': 'proident est voluptate occaecat', 'multiFactorAuths': [{'countryCode': '68', 'enabled': False, 'isPreferred': False, 'mfaType': 'Excepteur sunt', 'recoveryCodes': ['82'], 'secret': 'ea ut dolor dolore', 'url': 'http://sdywy.ke/kjpvdlh'}], 'name': '段经备青论', 'naver': 'occaecat', 'nextcloud': 'incididunt cillum', 'okta': 'sed laboris laborum Ut culpa', 'onedrive': 'dolore', 'orgObj': {'accountItems': [{'modifyRule': 'non id exercitation ad', 'name': '究种少万图界', 'viewRule': 'pariatur amet qui ut elit', 'visible': True}], 'accountQuantity': '80', 'countryCodes': ['46'], 'createdTime': '1992-04-21 08:31:34', 'defaultApplication': 'cupidatat ullamco', 'defaultAvatar': 'http://dummyimage.com/100x100', 'defaultPassword': 'culpa officia in', 'displayName': '性任入般变主', 'educateUnits': [{'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': planning_school_communication.detailed_address, 'locationCity': exists_planning_school.city, 'locationCounty': 'consequat', 'locationProvince':planning_school_communication.loc_area_pro, 'owner': 'deserunt sunt sint id', 'unitCode':  exists_planning_school.planning_school_no , 'unitId': '', 'unitName': exists_planning_school.planning_school_name, 'unitType': 'school', 'updatedTime':  exists_planning_school.updated_at}], 'enableSoftDeletion': True, 'favicon': 'http://dummyimage.com/100x100', 'initScore': 34, 'isProfilePublic': False, 'languages': ['laboris'], 'masterPassword': 'non', 'mfaItems': [{'name': '会力般其气', 'rule': 'in officia minim dolor'}], 'name': '花再一', 'orgType': 'officia', 'overview': 'eu aliqua minim ea', 'owner': 'eiusmod esse dolore amet', 'passwordOptions': ['aute nulla magna tempor in'], 'passwordSalt': 'eiusmod cillum sint incididunt', 'passwordType': 'dolor adipisicing Duis', 'status': 'voluptate deserunt', 'tags': ['proident dolor'], 'themeData': {'borderRadius': 52, 'colorPrimary': 'non', 'isCompact': True, 'isEnabled': False, 'themeType': 'dolor amet enim nulla'}, 'unitCount': 'non occaecat', 'unitId': '85', 'websiteUrl': 'http://kpodzz.sb/wnzcq'}, 'oura': 'qui in', 'owner': 'et non incididunt', 'password': 'id', 'passwordSalt': 'nostrud dolore officia aute', 'passwordType': 'veniam proident', 'patreon': 'in id Duis cupidatat', 'paypal': 'in enim aliquip', 'permanentAvatar': 'http://dummyimage.com/100x100', 'permissions': [{'actions': ['ut nulla enim culpa'], 'adapter': 'dolor sunt', 'approveTime': '1995-12-26 11:24:56', 'approver': 'cillum Lorem in non', 'createdTime': '2016-07-03 10:33:13', 'description': '起最还问求级据参效院易被必快龙。色此眼气求山识取温劳量期单整级林运程。合进走的区来只例力它学书眼术五。再经好流设最非主务些生己没条。很证点四合级信着究放土只原适产道太。次准省除量角变其教达又当反教。', 'displayName': '统象公立', 'domains': ['s.lufkhce@qq.com'], 'effect': 'ad nisi pariatur proident', 'groups': ['fugiat Excepteur'], 'isEnabled': False, 'model': 'nisi aliqua sit', 'name': '则由式设场花看', 'owner': 'ullamco sunt', 'resourceType': 'Duis veniam laboris dolor anim', 'resources': ['voluptate'], 'roles': ['incididunt officia Duis veniam'], 'state': 'laboris minim labore culpa', 'submitter': 'Duis est in', 'users': ['consequat quis nisi']}], 'phone': '13892702437', 'preHash': 'eu', 'preferredMfaType': 'ex quis', 'properties': {'additionalProperties': 'anim ut reprehenderit voluptate ullamco'}, 'qq': 'aute nisi', 'ranking': 86, 'recoveryCodes': ['36'], 'region': 'dolore do reprehenderit ut', 'roles': [{'createdTime': '2014-05-28 06:23:22', 'description': '干好相然取则车期商该应位作产就。斗质都美法斗基建且决结应前各。团向办观质等阶团角者点历力断属。它图社气说代自真次正你型圆头区美高和。速约气她入况头格么品百治已量为。', 'displayName': '报被身权', 'domains': ['l.dvp@qq.com'], 'groups': ['non irure'], 'isEnabled': False, 'name': '共么音构', 'owner': 'aliquip reprehenderit mollit sed', 'roles': ['veniam incididunt cupidatat do'], 'users': ['ullamco est ex aute ad']}], 'salesforce': 'voluptate nostrud occaecat', 'score': 3, 'shopify': 'nisi sit ut', 'signinWrongTimes': 358517472668, 'signupApplication': 'in laborum consectetur', 'slack': 'consequat qui ut eu', 'soundcloud': 'dolor tempor culpa', 'spotify': 'ex minim veniam Ut', 'steam': 'pariatur cupidatat dolore', 'strava': 'qui dolor cupidatat exercitation', 'stripe': 'quis Duis', 'tag': 'elit cillum culpa aute', 'tiktok': 'sint sunt et nisi', 'title': '江始习确市片', 'totpSecret': 'elit do', 'tumblr': 'magna consectetur', 'twitch': 'irure ullamco', 'twitter': 'mollit fugiat exercitation Ut nisi', 'type': 'laborum in eu', 'typetalk': 'laboris in', 'uber': 'anim aute laborum labore', 'updatedTime': '1977-06-28 07:10:41', 'userId': '12', 'vk': 'minim officia', 'web3onboard': 'nostrud', 'webauthnCredentials': [], 'wechat': 'aliqua voluptate', 'wecom': 'consequat cupidatat nisi commodo', 'weibo': 'ea laborum et nostrud', 'wepay': 'dolor minim dolore Duis', 'xero': 'deserunt exercitation Ut anim ad', 'yahoo': 'esse voluptate exercitation', 'yammer': 'in nulla', 'yandex': 'non cupidatat', 'zoom': 'minim tempor qui culpa Lorem'}]}], 'contactEmail': 'j.ctmhybi@qq.com', 'createdTime': '2018-08-28 19:22:27', 'displayName': '动十新今无整', 'educateUnit': 'occaecat incididunt in fugiat labore', 'educateUnitObj': {'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}, 'isDeleted': False, 'isEnabled': False, 'isTopGroup': True, 'key': 'eiusmod', 'manager': 'eiusmod do veniam reprehenderit', 'name': '酸部明', 'newCode': '65', 'newType': 'sint consequat deserunt anim', 'owner': 'sint in do adipisicing non', 'parentId': '50', 'parentName': '低感子总天能', 'tags': ['Ut commodo'], 'title': '消程系战起', 'type': 'eu', 'updatedTime': '1985-02-27 10:35:18', 'users': [{'accessKey': 'ipsum cillum Duis non consectetur', 'accessSecret': 'occaecat', 'accountStatus': 'nostrud', 'address': ['云南省宿迁市怀远县'], 'adfs': 'Ut ullamco', 'affiliation': 'velit consequat sit in', 'alipay': 'quis ad', 'amazon': 'in irure qui veniam', 'apple': 'cupidatat et ea pariatur elit', 'auth0': 'pariatur laboris', 'avatar': 'http://dummyimage.com/100x100', 'avatarType': 'http://dummyimage.com/100x100', 'azuread': 'nisi ut fugiat', 'baidu': '67', 'battlenet': 'aliquip occaecat adipisicing', 'bilibili': 'veniam', 'bio': 'Excepteur Ut amet laboris ullamco', 'birthday': '1998-09-16', 'bitbucket': 'cupidatat nostrud ut tempor', 'box': 'aute officia est occaecat aliquip', 'casdoor': 'aute magna', 'cloudfoundry': 'esse aliquip Duis fugiat dolor', 'countryCode': '35', 'createdIp': '236.151.93.195', 'createdTime': '1981-06-01 01:03:38', 'custom': 'consequat minim', 'dailymotion': 'ea non', 'deezer': 'consequat', 'digitalocean': 'dolor ex commodo', 'dingtalk': 'ipsum', 'discord': 'adipisicing quis', 'displayName': '先出听面', 'douyin': 'consequat sit', 'dropbox': 'deserunt irure cupidatat tempor', 'educateUser': {'avatar': 'http://dummyimage.com/100x100', 'birthDate': '1978-08-11', 'createdTime': '2014-03-04 00:52:36', 'currentUnit': 'nostrud cupidatat magna culpa est', 'departmentId': '88', 'departmentNames': '种委己切', 'email': 'b.rmrofqjxki@qq.com', 'gender': '女', 'idCardNumber': '41', 'idCardType': '77', 'identity': '61', 'identityNames': '打线结角下号', 'identityType': '84', 'identityTypeNames': '林学育', 'mainUnitName': '酸那物两月心', 'name': '长水技片完军', 'owner': 'exercitation aute elit Excepteur', 'phoneNumber': '94', 'realName': '思入权', 'sourceApp': 'quis dolore deserunt', 'updatedTime': '2021-08-30 14:57:08', 'userCode': '99', 'userId': '2', 'userStatus': 'magna adipisicing'}, 'education': 'irure in laboris ea in', 'email': 'm.mmrwtk@qq.com', 'emailVerified': False, 'eveonline': 'ad', 'externalId': '25', 'facebook': 'dolore dolor', 'firstName': '空适带化的断', 'fitbit': 'ut et', 'gender': '男', 'gitea': 'nisi aliqua dolor qui elit', 'gitee': 'aute amet irure', 'github': 'laboris esse', 'gitlab': 'deserunt culpa laborum non', 'google': 'velit consequat aute Lorem', 'groups': ['consectetur'], 'hash': 'voluptate eiusmod aliqua velit', 'heroku': 'in dolor', 'homepage': 'quis do sit velit qui', 'id': '87', 'idCard': '52', 'idCardType': '53', 'influxcloud': 'nulla eu est laborum cupidatat', 'infoflow': 'ex eiusmod dolor nisi mollit', 'instagram': 'tempor ipsum', 'intercom': 'reprehenderit commodo', 'isAdmin': False, 'isDefaultAvatar': False, 'isDeleted': False, 'isForbidden': True, 'isOnline': True, 'kakao': 'labore Ut in culpa voluptate', 'karma': 74, 'language': 'fugiat', 'lark': 'dolore', 'lastName': '内思第响共', 'lastSigninIp': '181.184.129.212', 'lastSigninTime': '2009-05-28 04:49:19', 'lastSigninWrongTime': '1983-02-07 03:04:25', 'lastfm': 'Lorem enim sit', 'ldap': 'eiusmod mollit ex occaecat', 'line': 'laborum ut in et', 'linkedin': 'Duis ut', 'location': 'exercitation in ullamco', 'mailru': 'x.jruyepb@qq.com', 'managedAccounts': [{'application': 'reprehenderit dolor elit Ut magna', 'password': 'magna nostrud', 'signinUrl': 'http://supes.gw/eaejtqm', 'username': '林芳'}], 'meetup': 'cupidatat sint tempor', 'metamask': 'culpa elit ex', 'mfaEmailEnabled': True, 'mfaPhoneEnabled': True, 'microsoftonline': 'sed in labore', 'multiFactorAuths': [{'countryCode': '73', 'enabled': False, 'isPreferred': True, 'mfaType': 'tempor culpa nulla dolore', 'recoveryCodes': ['12'], 'secret': 'exercitation', 'url': 'http://jfttvq.no/rqeiosze'}], 'name': '则群着志节合', 'naver': 'ex reprehenderit eu nostrud dolore', 'nextcloud': 'eu nostrud ex', 'okta': 'quis', 'onedrive': 'sunt ullamco minim in', 'orgObj': {'accountItems': [{'modifyRule': 'minim in sint', 'name': '清金知华细听', 'viewRule': 'aute sed', 'visible': True}], 'accountQuantity': '51', 'countryCodes': ['44'], 'createdTime': '2016-10-28 19:47:31', 'defaultApplication': 'laborum', 'defaultAvatar': 'http://dummyimage.com/100x100', 'defaultPassword': 'aliquip magna', 'displayName': '土活争回', 'educateUnits': [{'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}], 'enableSoftDeletion': True, 'favicon': 'http://dummyimage.com/100x100', 'initScore': 52, 'isProfilePublic': True, 'languages': ['et aute'], 'masterPassword': 'nisi est in irure Ut', 'mfaItems': [{'name': '格走思技不打构', 'rule': 'proident'}], 'name': '转华斯族风', 'orgType': 'ad pariatur veniam minim eu', 'overview': 'ea enim qui', 'owner': 'Lorem deserunt sed', 'passwordOptions': ['dolor nulla'], 'passwordSalt': 'quis eiusmod reprehenderit tempor', 'passwordType': 'ea nulla', 'status': 'dolor nisi adipisicing', 'tags': ['veniam dolor sunt qui'], 'themeData': {'borderRadius': 13, 'colorPrimary': 'non cillum Excepteur elit consectetur', 'isCompact': False, 'isEnabled': True, 'themeType': 'irure'}, 'unitCount': 'esse aute laboris tempor nulla', 'unitId': '78', 'websiteUrl': 'http://usiehdlm.pl/hbomleqnz'}, 'oura': 'in cupidatat incididunt consequat', 'owner': 'aliqua aute culpa nulla', 'password': 'est amet', 'passwordSalt': 'esse quis laboris Excepteur', 'passwordType': 'in Duis ad', 'patreon': 'in veniam anim commodo laborum', 'paypal': 'consectetur pariatur laboris aute', 'permanentAvatar': 'http://dummyimage.com/100x100', 'permissions': [{'actions': ['enim aliquip ullamco Duis'], 'adapter': 'ut esse', 'approveTime': '2004-09-18 12:05:34', 'approver': 'Lorem sit aute Excepteur voluptate', 'createdTime': '1982-11-19 06:26:43', 'description': '原斗术而果给这区于眼亲带里标正求计。至手公便清热问没指规以般物深素认九。号人十算引自造市里几白一温般为领林。置造往算务连她道反或实收根信观存低龙。今多商元人以影状越论却养通共还正之众。北复眼省北直用风物派成提公少话你积。', 'displayName': '给数酸学', 'domains': ['p.chek@qq.com'], 'effect': 'sunt in non aliqua magna', 'groups': ['ad laborum nostrud Ut incididunt'], 'isEnabled': False, 'model': 'labore incididunt fugiat amet esse', 'name': '开酸却见或他', 'owner': 'officia eiusmod', 'resourceType': 'culpa dolor anim cupidatat', 'resources': ['ipsum laboris'], 'roles': ['laborum culpa esse velit'], 'state': 'in elit quis cupidatat pariatur', 'submitter': 'aliquip ut anim', 'users': ['do']}], 'phone': '18170728388', 'preHash': 'dolore dolor ut', 'preferredMfaType': 'sed', 'properties': {'additionalProperties': 'enim'}, 'qq': 'in elit ut', 'ranking': 70, 'recoveryCodes': ['29'], 'region': 'in aute minim nostrud labore', 'roles': [{'createdTime': '2018-07-02 12:24:41', 'description': '求广方引产将写作市节民体矿三委万选明。华备必油应地儿海广期信眼能王系论研。内从战这在商形是八太情成容最改国自业。书系去书现市头开细已结四角这响。', 'displayName': '也委面求米酸', 'domains': ['p.knfquvoc@qq.com'], 'groups': ['Duis sit amet'], 'isEnabled': False, 'name': '或片严', 'owner': 'esse id sit amet ut', 'roles': ['dolor adipisicing tempor reprehenderit ea'], 'users': ['velit ea eu deserunt sunt']}], 'salesforce': 'occaecat pariatur amet', 'score': 94, 'shopify': 'sint nisi dolor Lorem', 'signinWrongTimes': 1438792728370, 'signupApplication': 'anim', 'slack': 'amet cupidatat consequat', 'soundcloud': 'do', 'spotify': 'labore tempor quis dolor', 'steam': 'consectetur adipisicing', 'strava': 'tempor', 'stripe': 'in Ut', 'tag': 'do in consectetur sed', 'tiktok': 'voluptate anim in Duis nostrud', 'title': '却行图好被权', 'totpSecret': 'sunt ipsum sit in', 'tumblr': 'amet ad sit et consequat', 'twitch': 'Ut Excepteur', 'twitter': 'ipsum', 'type': 'laboris ullamco sint', 'typetalk': 'ipsum', 'uber': 'cupidatat sint', 'updatedTime': '1971-02-02 11:23:26', 'userId': '16', 'vk': 'deserunt amet', 'web3onboard': 'dolore ipsum fugiat eu magna', 'webauthnCredentials': [], 'wechat': 'irure aliquip', 'wecom': 'sit', 'weibo': 'ex qui', 'wepay': 'officia', 'xero': 'ullamco id adipisicing', 'yahoo': 'fugiat nostrud sed et', 'yammer': 'sunt pariatur', 'yandex': 'cillum do pariatur', 'zoom': 'Excepteur fugiat incididunt cillum et'}]}], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}




        apiname = '/api/add-educate-unit'
        # 字典参数
        datadict = dict_data


        response = await send_orgcenter_request(apiname,datadict,'post',False)
        print(response,'接口响应')
        try:
            print(response)



            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None


