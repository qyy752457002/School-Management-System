# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import json

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
import hashlib

import shortuuid
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select, or_

from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.enum_value_dao import EnumValueDAO
from daos.planning_school_dao import PlanningSchoolDAO
from daos.school_dao import SchoolDAO
from models.planning_school import PlanningSchool
from models.school import School
from models.student_transaction import AuditAction
from rules.common.common_rule import send_request
from rules.enum_value_rule import EnumValueRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config
from views.models.extend_params import ExtendParams
from views.models.institutions import InstitutionKeyInfo
# from rules.planning_school_rule import PlanningSchoolRule
from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolTransactionAudit, PlanningSchoolKeyInfo
from views.models.school import School as SchoolModel, SchoolKeyAddInfo, SchoolKeyInfo

from views.models.school import SchoolBaseInfo
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus
from views.models.system import PLANNING_SCHOOL_OPEN_WORKFLOW_CODE, SCHOOL_OPEN_WORKFLOW_CODE, \
    PLANNING_SCHOOL_CLOSE_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, PLANNING_SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, \
    SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE


@dataclass_inject
class SchoolRule(object):
    school_dao: SchoolDAO
    p_school_dao: PlanningSchoolDAO
    enum_value_dao: EnumValueDAO
    system_rule: SystemRule
    other_mapper={"school_name": "institution_name",
                  "school_no": "institution_code",
                  "school_en_name": "institution_en_name",
                  "school_org_type": "institution_type",

                  }



    async def get_school_by_id(self, school_id,extra_model=None):
        # other_mapper={ }
        school_db = await self.school_dao.get_school_by_id(school_id)
        if not school_db:
            return None
        if extra_model:
            if (extra_model== InstitutionKeyInfo):
                # 加了转换
                pass


            school = orm_model_to_view_model(school_db, extra_model,other_mapper=self.other_mapper)
        else:
            school = orm_model_to_view_model(school_db, SchoolModel)
        return school

    async def get_school_by_school_name(self, school_name):
        school_db = await self.school_dao.get_school_by_school_name(
            school_name)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school

    async def add_school(self, school: SchoolModel):
        exists_school = await self.school_dao.get_school_by_school_name(
            school.school_name)
        if exists_school:
            raise Exception(f"学校{school.school_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        school_db = view_model_to_orm_model(school, School,    exclude=["id"])

        school_db.status =  PlanningSchoolStatus.DRAFT.value
        school_db.created_uid = 0
        school_db.updated_uid = 0
        if school.planning_school_id and  school.planning_school_id>0 :
            # rule互相应用有问题  用dao
            p_exists_school_model = await self.p_school_dao.get_planning_school_by_id(  school.planning_school_id)
            if not p_exists_school_model:
                raise PlanningSchoolNotFoundError()
            print(p_exists_school_model,999)

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
        school = orm_model_to_view_model(school_db, SchoolKeyAddInfo, exclude=["created_at",'updated_at'])
        return school


    async def add_school_from_planning_school(self, planning_school: PlanningSchool):
        # todo 这里的值转换 用 数据库db类型直接赋值  模型转容易报错   另 其他2个表的写入
        return None
        school = orm_model_to_view_model(planning_school, SchoolKeyAddInfo, exclude=["id"])
        school.school_name = planning_school.planning_school_name
        school.planning_school_id = planning_school.id

        school.school_no = planning_school.planning_school_no
        school.borough = planning_school.borough
        school.block = planning_school.block
        # school.school_type = planning_school.planning_school_type
        school.school_edu_level = planning_school.planning_school_edu_level
        school.school_category = planning_school.planning_school_category
        school.school_operation_type = planning_school.planning_school_operation_type
        school.school_org_type = planning_school.planning_school_org_type
        school.school_level = planning_school.planning_school_level
        school.school_code = planning_school.planning_school_code

        exists_school = await self.school_dao.get_school_by_school_name(
            school.school_name)
        if exists_school:
            raise Exception(f"学校{school.school_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        school_db = view_model_to_orm_model(school, School,    exclude=["id"])

        school_db.status =  PlanningSchoolStatus.DRAFT.value
        school_db.created_uid = 0
        school_db.updated_uid = 0
        print(school_db)

        school_db = await self.school_dao.add_school(school_db)
        school = orm_model_to_view_model(school_db, SchoolKeyAddInfo, exclude=["created_at",'updated_at'])
        return school
    # 废弃 未使用
    async def update_school(self, school,ctype=1):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"学校{school.id}不存在")
        if ctype==1:
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
            school_db.school_name=school.school_name
            school_db.school_short_name=school.school_short_name
            school_db.school_code=school.school_code
            school_db.create_school_date=school.create_school_date
            school_db.founder_type=school.founder_type
            school_db.founder_name=school.founder_name
            school_db.urban_rural_nature=school.urban_rural_nature
            school_db.school_edu_level=school.school_edu_level
            school_db.school_org_form=school.school_org_form
            school_db.school_category=school.school_category
            school_db.school_operation_type=school.school_operation_type
            school_db.department_unit_number=school.department_unit_number
            school_db.sy_zones=school.sy_zones
            school_db.historical_evolution=school.historical_evolution


        school_db = await self.school_dao.update_school(school_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""])
        return school_db

    async def update_school_byargs(self, school,):
        exists_school = await self.school_dao.get_school_by_id(school.id)
        if not exists_school:
            raise Exception(f"单位{school.id}不存在")
        if exists_school.status== PlanningSchoolStatus.DRAFT.value:
            exists_school.status= PlanningSchoolStatus.OPENING.value
            school.status= PlanningSchoolStatus.OPENING.value
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
        return school_db

    async def delete_school(self, school_id):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"单位{school_id}不存在")
        school_db = await self.school_dao.delete_school(exists_school)
        school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
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

    async def query_school_with_page(self, page_request: PageRequest,   school_name=None,school_no=None,school_code=None,
                                     block=None,school_level=None,borough=None,status=None,founder_type=None,
                                     founder_type_lv2=None,
                                     founder_type_lv3=None,planning_school_id=None,province=None,city=None ,institution_category=None,social_credit_code=None,school_org_type=None,extra_model =None):
        #  根据举办者类型  1及 -3级  处理为条件   1  2ji全部转换为 3级  最后in 3级查询
        enum_value_rule = get_injector(EnumValueRule)
        if founder_type:
            if len(founder_type) > 0:

                founder_type_lv2_res= await enum_value_rule.get_next_level_enum_values('founder_type'  ,founder_type)
                for item in founder_type_lv2_res:
                    founder_type_lv2.append(item.enum_value)


            # query = query.where(PlanningSchool.founder_type_lv2 == founder_type_lv2)
        if founder_type_lv2 and  len(founder_type_lv2)>0:
            founder_type_lv3_res= await enum_value_rule.get_next_level_enum_values('founder_type_lv2'  ,founder_type_lv2)
            for item in founder_type_lv3_res:
                founder_type_lv3.append(item.enum_value)

        paging = await self.school_dao.query_school_with_page(page_request,  school_name,school_no,school_code,
                                                                block,school_level,borough,status,founder_type,
                                                                founder_type_lv2,
                                                                founder_type_lv3,planning_school_id,province,city,institution_category,social_credit_code,school_org_type
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        if extra_model:
            # paging.data = [extra_model(**item) for item in paging.data]
            paging_result = PaginatedResponse.from_paging(paging, extra_model,other_mapper=self.other_mapper)

        else:
            paging_result = PaginatedResponse.from_paging(paging, SchoolModel)
        return paging_result


    async def update_school_status(self, school_id, status,action=None):
        exists_school = await self.school_dao.get_school_by_id(school_id)
        if not exists_school:
            raise Exception(f"单位{school_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_school.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"单位当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_school.status,2222222)
        school_db = await self.school_dao.update_school_byargs(exists_school,*need_update_list)


        # school_db = await self.school_dao.update_school_status(exists_school,status)
        # school = orm_model_to_view_model(school_db, SchoolModel, exclude=[""],)
        return school_db


    # 搜索使用
    async def query_schools(self,school_name,extend_params:ExtendParams|None,school_id=None,block=None,borough=None):
        # block,borough
        session = await db_connection_manager.get_async_session("default", True)
        query = select(School)
        if school_name:
            if ',' in school_name:
                school_name = school_name.split(',')
                if isinstance(school_name, list):
                    query = query.where(School.school_name.in_(school_name))
            else:
                query = query.where(School.school_name.like(f'%{school_name}%') )
        if school_id:
            if ',' in school_id:
                school_id = school_id.split(',')
                if isinstance(school_id, list):
                    query = query.where(School.id.in_(school_id))
            else:
                query = query.where(School.id==school_id  )
        if block:
            if ',' in block:
                block = block.split(',')
                if isinstance(block, list):
                    query = query.where(School.block.in_(block))
            else:
                query = query.where(School.block.like(f'%{block}%') )
        if borough:
            if ',' in borough:
                borough = borough.split(',')
                if isinstance(borough, list):
                    query = query.where(School.borough.in_(borough))
            else:
                query = query.where(School.borough.like(f'%{borough}%') )
        # print(extend_params,3333333333)
        if extend_params:
            if extend_params.school_id:
                query = query.where(School.id == int(extend_params.school_id)  )
            if extend_params.planning_school_id:
                query = query.where(School.planning_school_id == int(extend_params.planning_school_id)  )

            if extend_params.county_name:
                # 区的转换   or todo
                # enuminfo = await self.enum_value_dao.get_enum_value_by_value(extend_params.county_id, 'country' )
                query = query.filter( or_( School.block == extend_params.county_name , School.borough == extend_params.county_name))


                # if enuminfo:
                pass
            if extend_params.system_type:
                pass

        result = await session.execute(query)
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, SchoolModel)

            # account = PlanningSchool(school_id=row.school_id,
            #                  grade_no=row.grade_no,
            #                  grade_name=row.grade_name,
            #                  grade_alias=row.grade_alias,
            #                  description=row.description)
            lst.append(planning_school)
        return lst

    # 向工作流中心发送申请
    async def add_school_work_flow(self, school_flow: SchoolModel,):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = SCHOOL_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        datadict['block'] =   school_flow.block
        datadict['borough'] =   school_flow.borough
        datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no
        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['school_id'] = school_flow.id

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
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


    async def add_school_close_work_flow(self, school_flow: PlanningSchoolModel,action_reason,related_license_upload):
        # school_flow.id=0
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = SCHOOL_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        datadict['block'] =   school_flow.block
        datadict['borough'] =   school_flow.borough
        datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no

        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload
        dicta['school_id'] = school_flow.id

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

        datadict = dict()
        if audit_info.process_instance_id>0:
            node_id=await self.system_rule.get_work_flow_current_node_by_process_instance_id(  audit_info.process_instance_id)
            audit_info.node_id=node_id['node_instance_id']


        # 节点实例id
        datadict['node_instance_id'] =  audit_info.node_id

        apiname = '/api/school/v1/teacher-workflow/process-work-flow-node-instance'
        # from urllib.parse import urlencode
        # apiname += ('?' + urlencode(datadict))


        # 如果是query 需要拼接参数

        # 字典参数
        datadict ={"user_id":"11","action":"approved",**datadict}
        if audit_info.transaction_audit_action== AuditAction.PASS.value:
            datadict['action'] = 'approved'
        if audit_info.transaction_audit_action== AuditAction.REFUSE.value:
            datadict['action'] = 'rejected'

        response = await send_request(apiname,datadict,'post',True)
        print(response,'接口响应')
        if audit_info.transaction_audit_action== AuditAction.PASS.value:
            # 成功则写入数据
            # transrule = get_injector(StudentTransactionRule)
            # await transrule.deal_student_transaction(student_edu_info)
            res2 = await self.deal_school(audit_info.process_instance_id, action)
        # 终态的处理

        await self.set_transaction_end(audit_info.process_instance_id, audit_info.transaction_audit_action)



        return response
        pass

    async def deal_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        school = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到规划信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
        if action=='close':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            planning_school_orm = SchoolKeyInfo(**json_data)
            planning_school_orm.id= school.id

            res = await self.update_school_byargs(  planning_school_orm)
            pass

        # res = await self.update_school_status(school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass

    async def add_school_keyinfo_change_work_flow(self, school_flow: SchoolKeyInfo,):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['school_no'] = school_flow.school_no

        datadict['school_name'] = school_flow.school_name
        datadict['school_edu_level'] =   school_flow.school_edu_level
        datadict['block'] =   school_flow.block
        datadict['borough'] =   school_flow.borough
        datadict['school_level'] =   school_flow.school_level
        datadict['school_category'] =   school_flow.school_category
        datadict['school_operation_type'] =   school_flow.school_operation_type
        datadict['school_org_type'] =   school_flow.school_org_type

        datadict['apply_user'] =  'tester'
        mapa = school_flow.__dict__
        mapa['school_id'] = school_flow.id
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
        # 节点实例id    自动获取
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


    async def set_transaction_end(self,process_instance_id,status):
        tinfo=await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if tinfo:
            tinfo.workflow_status=status.value
            await self.update_school_byargs(tinfo)


        pass
    async def is_can_not_add_workflow(self, student_id,is_all_status_allow=False):
        tinfo=await self.get_school_by_id(student_id)
        if not is_all_status_allow:
            if tinfo and  tinfo.status == PlanningSchoolStatus.DRAFT.value:
                return True
        # 检查是否有占用
        if tinfo and  tinfo.workflow_status == AuditAction.NEEDAUDIT.value:
            return True
        return False
